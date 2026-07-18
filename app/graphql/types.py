from __future__ import annotations

from datetime import datetime

import strawberry

from app.models import User


@strawberry.type
class UserType:
    """A registered user. The password hash is intentionally not exposed."""

    id: int
    email: str
    is_active: bool
    is_verified: bool
    last_logged_in: datetime | None
    created_at: datetime

    @classmethod
    def from_model(cls, user: User) -> "UserType":
        return cls(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            last_logged_in=user.last_logged_in,
            created_at=user.created_at,
        )


@strawberry.type
class AuthPayload:
    ok: bool
    message: str
    access_token: str | None = None
    refresh_token: str | None = None
    user: UserType | None = None


@strawberry.type
class RegisterPayload:
    ok: bool
    message: str
