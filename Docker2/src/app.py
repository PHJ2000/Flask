from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.controller import v1_member
import wtforms_json
from instance.config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['WTF_CSRF_ENABLED'] = False
    wtforms_json.init()
    db.init_app(app)
    app.register_blueprint(v1_member, url_prefix='/member')
    return app
