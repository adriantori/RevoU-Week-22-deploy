import os
from flask import Flask
import flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_talisman import Talisman

from db import db, db_init
from auth.apis import auth_blueprint
from todo.apis import todo_blueprint

app = Flask(__name__)
flask.json.provider.DefaultJSONProvider.sort_keys = False

CORS(app)
Talisman(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:smittywerbenjagermanjensen@db.cxebhyrtajkjbwvricio.supabase.co:5432/postgres"
db.init_app(app)
app.config['JWT_SECRET_KEY'] = "watzittooya"
jwt = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix="")
app.register_blueprint(todo_blueprint, url_prefix="")

# with app.app_context():
#     db_init()