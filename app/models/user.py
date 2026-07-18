from __future__ import annotations

from datetime import datetime, timedelta, timezone

from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    last_logged_in: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __init__(self, email: str, password: str, **kwargs):
        super().__init__(email=email, password=generate_password_hash(password), **kwargs)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def mark_logged_in(self) -> None:
        self.last_logged_in = datetime.now(timezone.utc)
        self.save()

    def generate_access_token(self) -> str:
        return create_access_token(identity=str(self.id), expires_delta=timedelta(hours=1))

    def generate_refresh_token(self) -> str:
        return create_refresh_token(identity=str(self.id))
