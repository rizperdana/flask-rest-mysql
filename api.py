from flask import Blueprint
from flask_restx import Api
from resources.product import api as product_api
from resources.variant import api as variant_api
from resources.image import api as image_api

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp, doc='/doc', title='API Documentation of Product Variant')

def initialize_api():
  api.add_namespace(product_api)
  api.add_namespace(variant_api)
  api.add_namespace(image_api)