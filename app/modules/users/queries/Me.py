
from graphene import ObjectType, Field
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.User import User as UserModel
from graphql import GraphQLError


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password", )


class Me(ObjectType):
    me = Field(
        UserType,
        description=
    """
    :required: Access Token.

    :description: Returns the AdminUser Object along with 
    the respective role and role nodes information.
    """
    )

    @jwt_required
    def resolve_me(self, info):
        id = get_jwt_identity()
        user = UserModel.query.filter_by(id=id).scalar()
        if user:
            return user
        else:
            raise GraphQLError("User is not found.")
