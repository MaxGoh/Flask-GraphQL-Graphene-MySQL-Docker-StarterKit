from flask import Flask, jsonify
from strawberry.flask.views import GraphQLView

from app.extensions import db, jwt, migrate


def create_app(config_object: str = "config.Config", **overrides) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config.update(overrides)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"status": 401, "msg": "The token has expired"}), 401

    from app import models  # noqa: F401  (register models with SQLAlchemy)
    from app.graphql.schema import schema

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphql_ide="graphiql"),
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
