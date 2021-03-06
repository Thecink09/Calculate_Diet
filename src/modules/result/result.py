from src.modules.food.food import Food


class Result(object):
    def __init__(self, cal=None, pro=None, fat=None, carbs=None):
        self.cal = 0 if cal is None else cal
        self.pro = 0 if pro is None else pro
        self.fat = 0 if fat is None else fat
        self.carbs = 0 if carbs is None else carbs

    def add_to_result(self, food):
        self.cal += float(food.cal)
        self.pro += float(food.pro)
        self.fat += float(food.fat)
        self.carbs += float(food.carbs)

    def reduce_from_result(self, food):
        self.cal -= float(food.cal)
        self.pro -= float(food.pro)
        self.fat -= float(food.fat)
        self.carbs -= float(food.carbs)

    def zero(self):
        self.cal = 0
        self.pro = 0
        self.fat = 0
        self.carbs = 0

    @classmethod
    def get_result(cls, list_of_food):
        result = Result()
        for food in list_of_food:
            result.add_to_result(food=food)
        return result

    def json(self):
        return {
            "cal": self.cal,
            "pro": self.pro,
            "fat": self.fat,
            "carbs": self.carbs
        }