import re

from src.exceptions.food_exceptions import InvalidFoodAmount


class Utils:
    @staticmethod
    def get_hello():
        return "Hello' world"

    @staticmethod
    def valid_email(email):
        email_valid_check = re.compile("^[\w-]+@([\w-]+\.)+[\w]+$")
        return True if email_valid_check.match(email) else False

    @staticmethod
    def valid_amount(gram):
        if gram == "" or gram == "0":
            raise InvalidFoodAmount("Food amount cannot be lower than 1.")
