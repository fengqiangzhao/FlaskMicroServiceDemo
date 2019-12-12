from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprint(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprint(app):
    from project.api.views import user_blueprint
    app.register_blueprint(user_blueprint)
