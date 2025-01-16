import redis


class Ranking:
    def __init__(self, conn: redis.Redis):
        self.conn = conn

    def get_ratings(self, page: str, count=10):
        return map(lambda x: x.decode('ascii'), self.conn.zrevrange(self.key(page), 0, count-1))

    def increase(self, page: str, amount: int, member: str):
        return self.conn.zincrby(self.key(page), amount, member)

    def key(self, page):
        return "ranking:%s" % page
