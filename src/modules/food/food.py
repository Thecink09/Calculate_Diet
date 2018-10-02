import uuid
import re
import requests
from bs4 import BeautifulSoup
from src.common.database import Database
import src.exceptions.food_exceptions as food_exception


class Food(object):
    def __init__(self, name, user_id, url, cal=None, fat=None, pro=None, carbs=None, gram=None, _id=None):
        self.name = name
        self.user_id = user_id
        self.url = url
        self.cal = 0 if cal is None else cal
        self.fat = 0 if fat is None else fat
        self.pro = 0 if pro is None else pro
        self.carbs = 0 if carbs is None else carbs
        self.gram = 0 if gram is None else gram
        self._id = uuid.uuid4().hex if _id is None else _id

    def load_values(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        elements = soup.find_all("a", {"class": "linkHomepageMedium"})
        values_name = [eachElement.text.strip() for eachElement in elements]
        del values_name[0:5]
        elements = soup.find_all("td", {'id': re.compile('^currentValue')})
        amount = [float(eachElement.text.strip()) for eachElement in elements]
        for i in range(values_name.__len__()):
            current_value = values_name[i]
            if current_value == "קלוריות":
                self.cal = amount[i]
            if current_value == "חלבונים":
                self.pro = amount[i]
            if current_value == "פחמימות":
                self.carbs = amount[i]
            if current_value == "שומנים":
                self.fat = amount[i]

    def calculate_amount_value(self):
        gram = int(self.gram)
        self.cal = self.cal*gram/100
        self.pro = self.pro*gram/100
        self.fat = self.fat*gram/100
        self.carbs = self.carbs*gram/100

    @classmethod
    def get_foods(cls):
        data = Database.find('food', {})
        return [cls(**food) for food in data]

    @classmethod
    def get_food(cls, _id):
        data = Database.find_one('food', {"_id": _id})
        if data is None:
            raise food_exception.IdNotFoundException("Couldnt find this id in the system.")
        return cls(**data)

    @classmethod
    def get_by_name(cls, name):
        data = Database.find_one("food", {'name': name})
        if data is None:
            raise food_exception.NameNotFoundException("Couldnt find this name in the system.")
        return cls(**data)

    @staticmethod
    def check_name(name):
        if Database.find_one("food", {'name': name}) is not None:
            raise food_exception.NameAlreadyExistsException("The name already exists.")

    def update(self):
        Database.update(collection='food',
                        query={'_id': self._id},
                        data=self.json())

    def save_to_mongo(self):
        Food.check_name(self.name)
        self.load_values()
        Database.insert(collection='food',
                        query=self.json())

    @staticmethod
    def remove(_id):
        Database.remove('food', {'_id': _id})

    def json(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "name": self.name,
            "url": self.url,
            "cal": self.cal,
            "fat": self.fat,
            "pro": self.pro,
            "carbs": self.carbs,
            "gram": self.gram
        }

    # O <-
