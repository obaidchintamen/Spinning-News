from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_marshmallow import Marshmallow

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app import routes, models
models.db.create_all()

