from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required,login_user,logout_user,current_user

from Codice.auth.routes import auth

# Blueprint Configuration
user = Blueprint('user', __name__,static_folder='static',template_folder='templates')

@user.route('/home', methods=['GET'])
#@login_required
def home():
    return render_template("home.html",title="Home",user=current_user)

@user.route('/profile', methods=['GET'])
#@login_required
def profile():
    return render_template("profile.html",title="Home",user=current_user)