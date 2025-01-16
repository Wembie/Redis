import functools

from flask import session, abort

import storage
import redis


def check_quota(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        client = redis.Redis()
        rl = storage.ratelimit.RateLimit(client)
        if session.get("user_id") and not rl.update(session.get("user_id")):
            description = "Quota exceeded! Number of requests: %s. Max Requests: %s" % (rl.get(session["user_id"]), rl.getMaxRequests())
            client.close()
            abort(403, description=description)

        client.close()
        return f(*args, **kwargs)

    return decorated_function