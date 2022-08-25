from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user

from Codice.auth.routes import auth
from Codice.database import *
from Codice.user.forms import CrediCardForm, ModifyProfileForm
from Codice.models import *

# Blueprint Configuration
user = Blueprint('user', __name__, static_folder='static',
                 template_folder='templates')


@user.route('/home', methods=['GET'])
@login_required
def home():
    return render_template("home.html", title="Home", user=current_user, user_type=User.get_type_user(current_user.username))


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
                            form.password.data, form.phone.data, form.email.data,
                            check_password):
            flash('Update Successful')
            return redirect(url_for('user.profile'))
        else:
            flash('Update Failed')

    return render_template("profile.html", title="Profile", user=current_user, form=form, user_type=User.get_type_user(current_user.username))


@user.route('/delete', methods=['POST'])
@login_required
def delete():
    User.delete_user(Session_deletemanager, current_user.username)
    logout_user()
    flash('Your account was deleted.')
    return redirect(url_for('auth.signin'))


@user.route('/premium', methods=['GET', 'POST'])
@login_required
def premium():
    form = CrediCardForm()
    if form.validate_on_submit():
        if not form.card_number.data.isnumeric():
            flash("Card Number not valid.(Don't use letters!)")
        elif not form.cvv.data.isnumeric():
            flash("CVV not valid(Don't use letters!)")
        else:
            if User.move_user_to_premium(current_user.username):
                flash("Ugrade Succesful. YOU ROCK!")
            else:
                flash("Upgrade Failed.")
    return render_template("premium.html", title="Premium Account", user=current_user, form=form, user_type=User.get_type_user(current_user.username))
