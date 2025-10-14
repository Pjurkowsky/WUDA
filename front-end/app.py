from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.api_calls import (
    fetch_post,
    NewComment,
    fetch_posts,
    NewPost,
    add_post,
    add_comment,
    Login,
    login_user,
    register_user,
    RegisterUser,
    add_game_req,
    get_games_req,
)
from pydantic import ValidationError
from settings import SECRET_KEY, APP_PORT, APP_HOST
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app_errors.log",
)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.context_processor
def inject_user_info():
    if session.get("login", None):
        return dict(curr_user=session["login"])
    return dict(curr_user=None)


@app.errorhandler(500)
def internal_server_error(e):
    logger.exception("Internal server error: %s", e)
    return render_template("500.html"), 500


@app.route("/game/<int:game_id>")
def game_detail(game_id):
    game = get_games_req(game_id)
    return render_template("game_detail.html", game=game)


@app.route("/game/add", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        new_game = {
            "title": request.form["title"],
            "players": request.form.get("players", ""),
            "playtime": request.form.get("playtime", ""),
            "short_description": request.form.get("short_description", ""),
            "description": request.form.get("description", ""),
            "image_url": request.form.get("image_url", ""),
        }
        add_game_req(new_game)
        return redirect(url_for("index"))
    return render_template("add_game.html")


@app.route("/")
def index():
    games = get_games_req()
    session["games"] = games
    return render_template("index.html", games=games)


@app.route("/forum")
def forum():
    posts = fetch_posts()
    game_id = request.args.get("game_id", type=int)
    games = session["games"]
    use_filter = request.args.get("use_filter") == "on"
    if use_filter and game_id:
        posts = [p for p in posts if p.game and p.game.id == game_id]

    return render_template(
        "forum/forum.html",
        posts=posts,
        games=games,
        selected_game=game_id,
        use_filter=use_filter,
    )


@app.route("/forum/<int:post_id>")
def post_detail(post_id):
    post = fetch_post(post_id)
    print(post)
    return render_template("forum/post_detail.html", post=post)


@app.route("/forum/<int:post_id>/", methods=["POST"])
def post_comment(post_id):
    data = NewComment.model_validate(request.form.to_dict())
    add_comment(post_id, data)
    return redirect(url_for("post_detail", post_id=post_id))


@app.route("/forum/new", methods=["POST", "GET"])
def new_post():

    if request.method == "POST":
        form_data = request.form.to_dict()
        try:
            post_data = NewPost(**form_data)
            if add_post(post_data):
                return redirect(url_for("forum"))
            else:
                return render_template("forum/post_form.html", games=session["games"])
        except ValidationError as e:
            flash("❌ Błąd walidacji: " + str(e), "error")
            return render_template("forum/post_form.html", form=form_data)
    return render_template("forum/post_form.html", games=session["games"])


@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = RegisterUser.model_validate(request.form.to_dict())
        if data.password != data.repeat_pwd:
            flash("Hasła nie sa takie same", "error")
            return
        if register_user(data):
            flash("Udało się zarejestrować", "success")
            return redirect(url_for("login"))
        else:
            flash("Nie udało się utworzyć użytkownika", "error")
    return render_template("auth/register.html")


# @app.route("/")
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_login = Login.model_validate(request.form.to_dict())
        resp = login_user(user_login)
        # print(resp['access_token'])
        if resp:
            flash("Udało się zalogować", "success")
            session["login"] = user_login.username
            session["access-token"] = resp["access_token"]
            return redirect("/")
        else:
            flash("Błedne dane logownia", "error")
    return render_template("auth/login.html")


@app.route("/auth/logout")
def logout():
    session.pop("login", None)
    session.pop("access-token", None)
    flash("Wylogowano", "success")
    return redirect("/")


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
