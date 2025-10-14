from flask_restful import Resource, request
from database import SessionLocal
import models
from marshmallow import ValidationError
from resources.schemas import check_username, register_schema, login_schema
from flask_jwt_extended import create_access_token
from datetime import timedelta
from logger import LOGGER


class RegisterUser(Resource):
    def get(self):
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            data = check_username.load(data)
        except ValidationError as error:
            return {"message": "Wrong request"}, 400
        LOGGER.info("fetching username")
        session = SessionLocal()
        user = (
            session.query(models.User)
            .filter(models.User.username == data["username"])
            .first()
        )
        session.close()
        LOGGER.info("returning username")
        if user:
            return {"username": user.username}, 200
        return {"message": "User not found"}, 404

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400

        try:
            data = register_schema.load(data)
        except ValidationError as error:
            return {"message": "Invalid request"}, 400
        new_user = models.User(**data)
        LOGGER.info("Checking if username exist")
        session = SessionLocal()
        user = (
            session.query(models.User)
            .filter(models.User.username == data["username"])
            .first()
        )
        if user:
            return {"message": "User already exist"}, 409
        LOGGER.info("Registering new user username")
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()
        return {"message": "Created new user"}, 201


class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            data = login_schema.load(data)
        except ValidationError as error:
            return {"message": "Wrong request"}, 400
        LOGGER.info("Validating input")
        session = SessionLocal()
        user = (
            session.query(models.User)
            .filter(models.User.username == data["username"])
            .first()
        )

        if user:
            if user.password == data["password"]:
                jwt_token = create_access_token(
                    identity=str(user.id),
                    expires_delta=timedelta(hours=1),
                )
                return {"access_token": jwt_token}, 200
            else:
                return {"message": "Invalid credentials"}, 401
        else:
            return {"message": "User not found"}, 404
