from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user

from Codice.models import *
from Codice.database import *
from .forms import PlaylistForm,AddToPlaylist,GetSongsPlaylist


# Blueprint Configuration
music = Blueprint('music', __name__, static_folder='static',
                 template_folder='templates')

@login_required
@music.route('/search', methods=['GET','POST'])
def search():
    form=AddToPlaylist()
    session=User.get_type_user_session(current_user.username)
    
    playlist = Playlist.get_playlist_user(session,current_user.username)
    form.playlist.choices=Playlist.get_playlist_name_id(session,playlist)
    print(Playlist.get_playlist_name_id(session,playlist))
    if form.validate_on_submit():
        for idl in form.playlist.data:
            Contains.create(form.songid.data, idl)
            print("AAAAAAAAAAAAAAAAAAAA ",form.songid.data, idl)
    
    return render_template("songs.html",user=current_user,page_name="Search Songs",add_to_playlist=True,user_type=User.get_type_user(current_user.username),
                           listsong=Song.get_songs(),form=form)

@login_required
@music.route('/playlist', methods=['GET','POST'])
def playlist():
    form=PlaylistForm()
    playlistform=GetSongsPlaylist()
    session=User.get_type_user_session(current_user.username)
    if form.validate_on_submit():
        if Playlist.create(session,form.name.data,current_user.username):
            flash("Succesful Creation")
        else:
            flash("Creation Failed")
            
    return render_template("playlist.html",user=current_user, form=form,playlistform=playlistform,user_type=User.get_type_user(current_user.username),playlist=Playlist.get_playlist_user(session,current_user.username))

@login_required
@music.route('/getsongfromplaylist', methods=['POST'])
def getsongfromplaylist():
    form=GetSongsPlaylist()
    if form.validate_on_submit():
        song=Song.get_song_playlist(form.playlistid.data)
        return render_template("songs.html",user=current_user,page_name="Playlist "+form.name.data,add_to_playlist=False,user_type=User.get_type_user(current_user.username),
                           listsong=song)
