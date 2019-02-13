from config import Config

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object((set_environment_config()))

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def my_expired_token_callback():
        return jsonify({
            'status': 401,
            'sub_status': 42,
            'msg': 'The token has expired'
        }), 401

    db.init_app(app)

    from app.models.User import User
    from app.models.VerificationCode import VerificationCode

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.route('/')
    def hello_world():
        return "Hello World"

    from app.schema import schema

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # for having the GraphiQL interface
        )
    )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


def set_environment_config():
    if(Config.ENV == "PRODUCTION"):
        return 'config.ProductionConfig'
    elif (Config.ENV == "DEVELOPMENT"):
        return 'config.DevelopmentConfig'
