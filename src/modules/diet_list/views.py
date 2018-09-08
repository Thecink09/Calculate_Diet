from flask import Blueprint, request, session, render_template
from werkzeug.exceptions import HTTPException

from food.food import Food
from diet_list.diet_list import DietList
from result.result import Result
from src import decorators
from src.common.utils import Utils
from src.exceptions import food_exceptions
from user.user import User

list_blueprint = Blueprint("list", __name__)

list_blueprint.current_list = []
list_blueprint.result = Result()


@list_blueprint.route("add_to_list", methods=["POST"])
@decorators.requires_login
def add_to_list():
    all_food = Food.get_foods()

    try:
        name = request.form['name']
        food = Food.get_by_name(name)
        gram = request.form['gram']
        Utils.valid_amount(gram)
        food.gram = gram
        food.calculate_amount_value()
        list_blueprint.current_list.append(food)
        list_blueprint.result.add_to_result(food=food, amount=gram)
    except food_exceptions.NameNotFoundException:
        return render_template("user/profile.html", email=session['email'], ex="שם לא נמצא במאגר.",
                               current_food=None, all_food=all_food, current_list=list_blueprint.current_list,
                               result=list_blueprint.result)
    except HTTPException:
        return render_template("user/profile.html", email=session['email'], ex="אנא בחר מוצר מתוך הטבלה.",
                               current_food=None, all_food=all_food, current_list=list_blueprint.current_list,
                               result=list_blueprint.result)
    except food_exceptions.InvalidFoodAmount:
        return render_template("user/profile.html", email=session['email'], ex="אנא הוסף כמות.",
                               current_food=None, all_food=all_food, current_list=list_blueprint.current_list,
                               result=list_blueprint.result)
    return render_template("user/profile.html", email=session['email'],
                           current_food=None, all_food=all_food, current_list=list_blueprint.current_list,
                           result=list_blueprint.result)


@list_blueprint.route("my_lists")
@decorators.requires_login
def my_lists():
    user = User.get_by_email(session['email'])
    user_lists = DietList.get_user_lists(user._id)
    return render_template("list/my_lists.html", user_lists=user_lists)
