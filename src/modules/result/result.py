
class Result(object):
    def __init__(self):
        self.cal = 0
        self.pro = 0
        self.fat = 0
        self.carbs = 0

    def add_to_result(self, food, amount):
        self.cal += float(food.cal) * float(amount)/100
        self.pro += float(food.pro) * float(amount)/100
        self.fat += float(food.fat) * float(amount)/100
        self.carbs += float(food.carbs) * float(amount)/100

    def zero(self):
        self.cal = 0
        self.pro = 0
        self.fat = 0
        self.carbs = 0