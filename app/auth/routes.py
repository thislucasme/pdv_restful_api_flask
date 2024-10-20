import datetime
import os
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models.auth_model import AuthModel
from app.erros import not_found
from bson.json_util import dumps
from pymongo.errors import PyMongoError
import jwt

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
        user = AuthModel.validate(username= username, password= password)
        return user
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while login", "details": str(e)}), 500
