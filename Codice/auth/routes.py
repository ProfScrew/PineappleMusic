from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask import current_app as app
from flask_login import login_required
from flask_login import login_user,logout_user


from Codice import *


from Codice.models import User

from .forms import LoginForm


# Blueprint Configuration
auth = Blueprint('auth', __name__,static_folder='static',template_folder='templates')


@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = Session_guestmanager.query(User).filter(User.username==form.username.data).first()
        if user is not None and User.verify_password(form.password.data):
            login_user(user, True)
            return redirect(url_for('home.test'))
        flash('Invalid username or password.')
    return render_template("signin.html",title="Login", form=form)


#JackSparrow

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template("signup.html",title="Register")

@auth.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.signin'))

