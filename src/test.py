from diet_list.diet_list import DietList
from src.common.database import Database
from user.user import User

Database.initialize()

user = User.get_by_email("myemail@myemail.com")
List_Diets = DietList.get_user_lists(user._id)
food = List_Diets[0].list_of_food[0]
List_Diets[0].remove_food_from_list(List_Diets[0]._id, food=food)
for each_food in List_Diets[0].list_of_food:
    print("{} gr of {}.".format(each_food.gram, each_food.name))
