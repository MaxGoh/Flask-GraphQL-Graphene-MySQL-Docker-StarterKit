import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import Mutation, Boolean, String, Field
from app.models.User import User as UserModel
from graphql import GraphQLError


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password",)


class LoginUser(Mutation):
    ok = Boolean(description="Request status")
    message = String(description="Request message")
    access_token = String(description="User's Access Token")
    refresh_token = String(description="User's Refresh Token")
    user = Field(User)

    class Input:
        email = String(description="User's email address")
        password = String(description="User's password")

    def mutate(self, info, email, password):
        user = UserModel.query.filter_by(email=email).scalar()
        if user and user._verify_password(password):
            user.last_logged_in = datetime.datetime.now()
            try:
                user.save()
            except Exception as e:
                raise GraphQLError('Unable to update user', e)
            else:
                ok = True
                message = "User has successfully logged in"
                return LoginUser(
                    access_token=user.generate_access_token(),
                    refresh_token=user.generate_refresh_token(),
                    ok=ok,
                    message=message,
                    user=user
                )
        else:
            raise Exception('Invalid Login Credentials')
