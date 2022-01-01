import os
from dotenv import load_dotenv
from flask import Flask, Blueprint, jsonify
from flask_restx import Api
from ma import ma
from db import db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from resources.product import Product, ProductList, product_ns, products_ns
from marshmallow import ValidationError

app = Flask(__name__)
bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp, doc='/doc', title='API Documentation of products')
app.register_blueprint(bp)
load_dotenv()
db_uri = 'mysql://maker:toor@localhost:3306/flask-rest-mysql'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(product_ns)
api.add_namespace(products_ns)

@app.before_first_request
def setup_database():
  engine = create_engine(db_uri)
  if not database_exists(engine.url):
    create_database(engine.url)
    print("New database created" + database_exists(engine.url))
  else:
    print("Database already exists")
  db.create_all()

@api.errorhandler(ValidationError)
def handle_validation_error(error):
  return jsonify(error.message), 400

product_ns.add_resource(Product, '/<int:id>')
products_ns.add_resource(ProductList)

db.init_app(app)
ma.init_app(app)

if __name__ == '__main__':
  app.run(
    port = os.getenv('PORT'), 
    debug = os.getenv('DEBUG'), 
    host = os.getenv('HOST')
  )
