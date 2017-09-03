from flask import Flask


DEFAULT_DATABASE_URI = "postgresql://localhost/quest"


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DEFAULT_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    return app


def register_blueprints(app):
    from . import base, api
    app.register_blueprint(base.blueprint)
    app.register_blueprint(api.blueprint, url_prefix="/api")
