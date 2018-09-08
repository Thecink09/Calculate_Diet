from food.food import Food
from src.common.database import Database
from user.user import User
from result.result import Result
from src import decorators

@decorators.requires_login
def say_hello():
    print("Hi")

say_hello()

