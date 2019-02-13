from graphene import ObjectType

from .Me import Me


class UserQuery(Me, ObjectType):
    pass
