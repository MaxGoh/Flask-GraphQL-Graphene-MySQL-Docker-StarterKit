import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    app = create_app(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        JWT_SECRET_KEY="test-secret",
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def graphql(client, query, token=None, **variables):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = client.post("/graphql", json={"query": query, "variables": variables}, headers=headers)
    return resp.get_json()
