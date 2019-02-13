from graphene import ObjectType, Schema, String

from app.modules.users.queries import UserQuery
from app.modules.users.mutations import UserMutation


class RootQuery(UserQuery, ObjectType):
    pass



class RootMutation(UserMutation, ObjectType):
    pass


schema = Schema(query=RootQuery, mutation=RootMutation)
