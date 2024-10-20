from flask import Flask
from app.extention import mongo
from flask_pymongo import PyMongo
from app.users.routes import users_bp
from app.auth.routes import auth_bp
from app.produto.routes import produto_bp
from app.erros import not_found
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")
    
    mongo.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(produto_bp, url_prefix='/produtos')
    app.register_error_handler(404, not_found)

    return app
