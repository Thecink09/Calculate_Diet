from flask import Blueprint, request, render_template, session

import src.exceptions.user_exceptions as user_exceptions
from src.config import ADMINS
from src.modules.diet_list.views import list_blueprint
from src.modules.food.food import Food
from src.modules.result.result import Result
from src import decorators
from src.modules.user.user import User

user_blueprint = Blueprint("user", __name__)
user_blueprint.user_food = []


@user_blueprint.route("/profile")
@decorators.requires_login
def profile():
    return render_template("user/profile.html", email=session['email'], all_food=user_blueprint.user_food,
                           result=list_blueprint.result, current_list=list_blueprint.current_list)


@user_blueprint.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            if User.login_valid(email=email,
                                password=password):
                User.login(email)
                if email.lower() in ADMINS:
                    user_blueprint.user_food = Food.get_foods()
                else:
                    admin = User.get_by_email("thecink09@gmail.com")
                    user = User.get_by_email(email)
                    user_blueprint.user_food = Food.get_by_user_id(admin._id) + Food.get_by_user_id(user._id)
                return render_template("user/profile.html", email=email, all_food=user_blueprint.user_food)
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
            User.register(email=email,
                          password=password)
            admin = User.get_by_email("thecink09@gmail.com")
            user_blueprint.user_food = Food.get_by_user_id(admin._id)
            return render_template("user/profile.html",  email=email, all_food=user_blueprint.user_food)
        except user_exceptions.EmailAlreadyExistsException:
            return render_template("user/register.html", ex="אימייל קיים במערכת. האם אתה מנסה להתחבר למשתמש קיים?")
        except user_exceptions.EmailPatternInvalidException:
            return render_template("user/register.html", ex="כתובת אימייל אינה תקינה.")
    return render_template("user/register.html")


@user_blueprint.route("/logout")
def logout():
    User.logout()
    user_blueprint.user_food = []
    list_blueprint.current_list = []
    list_blueprint.result = Result()
    return render_template("home.html")
