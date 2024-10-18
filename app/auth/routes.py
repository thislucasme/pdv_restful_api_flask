import datetime
import os
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models.user_model import UserModel
from app.erros import not_found
from bson.json_util import dumps
from pymongo.errors import PyMongoError
import jwt
from app.auth.decorator import current_user

auth_bp = Blueprint('auth', __name__)
secret_key = os.getenv("SECRET_KEY")

@auth_bp.route('login', methods=['POST'])
def login():
    auth = request.json

    if not auth or  not 'username' in auth or not 'password' in auth:
        return jsonify({"message": "Credenciais inválidas"}), 401
    
    username = auth['username']
    password = auth['password']
    try:
        user = UserModel.validate(username= username, password= password)
        return user
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while login", "details": str(e)}), 500

@auth_bp.route('/add', methods=['POST'])
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

@auth_bp.route('/users', methods=['GET'])
@current_user
def users(user):
    try:
        users = UserModel.get_users()
        return dumps(users), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while getting the users", "details": str(e)}), 500

@auth_bp.route('/users/<id>', methods=['GET'])
def user(id):
    try:
        user = UserModel.get_user_by_id(id)
        return dumps(user), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while getting the user", "details": str(e)}), 500

@auth_bp.route('/users/<id>', methods=['PUT'])
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
        

@auth_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        UserModel.delete_user(id)
        return jsonify("User deleted"), 200
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while deleting the user", "details": str(e)}), 500
