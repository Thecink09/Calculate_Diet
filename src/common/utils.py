import re

from src.modules.food.food import Food
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

    @staticmethod
    def get_list_description(list_of_food):
            if list_of_food.__len__() == 0:
                pass
            description = ""
            for i in range(list_of_food.__len__()):
                if i > 0:
                    description += " "
                description += "{} גרם {}".format(list_of_food[i].gram, list_of_food[i].name)
                if not i == list_of_food.__len__()-1:
                    description += ","
            return description

    @staticmethod
    def get_food_list(list_of_food):
        full_list = []
        for each_item in list_of_food:
            food = Food.get_food(each_item._id)
            food.gram = int(each_item.gram)
            full_list.append(food)
        return full_list