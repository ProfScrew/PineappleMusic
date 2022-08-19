from flask import Blueprint, render_template
from flask import current_app as app


# Blueprint Configuration
auth = Blueprint('auth', __name__,static_folder='static',template_folder='templates')


@auth.route('/signin', methods=['GET'])
def signin():
    return render_template("signin.html",title="Login")

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template("signup.html",title="Register")

@auth.route('/signout', methods=['GET'])
def signout():
    return render_template("signout.html",title="Logout")


