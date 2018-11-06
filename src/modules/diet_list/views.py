from flask import Blueprint, request, session, render_template
from werkzeug.exceptions import HTTPException

from src.modules.food.food import Food
from src.modules.diet_list.diet_list import DietList
from src.modules.result.result import Result
from src import decorators
from src.common.utils import Utils
from src.exceptions import food_exceptions
from src.modules.user.user import User

list_blueprint = Blueprint("list", __name__)

list_blueprint.current_list = []
list_blueprint.result = Result()


@list_blueprint.route("add_to_list", methods=["POST"])
@decorators.requires_login
def add_to_list():
    try:
        food = Food.get_by_name(request.form['name'])
        gram = request.form['gram']
        if Utils.valid_amount(gram):
            food.gram = gram
            food.calculate_amount_value()
            list_blueprint.current_list.append(food)
            list_blueprint.result.add_to_result(food=food)
    except food_exceptions.NameNotFoundException:
        return render_template("user/profile.html", email=session['email'], ex="שם לא נמצא במאגר.",
                               current_food=None, all_food=Food.get_foods(), current_list=list_blueprint.current_list,
                               result=list_blueprint.result)
    except HTTPException:
        return render_template("user/profile.html", email=session['email'], ex="אנא בחר מוצר מתוך הטבלה.",
                               current_food=None, all_food=Food.get_foods(), current_list=list_blueprint.current_list,
                               result=list_blueprint.result)
    except food_exceptions.InvalidFoodAmount:
        return render_template("user/profile.html", email=session['email'], ex="אנא הוסף כמות.",
                               current_food=None, all_food=Food.get_foods(), current_list=list_blueprint.current_list,
                               result=list_blueprint.result)
    return render_template("user/profile.html", email=session['email'],
                           current_food=None, all_food=Food.get_foods(), current_list=list_blueprint.current_list,
                           result=list_blueprint.result)


@list_blueprint.route("my_lists")
@decorators.requires_login
def my_lists():
    user = User.get_by_email(session['email'])
    return render_template("list/my_lists.html", user_lists=DietList.get_user_lists(user._id))


@list_blueprint.route("get_list/<string:list_id>")
@decorators.requires_login
def get_list(list_id):
    user_list = DietList.get_list(list_id)
    return render_template("list/get_list.html", user_list=user_list)


@list_blueprint.route("save", methods=["POST"])
@decorators.requires_login
def save():
    user = User.get_by_email(session['email'])
    title = request.form['title']
    diet_list = DietList(user_id=user._id,
                         list_of_food=list_blueprint.current_list,
                         title=title)
    diet_list.save_to_mongo()
    list_blueprint.current_list = []
    list_blueprint.result = Result()
    return render_template("user/profile.html", all_food=Food.get_foods(), email=session['email'])


@list_blueprint.route("edit_list/<string:list_id>")
@decorators.requires_login
def edit_list(list_id):
    # give the user a page with the list items
    user_list = DietList.get_list(list_id=list_id)
    return render_template("list/edit_list.html", user_list=user_list)


@list_blueprint.route("add_to_my_list/<string:list_id>", methods=["POST", "GET"])
@decorators.requires_login
def add_to_my_list(list_id=None):
    if request.method == "POST":
        try:
            food = Food.get_food(request.form["id"])
            food.gram = int(request.form["gram"])
            DietList.add_to_list(list_id=list_id,
                                 food=food)
            user = User.get_by_email(session['email'])
        except food_exceptions.InvalidFoodAmount:
            return render_template("list/add_to_list.html", user_list=DietList.get_list(list_id),
                                   all_food=Food.get_foods(), ex="הכנס כמות אל התיבה.")
        return render_template("list/my_lists.html", user_lists=DietList.get_user_lists(user._id))
    return render_template("list/add_to_list.html", user_list=DietList.get_list(list_id),
                           all_food=Food.get_foods())


@list_blueprint.route("remove_from_list", methods=["POST"])
@decorators.requires_login
def remove_from_list():
    food = Food.get_food(request.form['id'])
    food.gram = int(request.form['gram'])
    DietList.remove_food_from_list(request.form['list_id'], food)
    user_list = DietList.get_list(request.form['list_id'])
    if user_list.list_of_food.__len__() == 0:
        DietList.remove_list(user_list._id)
        user = User.get_by_email(session['email'])
        return render_template("list/my_lists.html", user_lists=DietList.get_user_lists(user._id))
    return render_template("list/edit_list.html", user_list=user_list, list_of_food=user_list.list_of_food)


@list_blueprint.route("remove_list/<string:list_id>")
@decorators.requires_login
def remove_list(list_id=None):
    user = User.get_by_email(session['email'])
    user_lists = DietList.get_user_lists(user._id)
    if list_id in [each_list._id for each_list in user_lists]:
        DietList.remove_list(list_id)
    return render_template("list/my_lists.html", user_lists=DietList.get_user_lists(user._id))


@list_blueprint.route("clean_all")
@decorators.requires_login
def clean_all():
    list_blueprint.result = Result()
    list_blueprint.current_list = []
    return render_template("user/profile.html", all_food=Food.get_foods(), email=session['email'])
