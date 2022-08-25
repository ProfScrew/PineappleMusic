from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user

from Codice.models import *
from Codice.database import *


# Blueprint Configuration
music = Blueprint('music', __name__, static_folder='static',
                 template_folder='templates')


@music.route('/songs', methods=['GET'])
def songs():
    return render_template("songs.html",user=current_user,user_type=User.get_type_user(current_user.username))

@music.route('/playlist', methods=['GET'])
def playlist():
    return render_template("playlist.html",user=current_user, user_type=User.get_type_user(current_user.username))