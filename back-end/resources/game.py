from flask_restful import Resource, request
from marshmallow import ValidationError
from database import SessionLocal
import models
from resources.schemas import game_schema, games_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from logger import LOGGER


class GameList(Resource):
    def get(self, game_id=None):
        session = SessionLocal()
        if game_id == None:
            LOGGER.info("Id not provided, retrieving all games")
            games = session.query(models.Game).all()
            return_object = games_schema.dump(games)
        else:
            LOGGER.info("Id provided, retrieving single game")
            game = session.query(models.Game).filter(models.Game.id == game_id).first()
            return_object = game_schema.dump(game)
        session.close()
        return return_object, 200

    @jwt_required()
    def post(self):
        # current_user = int(get_jwt_identity())
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            LOGGER.info("Validating")
            game_data = game_schema.load(data)
        except ValidationError:
            return {"message": "Invalid request"}, 400
        LOGGER.info("Adding data")
        new_game = models.Game(**game_data)
        session = SessionLocal()
        session.add(new_game)
        session.commit()
        session.refresh(new_game)
        session.close()

        return game_schema.dump(new_game), 201
