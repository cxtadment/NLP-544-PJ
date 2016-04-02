from flask import Flask
from app.models import db
from app.views import bp


def create_app():

    app = Flask(__name__)
    app.config.from_object('config')

    register_blueprints(app)
    register_database(app)

    return app


def register_blueprints(app):
    app.register_blueprint(bp)


def register_database(app):
    db.init_app(app)