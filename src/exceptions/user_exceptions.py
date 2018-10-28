
class UserException(Exception):
    def __init__(self, message):
        self.message = message


class PasswordNotMatchedException(UserException):
    pass


class EmailAlreadyExistsException(UserException):
    pass


class WrongPasswordException(UserException):
    pass


class EmailPatternInvalidException(UserException):
    pass


class UserNotExistsException(UserException):
    pass
