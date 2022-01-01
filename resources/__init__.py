# This place contain namespace and resource

from flask import Blueprint, jsonify
from flask_restx import Api
from . import product
from marshmallow import ValidationError

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp, doc='/doc', title='API Documentation of products')

@api.errorhandler(ValidationError)
def handle_validation_error(error):
  return jsonify(error.message), 400

def load_resources():
  # namespace section
  api.add_namespace(product.product_ns)
  api.add_namespace(product.products_ns)

  # resource section
  product.product_ns.add_resource(product.Product, '/<int:id>')
  product.products_ns.add_resource(product.ProductList)