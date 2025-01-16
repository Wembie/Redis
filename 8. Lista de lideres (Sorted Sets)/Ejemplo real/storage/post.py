import json
import redis


class Post:
    def __init__(self, conn: redis.Redis):
        self.conn = conn

    def create(self, post: dict):
        post['id'] = self.next_post_id()
        self.save(post)
        return post['id']

    def save(self, post: dict):
        self.conn.hmset(
            self.post_key(post['id']),
            {'payload': json.dumps(post), 'likes': "0"},
        )

    def get(self, id: int):
        postAll = self.conn.hgetall(self.post_key(id))
        if not postAll:
            return {}

        post = json.loads(postAll[b'payload'])
        post['likes'] = int(postAll[b'likes']) or 0
        return post

    def get_all(self, ids: list):
        posts = []
        for id in ids:
            post = self.get(id)
            if not post:
                continue
            posts.append(post)
        return posts

    @staticmethod
    def post_key(id_post: int):
        return "post:%s" % id_post

    def next_post_id(self) -> int:
        return self.conn.incr("posts:id")

