from flask_restful import Resource, request
from database import SessionLocal
import models
from datetime import date
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
from resources.schemas import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from logger import LOGGER


class PostDetails(Resource):
    def get(self, post_id: int):
        session = SessionLocal()
        LOGGER.info("Retrieving post")
        post = session.query(models.Post).filter(models.Post.id == post_id).first()
        return_dump = details_schema.dump(post)
        session.close()
        if post:
            return return_dump, 200
        else:
            return {"message": "Not found"}, 400


class PostList(Resource):
    def get(self):
        session = SessionLocal()
        posts = (
            session.query(models.Post)
            .options(
                joinedload(models.Post.author),
                joinedload(models.Post.game),
                joinedload(models.Post.comments).joinedload(models.Comment.author),
            )
            .all()
        )
        session.close()
        return post_list_schema.dump(posts), 200

    @jwt_required()
    def post(self):
        current_user = int(get_jwt_identity())
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            data = post_add_schema.load(data)
        except ValidationError:
            return {"message": "Wrong request"}, 400

        session = SessionLocal()
        new_post = models.Post(
            title=data["title"],
            body=data["body"],
            author_id=current_user,
            game_id=data.get("game_id"),
            created_at=date.today(),
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return_data = details_schema.dump(new_post)
        session.close()

        return return_data, 201


class PostComments(Resource):
    @jwt_required()
    def post(self, post_id: int):
        current_user = int(get_jwt_identity())
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            data = comment_add_schema.load(data)
        except ValidationError:
            return {"message": "Wrong request"}, 400
        LOGGER.info("Adding new post post")
        session = SessionLocal()
        post = session.query(models.Post).filter(models.Post.id == post_id).first()
        if not post:
            session.close()
            return {"message": "Post not found"}, 404

        new_comment = models.Comment(
            content=data["content"],
            post_id=post_id,
            user_id=current_user,
            created_at=date.today(),
        )
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
        return_data = comment_schema.dump(new_comment)
        session.close()
        post = session.query(models.Post).filter(models.Post.id == post_id).first()

        return return_data, 201
