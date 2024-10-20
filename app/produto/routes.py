import datetime
import os
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from app.models.produto_model import ProdutoModel
from app.erros import not_found
from bson.json_util import dumps
from pymongo.errors import PyMongoError
import jwt
from app.users.decorator import authenticated_user
from app.schemas.product_schema import Product, ProdutoSchema
from app.schemas.query_product_pagination import QueryProductPagination, QueryProductPaginationSchema


produto_bp = Blueprint('produto', __name__)
secret_key = os.getenv("SECRET_KEY")

produto_schema = ProdutoSchema()
queryPagination_schema = QueryProductPaginationSchema()

@produto_bp.route('/', methods=['POST'])
def create_product():
    _json = request.json
    product_data: Product = None

    try:

        product_data = produto_schema.load(_json)

    except ValidationError as e:
       return jsonify({"error": "Invalid data", "details": str(e.messages)}), 400
    
    try:
        product = ProdutoModel.create_product(product_data)
        return product
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while creating a product", "details": str(e)}), 500

@produto_bp.route('/pagination', methods=['GET'])
@authenticated_user
def pagination(user):
    _json = request.json
    _query_params = request.args

    try:
        params: QueryProductPagination = queryPagination_schema.load(_query_params)
    except ValidationError as e:
       return jsonify({"error": "Invalid data", "details": str(e.messages)}), 400
    
    try:
        products = ProdutoModel.get_users(user, params)
        return dumps(products)
    except PyMongoError as e:
        return jsonify({"error": "An error occurred while creating a product", "details": str(e)}), 500
