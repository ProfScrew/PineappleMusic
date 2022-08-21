from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask import current_app as app
from flask_login import login_required
from flask_login import login_user,logout_user

from Codice import *

from Codice.models import User


# Blueprint Configuration
home = Blueprint('home', __name__,static_folder='static',template_folder='templates')

@home.route('/test', methods=['GET'])
@login_required
def test():
    return render_template("test.html",title="Test")
