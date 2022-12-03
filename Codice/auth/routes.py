from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required


from .forms import LoginForm, RegisterForm, SongForm
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
            artist_check = Artist.check_if_artist(form.username.data)
            if artist_check == 1:
                if Creates.check_artist(form.username.data):
                    login_user(user, True)
                    return redirect(url_for('user.home'))
                else:
                    flash("Song Not Found. Your Account was deleted. Register again and insert your first song.")
                    User.delete_user(form.username.data)
            elif artist_check == 0:
                flash("Artist. Login failed try again.")
            else:
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
                                  form.email.data, form.artist.data):
                flash('Registration Successfull.')
                if form.artist.data == 'True':
                    return redirect(url_for('auth.requiredsong'))
                else:
                    return redirect(url_for('auth.signin'))
            else:
                flash('Registraton Failed(Server Error), Please try agian.')
        else:
            flash('Field Gender or Artist not specified.')
    return render_template("signup.html", title="Register", form=form)

# check user and pss and if artist
# if ok
#   check links


@auth.route('/requiredsong', methods=['GET', 'POST'])
def requiredsong():
    form = SongForm()
    if form.validate_on_submit():
        if not form.premium.data == ' ':
            user = User.get_user(Session_guestmanager, form.username.data)
            if user is not None and user.verify_password(form.password.data) and (User.get_type_user(form.username.data) == 3):
                if Artist.check_links(form.cover.data,form.content.data):
                    if Artist.insert_song(form.name.data, None, form.cover.data.split("/")[5], form.release_date.data,
                                        form.content.data.split("/")[5], form.username.data, form.genre.data, form.premium.data, Session_artist):
                        flash("Succesfull Insert")
                        
                        return redirect(url_for('auth.signin'))
                    else:
                        flash("Error Insert Song.")
                else:
                    flash("Invalid Links.")
                    
                # https://drive.google.com/file/d/1XjENKcGg1SZTKWLwpwVI2qgAMvALM_fO/view?usp=sharing     cover
                # request = requests.get('https://drive.google.com/file/d/1HMKIjUQ5g_ABZVPfVGNWh0q2o10aYoK9/view?usp=sharing') # content

            else:
                flash('Error Account Info')
        else:
            flash('Song exclusivity not decided.')
    return render_template("requiredsong.html", title="Insert Required Song", form=form)


@auth.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.signin'))
