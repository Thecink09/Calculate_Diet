import uuid

from src.common.database import Database


class DietList(object):
    def __init__(self, user_id, list_of_food, description, _id=None):
        self.user_id = user_id
        self.list_of_food = list_of_food
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
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
    def get_user_lists(cls, user_id):
        data = Database.find('list', {'user_id': user_id})
        if data is not None:
            return [cls(**eachList) for eachList in data]

    def json(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "list_of_food": DietList.json_list([eachFood for eachFood in self.list_of_food]),
            "description": self.description
        }
