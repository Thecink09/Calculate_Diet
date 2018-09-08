
class FoodException(Exception):
    def __init__(self, message):
        self.message = message


class NameAlreadyExistsException(FoodException):
    pass


class NameNotFoundException(FoodException):
    pass


class IdNotFoundException(FoodException):
    pass


class InvalidFoodAmount(FoodException):
    pass
