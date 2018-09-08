from flask import Blueprint, request, render_template, session

import src
import src.exceptions.user_exceptions as user_exceptions
from diet_list.views import list_blueprint
from food.food import Food
from src import decorators
from user.user import User

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/profile")
@decorators.requires_login
def profile():
    all_food = Food.get_foods()
    return render_template("user/profile.html", email=session['email'], all_food=all_food)


@user_blueprint.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            if User.login_valid(email=email,
                                password=password):
                User.login(email)
                all_food = Food.get_foods()
                return render_template("user/profile.html", email=email, all_food=all_food)
        except user_exceptions.WrongPasswordException:
            return render_template("user/login.html", ex="הסיסמה שגויה, נסה שנית.")
        except user_exceptions.UserNotExistsException:
            return render_template("user/login.html", ex="המשתמש אינו קיים במערכת.")
    return render_template("user/login.html")


@user_blueprint.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            if User.register(email=email,
                             password=password):
                all_food = Food.get_foods()
                return render_template("user/profile.html", email=email, all_food=all_food)
        except user_exceptions.EmailAlreadyExistsException:
            return render_template("user/register.html", ex="אימייל קיים במערכת. האם אתה מנסה להתחבר למשתמש קיים?")
        except user_exceptions.EmailPatternInvalidException:
            return render_template("user/register.html", ex="כתובת אימייל אינה תקינה.")
    return render_template("user/register.html")


@user_blueprint.route("/logout")
def logout():
    User.logout()
    list_blueprint.current_list = []
    list_blueprint.result = None
    return render_template("home.html")
