import re
from passlib.hash import pbkdf2_sha512
from src.modules.food.food import Food
from src.exceptions.food_exceptions import InvalidFoodAmount


class Utils:
    @staticmethod
    def valid_email(email):
        email_valid_check = re.compile("^[\w-]+@([\w-]+\.)+[\w]+$")
        return True if email_valid_check.match(email) else False

    @staticmethod
    def valid_amount(gram):
        if gram == "" or gram == "0":
            raise InvalidFoodAmount("Food amount cannot be lower than 1.")
        return True

    @staticmethod
    def check_hashed_password(password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)
