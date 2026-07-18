from __future__ import annotations

import strawberry
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from graphql import GraphQLError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.graphql.types import AuthPayload, RegisterPayload, UserType
from app.models import User


def _current_user() -> User:
    """Resolve the authenticated user from the request's JWT, or raise."""
    verify_jwt_in_request()
    user = db.session.get(User, int(get_jwt_identity()))
    if user is None:
        raise GraphQLError("User not found.")
    return user


@strawberry.type
class Query:
    @strawberry.field(description="The currently authenticated user (requires a Bearer token).")
    def me(self) -> UserType:
        return UserType.from_model(_current_user())


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Register a new user account.")
    def register_user(self, email: str, password: str) -> RegisterPayload:
        try:
            User(email=email, password=password).save()
        except IntegrityError:
            db.session.rollback()
            raise GraphQLError("A user with this email already exists.")
        return RegisterPayload(ok=True, message="User has been created successfully.")

    @strawberry.mutation(description="Log in and receive access/refresh tokens.")
    def login_user(self, email: str, password: str) -> AuthPayload:
        user = db.session.execute(select(User).filter_by(email=email)).scalar_one_or_none()
        if user is None or not user.verify_password(password):
            raise GraphQLError("Invalid login credentials.")
        user.mark_logged_in()
        return AuthPayload(
            ok=True,
            message="User has successfully logged in.",
            access_token=user.generate_access_token(),
            refresh_token=user.generate_refresh_token(),
            user=UserType.from_model(user),
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
