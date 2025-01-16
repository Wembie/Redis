import redis


class RateLimit:
    SLICE_WINDOW_IN_SECOND = 5
    REQ_LIMIT_PER_WINDOW = 15

    def __init__(self, conn: redis.Redis):
        self.conn = conn

    def get(self, user: int) -> int:
        limit = self.conn.get(self._key(user))
        if not limit:
            return 0
        return int(limit)

    def update(self, user: int) -> bool:
        count = self.conn.incr(self._key(user), 1)
        if self.conn.ttl(self._key(user)) == -1:
            self.conn.expire(self._key(user), self.SLICE_WINDOW_IN_SECOND)
        if count > self.REQ_LIMIT_PER_WINDOW:
            return False
        return True

    def _key(self, user: int):
        return "user:%s:rate-limit" % user

    def getMaxRequests(self)-> int:
        return self.REQ_LIMIT_PER_WINDOW
