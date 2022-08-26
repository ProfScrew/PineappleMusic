from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from Codice.models import *
from Codice.database import *


# Blueprint Configuration
artist = Blueprint('artist', __name__, static_folder='static',
                 template_folder='templates')


@artist.route('/statistcs', methods=['GET'])
def statistics():
    return "ciao"



@artist.route('/insertsong', methods=['GET','POST'])
def insertsong():
    return render_template('insertsong.html')