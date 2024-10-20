
from functools import wraps
from flask import request, jsonify
import jwt
import os

secret_key = os.getenv("SECRET_KEY")

def authenticated_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"message": 'Token ausente!'}), 401
        
        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            kwargs['user'] = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401
        
        return f(*args, **kwargs)
    return decorated