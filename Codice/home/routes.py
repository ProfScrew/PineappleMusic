from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required,login_user,logout_user,current_user

from Codice.auth.routes import auth

# Blueprint Configuration
home = Blueprint('home', __name__,static_folder='static',template_folder='templates')

@home.route('/test', methods=['GET'])
#@login_required
def test():
    return render_template("test.html",title="Test")
