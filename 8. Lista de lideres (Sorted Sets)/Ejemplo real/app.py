import flask_session
import redis
from flask import Flask, render_template, redirect, session, request, abort

import reset
import storage
from decorator import check_quota

UP_VOTE = "upvote"

#VOTE_SYSTEM = "single"
VOTE_SYSTEM = "multiple"

# Initialize & Configure Flask App
app = Flask(__name__)
app.config.setdefault('SESSION_TYPE', 'redis')
app.config.from_object(__name__)

# Start Flask Session
flask_session.Session(app)

# Start Redis Connection
conn = redis.Redis()


@app.route('/reset-app')
def reset_app():
    reset.reset(conn, session)
    return redirect("/")


def update_user_id():
    user_id = request.args.get('user_id', '')
    if user_id:
        session["user_id"] = int(user_id)
    if 'user_id' not in session:
        session['user_id'] = 1


@app.route('/')
@check_quota
def home():
    def get_rate_limits():
        return {
            'current': rate_limit_repository.get(session["user_id"]),
            'max': rate_limit_repository.getMaxRequests(),
        }
    def get_top_books():
        return [post_repository.get(id) for id in ranking.get_ratings("books:top", 3)]

    # Conseguir un objeto CONF para cada request, y generar todos los Repositorios a partir de ello
    # Lo hacemos dinamico? No please. No empezemos.
    pages_repository = storage.pages.Pages(conn)
    post_repository = storage.post.Post(conn)
    votes_repository = storage.post_vote.repository_by_name(conn, VOTE_SYSTEM)
    rate_limit_repository = storage.ratelimit.RateLimit(conn)
    ranking = storage.ranking.Ranking(conn)

    # Remove from here and add it to a Configuration Screen
    update_user_id()

    # Get all the "post to show on the HOME listing"
    page = storage.pages.Page(pages_repository, "home")
    post_ids = page.get_posts()

    return render_template('home.html', **{
        'posts': post_repository.get_all(post_ids),
        'votes': votes_repository.get_votes_by_user(session["user_id"], post_ids),
        'visits': page.visit(),
        'rate_limits': get_rate_limits(),
        'user_id': session["user_id"],
        'top_books': get_top_books(),
    })


@app.route('/posts', methods=['POST'])
def new_post():
    repository = storage.post.Post(conn)
    title = request.form.get('title')
    if not title:
        abort(400, "Invalid arguments")

    post = {"title": title}
    id = repository.create(post)

    pages_repository = storage.pages.Pages(conn)
    page = storage.pages.Page(pages_repository, "home")
    page.add(id)

    return redirect("/")


@app.route('/post/<post_id>/<string:action>')
def like(post_id: int, action: str):
    votes = storage.post_vote.repository_by_name(conn, VOTE_SYSTEM)

    user_id = session['user_id']

    if action == UP_VOTE:
        votes.vote(user_id, post_id)
        update_ranking(post_id, 1)
    else:
        votes.downvote(user_id, post_id)
        update_ranking(post_id, -1)

    return redirect("/")


def update_ranking(post_id: int, amount: int):
    ranking = storage.ranking.Ranking(conn)
    ranking.increase("books:top", amount, str(post_id))


if __name__ == '__main__':
    app.run(debug=True)
