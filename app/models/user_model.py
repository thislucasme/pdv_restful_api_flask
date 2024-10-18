
from bson.objectid import ObjectId
from app import mongo
from flask import jsonify
from pymongo.errors import PyMongoError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

secret_key = os.getenv("SECRET_KEY")

class UserModel:

    @staticmethod
    def add_user(name, email, password):
        return mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'pwd': password
        })

    @staticmethod
    def get_users():
        return mongo.db.users.find()

    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def validate(username, password):
        user =  mongo.db.users.find_one({'email': username})

        username_result = user['email']
        pwd_result = user['pwd']


        if username == username_result and check_password_hash(pwd_result, password):
            token = jwt.encode({
                'user': username,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
            }, secret_key)

            return jsonify({"token": token})
        return jsonify({"message": "Credenciais inválidas!"})

    @staticmethod
    def update_user(user_id, name, email, password):
        return mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'name': name, 'email': email, 'pwd': password}}
        )

    @staticmethod
    def delete_user(user_id):
        try:
            result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count
        except PyMongoError as e:
            raise e
