
from bson.objectid import ObjectId
from app import mongo
from flask import jsonify
from pymongo.errors import PyMongoError
from werkzeug.security import check_password_hash
import jwt
import datetime
import os

secret_key = os.getenv("SECRET_KEY")

class AuthModel:
    @staticmethod
    def validate(username, password):
        try:
            user =  mongo.db.users.find_one({'email': username})
            user_id: str = user['_id']

            username_result = user['email']
            pwd_result = user['pwd']

            if username == username_result and check_password_hash(pwd_result, password):
                token = jwt.encode({
                    '_id': str(user_id),
                    'user': username,
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
                }, secret_key)

                return jsonify({"token": token})
            return jsonify({"message": "Credenciais inválidas!"})
        except PyMongoError as e:
            raise e
