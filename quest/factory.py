import os

from flask import Flask

from .models import ModelEncoder


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/quest")


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json_encoder = ModelEncoder

    if config:
        app.config.update(config)

    return app


def register_blueprints(app):
    from . import base, api
    app.register_blueprint(base.blueprint)
    app.register_blueprint(api.blueprint, url_prefix="/api")
