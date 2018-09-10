import uuid

from food.food import Food
from src.common.database import Database
from src.common.utils import Utils


class DietList(object):
    def __init__(self, user_id: object, list_of_food: object, title: object, description: object = None, _id: object = None) -> object:
        self.user_id = user_id
        self.list_of_food = list_of_food
        self.title = title
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
                "gram": float(each_food.gram)
            })
        return json_list

    @classmethod
    def get_list(cls, list_id):
        return DietList.render_list(data=Database.find_one('list', {'_id': list_id}))

    @classmethod
    def render_list(cls, data):
        list = cls(**data)
        list_of_food = []
        for each_food in list.list_of_food:
            food = Food.get_food(each_food['_id'])
            food.gram = each_food['gram']
            list_of_food.append(food)
        list.list_of_food = list_of_food
        return list

    @classmethod
    def get_user_lists(cls, user_id):
        data = Database.find('list', {'user_id': user_id})
        if data is not None:
            return [DietList.render_list(data=eachList) for eachList in data]

    @staticmethod
    def remove_food_from_list(list_id, food):
        # this will send the database an update method
        # with the new list in it
        diet_list = DietList.get_list(list_id)
        list_of_food = diet_list.list_of_food
        for i in range(list_of_food.__len__()):
            if list_of_food[i]._id == food._id and list_of_food[i].gram == food.gram:
                list_of_food.remove(list_of_food[i])
                break
        diet_list.list_of_food = list_of_food
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
            "description": self.description
        }
