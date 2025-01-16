from flask_session import Session
from redis import Redis

import storage


def reset(conn: Redis, session: Session):
    posts = [
        {"title": "Hyperion"},
        {"title": "Start with Why"},
        {"title": "Why we sleep"},
        {"title": "The subtle are of not giving a F*ck"},
        {"title": "Do more"},
        {"title": "The war of art"},
    ]

    def empty_redis():
        conn.flushall()

    def register_user():
        session.clear()
        session.setdefault("user_id", 1)

    def insert_posts():
        repository = storage.post.Post(conn)
        return [repository.create(p) for p in posts]

    def create_home_page(ids: list):
        repository = storage.pages.Pages(conn)
        repository.save("home", ids)

    empty_redis()
    register_user()
    post_ids = insert_posts()
    create_home_page(post_ids)

