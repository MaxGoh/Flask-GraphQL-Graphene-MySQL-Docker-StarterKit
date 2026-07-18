# Flask + Strawberry GraphQL + MySQL Starter Kit

Flask 3 / Strawberry GraphQL / SQLAlchemy 2 / MySQL 8.4 starter, containerized with Docker Compose.

## Architecture

- `wsgi.py` — entrypoint (`app` for gunicorn; `flask --app wsgi ...` for CLI)
- `config.py` — env-var-driven config (see `.env.example`)
- `app/__init__.py` — `create_app()` factory; mounts `/graphql` (GraphiQL enabled) and `/health`
- `app/extensions.py` — shared `db`, `migrate`, `jwt` instances (import from here, never from `app/__init__.py`, to avoid circular imports)
- `app/models/` — SQLAlchemy 2 typed models (`Mapped` / `mapped_column`)
- `app/graphql/` — Strawberry schema
  - `types.py` — output types (`UserType.from_model()` maps ORM → GraphQL; never expose `password`)
  - `schema.py` — `Query` (me), `Mutation` (registerUser, loginUser)

## Conventions

- Auth: Flask-JWT-Extended. JWT identity is `str(user.id)` (must be a string in v4). Resolvers auth via `verify_jwt_in_request()` — see `_current_user()` in `app/graphql/schema.py`.
- Passwords hashed with `werkzeug.security` (scrypt). Never log or return them.
- DB timestamps use `server_default=func.now()` — never `default=datetime.now()` (evaluates at import time).
- Migrations: Flask-Migrate/Alembic — `flask --app wsgi db migrate -m "msg" && flask --app wsgi db upgrade`. Do not use `db.create_all()` in production paths.

## Commands

```bash
docker compose up --build          # run the stack (needs .env; cp .env.example .env)
pip install -e ".[dev]"            # local dev install
pytest                             # tests (SQLite in-memory, no MySQL needed)
ruff check .                       # lint
python -c "from app.graphql.schema import schema; print(schema)"  # print GraphQL SDL
```

## Testing

`tests/` uses an in-memory SQLite DB via `create_app` with an overridden `SQLALCHEMY_DATABASE_URI`. Add tests for every new resolver.
