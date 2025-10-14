from flask import Flask
from flask_restful import Api, Resource
from database import init_db, check_database
from resources.posts import *
from resources.auth import *
from resources.game import *
from settings import JWT_KEY, APP_PORT, APP_HOST
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = JWT_KEY
jwt = JWTManager(app)


init_db()


class Liveness(Resource):
    def get(self):
        return {"status": "I am alive"}, 200


class Readiness(Resource):
    def get(self):
        if check_database():
            return {"status": "I am ready"}, 200
        else:
            return {"status": "I am not ready. Connect database"}, 503


api.add_resource(RegisterUser, "/auth/register")
api.add_resource(LoginUser, "/auth/login")
api.add_resource(PostList, "/posts")
api.add_resource(PostDetails, "/posts/<int:post_id>")  # GET szczegóły posta
api.add_resource(PostComments, "/posts/<int:post_id>/comments")
api.add_resource(GameList, "/games", "/games/<int:game_id>")
api.add_resource(Liveness, "/liveness")
api.add_resource(Readiness, "/readiness")


if __name__ == "__main__":
    app.run(debug=True, host=APP_HOST, port=APP_PORT)
