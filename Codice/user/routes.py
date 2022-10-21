from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user

from Codice.database import *
from Codice.user.forms import CrediCardForm, ModifyProfileForm, TableChoice
from Codice.music.forms import GetSongsGenres
from Codice.models import *

# Blueprint Configuration
user = Blueprint('user', __name__, static_folder='static',
                 template_folder='templates')


@user.route('/home', methods=['GET'])
@login_required
def home():
    likes = Song.get_top_like_songs(current_user.type_session)
    views = Song.get_top_view_songs(current_user.type_session)
    suggestion = Song.get_suggestion_songs(current_user.username, current_user.type_session)
    print("SUGGESTION: ", suggestion)
    if suggestion == None:
        suggestion = views
    form_redirect = TableChoice()    
    form_genre=GetSongsGenres()
    genres=Genre.get_genres()
    
    return render_template("home.html", title="Home", form_genre=form_genre,user=current_user,genres=genres, songview = views, songlike = likes, songsuggestion = suggestion, form_redirect = form_redirect)


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
        if User.update_user(current_user.type_session,
                            current_user.username, form.name.data,
                            form.surname.data, form.birthdate.data,
                            form.password.data, form.phone.data, form.email.data,
                            check_password):
            flash('Update Successful')
            return redirect(url_for('user.profile'))
        else:
            flash('Update Failed')
    return render_template("profile.html", title="Profile", user=current_user, form=form)


@user.route('/delete', methods=['POST'])
@login_required
def delete():
    User.delete_user(current_user.username)
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
    return render_template("premium.html", title="Premium Account", user=current_user, form=form)
