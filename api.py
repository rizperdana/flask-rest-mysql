from flask import Blueprint
from flask_restx import Api
from resources.product import api as product_api

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp, doc='/doc', title='API Documentation of products')

def initialize_api():
  api.add_namespace(product_api)