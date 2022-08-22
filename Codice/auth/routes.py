from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required


from .forms import LoginForm, RegisterForm
from Codice.models import *
from Codice.database import *


# Blueprint Configuration
auth = Blueprint('auth', __name__, static_folder='static',
                 template_folder='templates')


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(Session_guestmanager, form.username.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect(url_for('user.home'))
        flash('Invalid username or password.')
    return render_template("signin.html", title="Login", form=form)

# JackSparrow

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if not (form.artist.data == ' ' or form.gender.data == ' '):
            if User.register_user(Session_guestmanager, form.username.data, form.name.data, form.surname.data,
                                  form.birthdate.data, form.password.data, form.gender.data, form.phone.data,
                                  form.email.data):
                # register if artist or listener
                if form.artist.data == 'True':
                    print("Artist")
                    if not Artist.register_artist(Session_guestmanager, form.username.data):
                        # delete user
                        User.delete_user(form.username.data)
                        flash('Registration Failed(Type User Artist), Please try again.')
                elif form.artist.data == 'False':
                    print("Listener")
                    if not NormalListener.register_normallistener(Session_guestmanager, form.username.data):
                        # delete user
                        User.delete_user(form.username.data)
                        flash('Registration Failed(Type User Listener), Please try again.')

                flash('Registration Successfull.')
                return redirect(url_for('auth.signin'))
            else:
                flash('Registraton Failed(User not registered), Please try agian.')
        else:
            flash('Field Gender or Artist not specified.')
    return render_template("signup.html", title="Register", form=form)


@auth.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.signin'))
