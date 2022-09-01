from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user

from Codice.models import *
from Codice.database import *
from .forms import PlaylistForm,AddToPlaylist


# Blueprint Configuration
music = Blueprint('music', __name__, static_folder='static',
                 template_folder='templates')

@login_required
@music.route('/search', methods=['GET','POST'])
def search():
    form=AddToPlaylist()
    session=User.get_type_user_session(current_user.username)
    
    playlist = Playlist.get_playlist_user(session,current_user.username)
    form.playlist.choices= Playlist.get_playlist_name(session,playlist)
    
    if form.validate_on_submit():
        print("AAAAAAAAAAAAAAAAAAAA ",form.songname.data, form.playlist.data)
    
    return render_template("songs.html",user=current_user,page_name="Search Songs",add_to_playlist=True,user_type=User.get_type_user(current_user.username),
                           listsong=Song.get_songs(),form=form)

@login_required
@music.route('/playlist', methods=['GET','POST'])
def playlist():
    form=PlaylistForm()
    session=User.get_type_user_session(current_user.username)
    if form.validate_on_submit():
        if Playlist.create(session,form.name.data,current_user.username):
            flash("Succesful Creation")
        else:
            flash("Creation Failed")
            
    return render_template("playlist.html",user=current_user, form=form,user_type=User.get_type_user(current_user.username),playlist=Playlist.get_playlist_user(session,current_user.username))


