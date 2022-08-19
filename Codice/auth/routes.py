from flask import Blueprint, render_template
from flask import current_app as app


# Blueprint Configuration
home_a = Blueprint(
    'home', __name__,template_folder='templates',static_folder='static'
)


@home_a.route('/', methods=['GET'])
def home():
    return render_template("index.html")
