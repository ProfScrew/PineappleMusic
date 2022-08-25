from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from Codice.auth.routes import auth
from Codice.database import *
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
    
    if form.validate_on_submit():
        if form.password.data == '':
            check_password = False
        else:
            check_password = True
            form.password.data = User.encrypt_password(form.password.data)
        if User.update_user(User.get_type_user_session(current_user.username),
                            current_user.username, form.name.data,
                            form.surname.data, form.birthdate.data,
                            form.password.data,form.phone.data,form.email.data,
                            check_password):
            flash('Update Successful')
            return redirect(url_for('user.profile'))
        else:
            flash('Update Failed')
        
        
                
    return render_template("profile.html", title="Profile", user=current_user, form=form)


@user.route('/delete', methods=['POST'])
@login_required
def delete():
    
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.signin'))
