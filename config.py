import os


class Config:
    """Configuration loaded from environment variables (see .env.example)."""

    ENV = os.environ.get("ENV", "DEVELOPMENT")
    DEBUG = ENV != "PRODUCTION"

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
            user=os.environ.get("DB_USERNAME", "username"),
            password=os.environ.get("DB_PASSWORD", "password"),
            host=os.environ.get("DB_HOST", "127.0.0.1"),
            port=os.environ.get("DB_PORT", "3306"),
            database=os.environ.get("DB_DATABASE", "database_name"),
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
