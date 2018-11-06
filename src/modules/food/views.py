from flask import Blueprint, render_template, session, request

from src.config import ADMINS
from src.modules.diet_list.views import list_blueprint
from src.modules.food.food import Food
from src import decorators
from src.exceptions import food_exceptions
from src.modules.user.user import User
from src.modules.user.views import user_blueprint

food_blueprint = Blueprint("food", __name__)


@food_blueprint.route("/select_food/<string:food_id>")
@decorators.requires_login
def select_food(food_id):
    try:
        current_food = Food.get_food(food_id)
    except food_exceptions.IdNotFoundException:
        return render_template("user/profile.html", email=session['email'],
                               current_food=None, all_food=Food.get_foods(), ex="לא נמצא.",
                               result=list_blueprint.result)
    return render_template("user/profile.html", email=session['email'], current_food=current_food,
                           all_food=user_blueprint.user_food, current_list=list_blueprint.current_list,
                           result=list_blueprint.result)


@food_blueprint.route("/add_food", methods=["POST", "GET"])
@decorators.requires_login
def add_food():
    if request.method == "POST":
        try:
            user = User.get_by_email(email=session['email'])
            food = Food(request.form['name'], user_id=user._id)
            if not request.form['cal'] == "":
                food.cal = float(request.form['cal'])
            if not request.form['pro'] == "":
                food.pro = float(request.form['pro'])
            if not request.form['fat'] == "":
                food.fat = float(request.form['fat'])
            if not request.form['carbs'] == "":
                food.carbs = float(request.form['carbs'])
            food.save_to_mongo()
            user_blueprint.user_food.append(food)
        except food_exceptions.NameAlreadyExistsException:
            return render_template("food/add_food.html", ex="שם זה קיים כבר, הכנס שם אחר.")
        return render_template("food/add_food.html", added=food.name)
    return render_template("food/add_food.html")


@food_blueprint.route("/add_with_a_link", methods=["POST", "GET"])
@decorators.requires_login
def add_with_a_link():
    if request.method == "POST":
        user = User.get_by_email(session['email'])
        try:
            food = Food(name=request.form['name'],
                        user_id=user._id,
                        url=request.form['url'])
            food.load_values()
            food.save_to_mongo()
            user_blueprint.user_food.append(food)
        except food_exceptions.NameAlreadyExistsException:
            return render_template("food/add_with_a_link.html", ex="שם זה קיים כבר, הכנס שם אחר.")
        return render_template("food/add_with_a_link.html", added=food.name)
    return render_template("food/add_with_a_link.html")


@food_blueprint.route("/edit_food/<string:food_id>", methods=["POST", "GET"])
@decorators.requires_login
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
        return render_template("food/edit_food.html", all_food=Food.get_foods())
    elif request.method == "GET":
        try:
            return render_template("food/edit_food.html", food=Food.get_food(food_id))
        except food_exceptions.IdNotFoundException:
            if session['email'] in ADMINS:
                all_food = Food.get_foods()
            else:
                user = User.get_by_email(session['email'])
                all_food = Food.get_by_user_id(user_id=user._id)
            return render_template("food/edit_food.html", all_food=all_food)


@food_blueprint.route("/delete_food/<string:food_id>")
@decorators.requires_login
def delete_food(food_id):
    try:
        for food in user_blueprint.user_food:
            if food._id == food_id:
                user_blueprint.user_food.remove(food)
                Food.remove(food_id)
                break
    except food_exceptions.IdNotFoundException:
        return render_template("user/profile.html",
                               all_food=user_blueprint.user_food, ex="לא נמצא.")
    return render_template("food/edit_food.html", all_food=Food.get_foods())
