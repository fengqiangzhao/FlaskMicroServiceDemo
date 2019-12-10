from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprint(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprint(app):
    from project.api.views import user_blueprint
    app.register_blueprint(user_blueprint)
