from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from Codice.auth.routes import auth
from Codice.user.forms import ModifyProfileForm
from Codice.models import *

# Blueprint Configuration
user = Blueprint('user', __name__, static_folder='static',
                 template_folder='templates')


@user.route('/home', methods=['GET'])
@login_required
def home():
    return render_template("home.html", title="Home", user=current_user)


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ModifyProfileForm()
    if form.is_submitted(): #da riveder questo metodo(un po cringe)
        check_password = True
        if form.password.data is None:
            form.password.data = "temppassword"
            check_password = False
        if form.validate_on_submit():
            print("meh")
            
            #compilare signature
            User.update_user(form.username.data)
            
                
    return render_template("profile.html", title="Profile", user=current_user, form=form)


@user.route('/delete', methods=['POST'])
@login_required
def delete():
    
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.signin'))
