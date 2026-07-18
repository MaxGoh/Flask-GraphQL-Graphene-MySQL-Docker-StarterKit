# Flask + Strawberry GraphQL + MySQL + Docker Starter Kit

A modern, AI-ready starter kit: **Flask 3**, **Strawberry GraphQL**, **SQLAlchemy 2** (typed models), **Flask-JWT-Extended**, **MySQL 8.4**, containerized with **Docker Compose** and served by **gunicorn**.

> Originally the reference repo for [this freeCodeCamp article](https://medium.freecodecamp.org/how-to-develop-a-flask-graphql-graphene-mysql-and-docker-starter-kit-4d475f24ee76) (Flask 1 + Graphene 2). Fully modernized in v2.

## Quick start

```bash
git clone https://github.com/MaxGoh/Flask-GraphQL-Graphene-MySQL-Docker-StarterKit.git
cd Flask-GraphQL-Graphene-MySQL-Docker-StarterKit
cp .env.example .env   # then edit secrets
docker compose up --build
```

- GraphiQL: http://localhost:8000/graphql
- Health check: http://localhost:8000/health

(The container listens on 5000 internally; it's published on host port 8000 because macOS AirPlay occupies 5000.)

Initialize the database schema:

```bash
docker compose exec server flask --app wsgi db init      # first time only
docker compose exec server flask --app wsgi db migrate -m "initial"
docker compose exec server flask --app wsgi db upgrade
```

## Example queries

```graphql
mutation { registerUser(email: "me@example.com", password: "s3cret!") { ok message } }
mutation { loginUser(email: "me@example.com", password: "s3cret!") { accessToken refreshToken } }
query { me { id email isVerified } }   # requires Authorization: Bearer <accessToken>
```

## Local development (no Docker)

```bash
pip install -e ".[dev]"
pytest                 # runs against in-memory SQLite
ruff check .
flask --app wsgi run --debug
```

## AI-ready

- `CLAUDE.md` documents architecture, conventions, and commands for AI coding agents.
- Fully type-hinted models (SQLAlchemy 2 `Mapped`) and schema (Strawberry) — agents and IDEs can reason about the code statically.
- Export the GraphQL SDL any time: `python -c "from app.graphql.schema import schema; print(schema)"`

## License

MIT
