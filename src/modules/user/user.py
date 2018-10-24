import uuid
from passlib.exc import InvalidHashError
from flask import session
import src.exceptions.user_exceptions as user_exceptions
from src.common.database import Database
from src.modules.food.food import Food
from src.common.utils import Utils


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='users',
                        query=self.json())

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email=email)
        if user is None:
            raise user_exceptions.UserNotExistsException("The user not exists in the system.")
        if password == user.password:
            return True
        try:
            if not Utils.check_hashed_password(password=password, hashed_password=user.password):
                raise user_exceptions.WrongPasswordException("The password is not correct.")
        except InvalidHashError:
            raise user_exceptions.WrongPasswordException("The password is not correct.")
        return True

    @classmethod
    def get_by_email(cls, email):
        user = Database.find_one(collection='users',
                                 query={'email': email})
        if user is not None:
            return cls(**user)

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(collection='users',
                                       query={'id': _id}))

    @staticmethod
    def login(email):
        session['email'] = email

    @staticmethod
    def register(email, password):
        user = User.get_by_email(email=email)
        if user is not None:
            raise user_exceptions.EmailAlreadyExistsException("The given email address already exists in the system.")
        if not Utils.valid_email(email=email):
            raise user_exceptions.EmailPatternInvalidException("The given email doesnt stand the email conventions.")
        user = User(email=email, password=password)
        user.save_to_mongo()
        session['email'] = email

    @staticmethod
    def list_food():
        all_food = Food.get_foods()
        for each_food in all_food:
            print("Name: {}, Cal: {}, Pro: {}, Fat: {}, Carb: {}, Id: {}.".
                  format(each_food.name, each_food.cal, each_food.pro, each_food.fat
                         , each_food.carbs, each_food._id))
        id = input("Input id of the item: ")
        gram = input("Input gram amount: ")
        food = Food.get_food(id)
        food.gram = gram
        return food

    def get_foods(self):
        foods = Database.find('food', {'user_id': self._id})
        return [Food(**each_food) for each_food in foods]

    @staticmethod
    def logout():
        session['email'] = None

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": Utils.hash_password(self.password)
        }
