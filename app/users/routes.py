import datetime
import os
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models.user_model import UserModel
from app.erros import not_found
from bson.json_util import dumps
from pymongo.errors import PyMongoError
import jwt
from app.users.decorator import authenticated_user

users_bp = Blueprint('users', __name__)
secret_key = os.getenv("SECRET_KEY")


@users_bp.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json.get('name')
    _email = _json.get('email')
    _password = _json.get('password')

    if _name and _email and _password:
        _hashed_password = generate_password_hash(_password)
    try:
        UserModel.add_user(_name, _email, _hashed_password)
        return jsonify({"message": "User added successfully"}), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while getting the users", "details": str(e)}), 500

@users_bp.route('/', methods=['GET'])
@authenticated_user
def users(user):
    print(user)
    try:
        users = UserModel.get_users()
        return dumps(users), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while getting the users", "details": str(e)}), 500

@users_bp.route('/users/<id>', methods=['GET'])
def user(id):
    try:
        user = UserModel.get_user_by_id(id)
        return dumps(user), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while getting the user", "details": str(e)}), 500

@users_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    _json = request.json
    _name = _json.get('name')
    _email = _json.get('email')
    _password = _json.get('password')

    if _name and _email and _password:
        _hashed_password = generate_password_hash(_password)
    try:
        UserModel.update_user(id, _name, _email, _hashed_password)
        return jsonify({"message": 'User updated'}), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while updating the user", "details": str(e)}), 500
        

@users_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        UserModel.delete_user(id)
        return jsonify("User deleted"), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while deleting the user", "details": str(e)}), 500
