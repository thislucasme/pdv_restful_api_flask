
from bson.objectid import ObjectId
from app import mongo
from flask import jsonify
from pymongo.errors import PyMongoError
from werkzeug.security import check_password_hash
import os
from dataclasses import asdict
from app.schemas.query_product_pagination import QueryProductPagination
from app.schemas.product_schema import Product
import copy

class ProdutoModel:
    @staticmethod
    def create_product(product):
        try:
            product_data = asdict(product)
            product_data_for_insert = copy.deepcopy(product_data)
            product_data_for_insert.pop('_id', None)
            result = mongo.db.products.insert_one(product_data_for_insert)
            inserted_product = {**product_data_for_insert, "_id": str(result.inserted_id)}
            return inserted_product
        except PyMongoError as e:
            raise e 

    @staticmethod
    def get_users(user, query_pagination: QueryProductPagination):
        try:

            result = mongo.db.products.find()
            return result
        except PyMongoError as e:
            raise e 