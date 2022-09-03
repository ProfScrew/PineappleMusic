from flask import Blueprint, render_template, flash
from flask_login import  login_required,current_user

from Codice.models import *
from Codice.database import *
from .forms import DeletePlaylist, DeleteSongFromPlaylist, PlaylistForm,AddToPlaylist,GetSongsPlaylist


# Blueprint Configuration
music = Blueprint('music', __name__, static_folder='static',
                 template_folder='templates')

@login_required
@music.route('/search', methods=['GET','POST'])
def search():
    form=AddToPlaylist()
    session=User.get_type_user_session(current_user.username)
    type=User.get_type_user(current_user.username)
    if type==1:
        song=NormalSong.get_songs()
    else:
        song=Song.get_songs()

    playlist = Playlist.get_playlist_user(session,current_user.username)
    form.playlist.choices=Playlist.get_playlist_name_id(session,playlist)
    
    if form.validate_on_submit():
        for idl in form.playlist.data:
            Contains.create(form.songid.data, idl)
    
    return render_template("songs.html",user=current_user,page_name="Search Songs",add_to_playlist=True,user_type=User.get_type_user(current_user.username),
                           listsong=song,form=form)

@login_required
@music.route('/playlist', methods=['GET','POST'])
def playlist():
    form=PlaylistForm()
    playlistform=GetSongsPlaylist()
    deleteplaylist=DeletePlaylist()
    session=User.get_type_user_session(current_user.username)
    if form.validate_on_submit():
        if Playlist.create(session,form.name.data,current_user.username):
            flash("Succesful Creation")
        else:
            flash("Creation Failed")
    
    if deleteplaylist.validate_on_submit():
        Playlist.delete_playlist(deleteplaylist.playlistid.data)
            
    return render_template("playlist.html",user=current_user, form=form,playlistform=playlistform,delete_playlist=deleteplaylist,user_type=User.get_type_user(current_user.username),playlist=Playlist.get_playlist_user(session,current_user.username))

@login_required
@music.route('/getsongfromplaylist', methods=['POST'])
def getsongfromplaylist():
    form=GetSongsPlaylist()
    delete_form=DeleteSongFromPlaylist()
    if form.validate_on_submit():
        if delete_form.validate_on_submit():
            Contains.delete_song_from_playlist(delete_form.idsong.data,delete_form.playlistid.data)

        song=Song.get_song_playlist(form.playlistid.data)
        return render_template("songs.html",user=current_user,page_name="Playlist",user_type=User.get_type_user(current_user.username),
                listsong=song,delete_from_playlist=True,delete_form=delete_form,playlistid=form.playlistid.data)
