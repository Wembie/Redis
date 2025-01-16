import redis

from storage.post import Post


class PostVote:
    def vote(self, user_id: int, id: int):
        self._vote(user_id, id, 1)

    def downvote(self, user_id: int, id: int):
        self._vote(user_id, id, -1)

    def _vote(self, user_id: int, post_id: int, value: int):
        raise ("Not implemented")

    def get_votes_by_user(self, user_id: int, post_ids: list) -> dict:
        return {}


class DumbPostVote(PostVote):
    def __init__(self, conn: redis.Redis):
        self.conn = conn

    def _vote(self, user_id: int, post_id: int, value: int):
        post_key = Post.post_key(post_id)
        self.conn.hincrby(post_key, "likes", value)


class SinglePostVote(PostVote):
    def __init__(self, conn: redis.Redis):
        self.conn = conn

    def _vote(self, user_id: int, post_id: int, value: int):
        if self.conn.sadd(self._key(user_id), post_id) != 0:
            self.conn.hincrby(Post.post_key(post_id), "likes", value)

    @staticmethod
    def _key(user_id) -> str:
        return "user:%s:votes:single" % user_id


class ChangeablePostVote(PostVote):
    def __init__(self, conn: redis.Redis):
        self.conn = conn

    def get_votes_by_user(self, user_id: int, post_ids: list) -> dict:
        if not post_ids:
            return {}

        rsp = self.conn.hmget(self._key(user_id), post_ids)
        rsp = [int(v) if v else None for v in rsp]
        return dict(zip(post_ids, rsp))

    def _vote(self, user_id: int, post_id: int, value: int):
        user_key = self._key(user_id)
        post_key = Post.post_key(post_id)

        if self.conn.hsetnx(user_key, post_id, value):
            # New vote
            self.conn.hincrby(post_key, "likes", value)
            return

        last_vote = self.conn.hget(user_key, post_id)
        if last_vote is None:
            # Edge case: cannot read the vote that should be there. Skipping.
            return

        last_vote = int(last_vote)
        if last_vote == value:
            # Exact same vote already processed
            return

        # Changing the vote
        pipeline = self.conn.pipeline()
        pipeline.hincrby(post_key, "likes", -last_vote + value)
        pipeline.hset(user_key, post_id, value)
        pipeline.execute()

    @staticmethod
    def _key(user_id) -> str:
        return "user:%s:votes:changeable" % user_id


def repository_by_name(conn: redis.Redis, name: str) -> PostVote:
    types = {
        "multiple": DumbPostVote,
        "single": SinglePostVote,
        "changeable": ChangeablePostVote,
    }

    return types[name](conn)
