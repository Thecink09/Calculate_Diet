from flask import Flask, render_template

from src.modules.food.views import food_blueprint
from src.modules.diet_list.views import list_blueprint
from src.common.database import Database
from src.modules.user.views import user_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "1234"
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(food_blueprint, url_prefix="/food")
app.register_blueprint(list_blueprint, url_prefix="/list")


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route("/")
def home_page():
    return render_template("home.html")

