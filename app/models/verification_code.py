from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

CODE_TTL = timedelta(minutes=10)


class VerificationCode(db.Model):
    __tablename__ = "verification_code"

    id: Mapped[int] = mapped_column(primary_key=True)
    verification_code: Mapped[str] = mapped_column(String(6), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    def __init__(self, user_id: int, **kwargs):
        super().__init__(
            user_id=user_id, verification_code=self.generate_verification_code(), **kwargs
        )

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def is_valid(self) -> bool:
        created = self.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) - created < CODE_TTL

    @staticmethod
    def generate_verification_code() -> str:
        """Cryptographically secure 6-digit code."""
        return f"{secrets.randbelow(1_000_000):06d}"
