import redis


class Pages:
    def __init__(self, conn: redis.Redis):
        self.conn = conn

    def save(self, page: str, posts: list):
        self.conn.delete(self._get_key(page))
        self.conn.lpush(self._get_key(page), *posts)

    def get(self, page: str) -> list:
        return [int(id) for id in self.conn.lrange(self._get_key(page), 0, -1)]

    def count_visit(self, page: str):
        key = self._get_visit_key(page)
        return self.conn.incr(key, 1)

    def add(self, page, id, limit=None):
        self.conn.lpush(self._get_key(page), id)
        if limit:
            self.conn.ltrim(self._get_key(page), 0, limit-1)

    def _get_key(self, page: str) -> str:
        return "page:%s" % page

    def _get_visit_key(self, page: str) -> str:
        return "page:%s:visit-count" % page



class Page:
    def __init__(self, pages: Pages, name: str):
        self.pages = pages
        self.name = name

    def visit(self):
        return self.pages.count_visit(self.name)

    def get_posts(self):
        return self.pages.get(self.name)

    def add(self, id: int):
        self.pages.add(self.name, id, 6)
