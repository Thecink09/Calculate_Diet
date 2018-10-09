import uuid

from src.common.utils import Utils
from src.modules.food.food import Food
from src.common.database import Database
from src.modules.result.result import Result


class DietList(object):
    def __init__(self, user_id: object, list_of_food: object, title: object, result: object = None, description: object = None, _id: object = None) -> object:
        self.user_id = user_id
        self.list_of_food = list_of_food
        self.title = title
        self.result = Result.get_result(list_of_food) if result is None else result
        self.description = "" if description is None else description
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        if self.description == "":
            self.description = Utils.get_list_description(self.list_of_food)
        Database.insert(collection='list',
                        query=self.json())

    @staticmethod
    def json_list(list_of_food):
        json_list = []
        for each_food in list_of_food:
            json_list.append({
                "_id": each_food._id,
                "gram": int(each_food.gram)
            })
        return json_list

    @classmethod
    def get_list(cls, list_id):
        return DietList.render_list(data=Database.find_one('list', {'_id': list_id}))

    @classmethod
    def render_list(cls, data):
        list = cls(**data)
        list_of_food = []
        # fixing list from dict array to obj array
        for each_food in list.list_of_food:
            food = Food.get_food(each_food['_id'])
            food.gram = each_food['gram']
            list_of_food.append(food)
        list.list_of_food = list_of_food

        # fixing result from dict to obj
        result = Result(cal=list.result['cal'],
                        pro=list.result['pro'],
                        fat=list.result['fat'],
                        carbs=list.result['carbs'])
        list.result = result
        return list

    @staticmethod
    def remove_list(list_id):
        Database.remove(collection='list',
                        query={'_id': list_id})

    @classmethod
    def get_user_lists(cls, user_id):
        data = Database.find('list', {'user_id': user_id})
        if data is not None:
            return [DietList.render_list(data=eachList) for eachList in data]

    def remove_list_item(self, food):
        self.list_of_food.remove(food)
        self.result.reduce_from_result(food)
        self.update_description()

    @staticmethod
    def remove_food_from_list(list_id, food):
        diet_list = DietList.get_list(list_id)
        for item in diet_list.list_of_food:
            if item._id == food._id and int(item.gram) == int(food.gram):
                diet_list.list_of_food.remove(item)
                food.calculate_amount_value()
                diet_list.result.reduce_from_result(food)
                diet_list.update_description()
                break
        Database.update(collection='list',
                        query={'_id': diet_list._id},
                        data=diet_list.json())

    def update_description(self):
        self.description = Utils.get_list_description(self.list_of_food)

    @staticmethod
    def add_to_list(list_id, food):
        diet_list = DietList.get_list(list_id)
        diet_list.list_of_food.append(food)
        diet_list.result.add_to_result(food)
        diet_list.update_description()
        Database.update(collection='list',
                        query={'_id': list_id},
                        data=diet_list.json())

    @staticmethod
    def remove_list(list_id):
        Database.remove(collection='list', query={'_id': list_id})

    def json(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "title": self.title,
            "list_of_food": DietList.json_list([eachFood for eachFood in self.list_of_food]),
            "result": {
                'cal': self.result.cal,
                'pro': self.result.pro,
                'fat': self.result.fat,
                'carbs': self.result.carbs
            },
            "description": self.description
        }
