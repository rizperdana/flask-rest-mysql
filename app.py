import os
from dotenv import load_dotenv
from flask import Flask
from ma import ma
from db import db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from resources import load_resources, bp

app = Flask(__name__)
app.register_blueprint(bp)
load_resources()
load_dotenv()

db_uri = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.before_first_request
def setup_database():
  engine = create_engine(db_uri)
  if not database_exists(engine.url):
    create_database(engine.url)
    print("New database created" + database_exists(engine.url))
  else:
    print("Database already exists")
  db.create_all()

db.init_app(app)
ma.init_app(app)

if __name__ == '__main__':
  app.run(
    port = os.getenv('PORT'),
    debug = os.getenv('DEBUG'),
    host = os.getenv('HOST')
  )
