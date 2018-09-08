from flask import Blueprint, render_template, session, request

from diet_list.views import list_blueprint
from food.food import Food
from src import decorators
from src.exceptions import food_exceptions
from user.user import User

food_blueprint = Blueprint("food", __name__)


@food_blueprint.route("/select_food/<string:food_id>")
@decorators.requires_login
def select_food(food_id):
    try:
        all_food = Food.get_foods()
        current_food = Food.get_food(food_id)
    except food_exceptions.IdNotFoundException:
        return render_template("user/profile.html", email=session['email'],
                               current_food=None, all_food=all_food, ex="לא נמצא.",
                               result=list_blueprint.result)
    return render_template("user/profile.html", email=session['email'], current_food=current_food,
                           all_food=all_food, current_list=list_blueprint.current_list,
                           result=list_blueprint.result)


@food_blueprint.route("/add_food", methods=["POST", "GET"])
@decorators.requires_login
def add_food():
    if request.method == "POST":
        user = User.get_by_email(session['email'])
        all_food = Food.get_foods()
        try:
            food = Food(name=request.form['name'],
                        user_id=user._id,
                        url=request.form['url'])
            food.save_to_mongo()
        except food_exceptions.NameAlreadyExistsException:
            return render_template("add_food.html", ex="שם זה קיים כבר, הכנס שם אחר.")
        return render_template("user/profile.html", all_food=all_food)
    return render_template("food/add_food.html")

