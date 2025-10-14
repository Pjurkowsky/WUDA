from marshmallow import Schema, fields
from datetime import datetime


class GameSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    players = fields.Str(required=True)
    playtime = fields.Int(required=True)
    short_description = fields.Str(required=True)
    description = fields.Str(required=True)
    image_url = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()


class GameSchemaListSingle(Schema):
    id = fields.Int()
    title = fields.Str()


class CommentAddSchema(Schema):
    content = fields.Str(required=True)


class CommentSchema(Schema):
    id = fields.Int()
    author = fields.Nested(UserSchema, many=False)
    content = fields.Str()
    author = fields.Nested(UserSchema)
    post_id = fields.Int(load_only=True)  # ukryte przy zwracaniu
    user_id = fields.Int(load_only=True)
    created_at = fields.Method("get_created_at")

    def get_created_at(self, obj):
        # serializacja do isoformat jak w przykładzie frontendowym
        return datetime.combine(obj.created_at, datetime.min.time()).isoformat()


class PostDetailsSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    created_at = fields.Method("get_created_at")
    author = fields.Nested(UserSchema)
    game = fields.Nested(GameSchemaListSingle)
    comments = fields.Nested(CommentSchema, many=True)

    def get_created_at(self, obj):
        # serializacja do isoformat jak w przykładzie frontendowym
        return datetime.combine(obj.created_at, datetime.min.time()).isoformat()


class PostListSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    created_at = fields.Method("get_created_at")
    author = fields.Nested(UserSchema)
    body = fields.Str()

    def get_created_at(self, obj):
        return datetime.combine(obj.created_at, datetime.min.time()).isoformat()


class PostAddSchema(Schema):
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    game_id = fields.Int()


class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterUser(LoginUserSchema):
    email = fields.Email(required=True)


class CheckUser(Schema):
    username = fields.Str(required=True)


game_schema = GameSchema()
games_schema = GameSchema(many=True)

check_username = CheckUser()
login_schema = LoginUserSchema()
register_schema = RegisterUser()

details_schema = PostDetailsSchema()
post_list_schema = PostListSchema(many=True)
post_add_schema = PostAddSchema()
comment_add_schema = CommentAddSchema()
comment_schema = CommentSchema()
