from tests.conftest import graphql

REGISTER = """
mutation Register($email: String!, $password: String!) {
  registerUser(email: $email, password: $password) { ok message }
}
"""

LOGIN = """
mutation Login($email: String!, $password: String!) {
  loginUser(email: $email, password: $password) {
    ok accessToken user { id email }
  }
}
"""

ME = "query { me { id email } }"


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_register_login_me_flow(client):
    data = graphql(client, REGISTER, email="a@b.com", password="pw12345")
    assert data["data"]["registerUser"]["ok"] is True

    data = graphql(client, LOGIN, email="a@b.com", password="pw12345")
    login = data["data"]["loginUser"]
    assert login["ok"] is True and login["accessToken"]

    data = graphql(client, ME, token=login["accessToken"])
    assert data["data"]["me"]["email"] == "a@b.com"


def test_duplicate_email_rejected(client):
    graphql(client, REGISTER, email="a@b.com", password="pw12345")
    data = graphql(client, REGISTER, email="a@b.com", password="pw12345")
    assert "already exists" in data["errors"][0]["message"]


def test_wrong_password_rejected(client):
    graphql(client, REGISTER, email="a@b.com", password="pw12345")
    data = graphql(client, LOGIN, email="a@b.com", password="nope")
    assert "Invalid login credentials" in data["errors"][0]["message"]


def test_me_requires_auth(client):
    data = graphql(client, ME)
    assert data.get("errors")
