from graphene import AbstractType

from .LoginUser import LoginUser
from .RegisterUser import RegisterUser


class UserMutation(AbstractType):
    login_user = LoginUser.Field()
    register_user = RegisterUser.Field()
