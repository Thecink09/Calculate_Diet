from flask import Blueprint, render_template, session, request

from diet_list.views import list_blueprint
from food.food import Food
from src import decorators
from src.common.database import Database
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
@decorators.requires_admin
def add_food():
    if request.method == "POST":
        user = User.get_by_email(session['email'])
        try:
            food = Food(name=request.form['name'],
                        user_id=user._id,
                        url=request.form['url'])
            food.save_to_mongo()
        except food_exceptions.NameAlreadyExistsException:
            return render_template("add_food.html", ex="שם זה קיים כבר, הכנס שם אחר.")
        return render_template("food/add_food.html", added=food.name)
    return render_template("food/add_food.html")


@food_blueprint.route("/edit_food/<string:food_id>", methods=["POST", "GET"])
@decorators.requires_admin
def edit_food(food_id=None):
    if request.method == "POST":
        food = Food.get_food(food_id)
        if not request.form['cal'] == "":
            food.cal = float(request.form['cal'])
        if not request.form['pro'] == "":
            food.pro = float(request.form['pro'])
        if not request.form['fat'] == "":
            food.fat = float(request.form['fat'])
        if not request.form['carbs'] == "":
            food.carbs = float(request.form['carbs'])
        food.update()
        all_foods = Food.get_foods()
        return render_template("food/edit_food.html", all_food=all_foods)
    elif request.method == "GET":
        try:
            return render_template("food/edit_food.html", food=Food.get_food(food_id))
        except food_exceptions.IdNotFoundException:
            return render_template("food/edit_food.html", all_food=Food.get_foods())


@food_blueprint.route("/delete_food/<string:food_id>")
@decorators.requires_admin
def delete_food(food_id):
    Food.remove(food_id)
    return render_template("food/edit_food.html", all_food=Food.get_foods())
