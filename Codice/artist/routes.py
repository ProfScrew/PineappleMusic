from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from Codice.models import *
from Codice.database import *
from Codice.artist.forms import *

# Blueprint Configuration
artist = Blueprint('artist', __name__, static_folder='static',
                 template_folder='templates')


@artist.route('/statistcs', methods=['GET'])
def statistics():
    return "ciao"



@artist.route('/insertsong', methods=['GET','POST'])
@login_required
def insertsong():
    #print(current_user)
    form = ModifyProfileForm()
    print(current_user.username)
    
    
    form2 = SongForm(current_user.username)
    
    
    form2.genre.choices = Genre.list
    #list_albums = Album.get_albums(current_user.username)
    #form2.album.choices = list_albums
    
    return render_template('insertsong.html', form = form, form2=form2, user = current_user)