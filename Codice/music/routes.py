from flask import Blueprint, render_template, flash,redirect,url_for,request
from flask_login import  login_required,current_user

import json

from Codice.models import *
from Codice.database import *
from .forms import DeletePlaylist, DeleteSongFromPlaylist, PlaylistForm,AddToPlaylist,GetSongsPlaylist,GetSongsGenres


# Blueprint Configuration
music = Blueprint('music', __name__, static_folder='static',
                 template_folder='templates')

@music.route('/views', methods=['GET','POST'])
def views():
    var=request.data
    data = json.loads(var)
    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAa", var)
    #if data["upvote"] == "up":
    #    print("AAAAAAAAAAAAAAAAAAAAAAAA")
    
    if data["view"] == "true":
        Statistic.increase_views(int(data["idsong"]),current_user.type_session)
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAA")  
    elif "upvote" in data:
        if data["upvote"] == "up":
            like = True
            Record.delete(current_user.username, int(data["idsong"]),current_user.type_session)
            Record.insert(current_user.username, int(data["idsong"]), like,current_user.type_session)  
        elif data["downvote"] == "down":
            like = False
            Record.delete(current_user.username, int(data["idsong"]), current_user.type_session)
            Record.insert(current_user.username, int(data["idsong"]), like, current_user.type_session)  
        elif data["upvote"] == "null" and data["downvote"] == "null":
            Record.delete(current_user.username, int(data["idsong"]), current_user.type_session)
        
    return "ok"


@login_required
@music.route('/search', methods=['GET','POST'])
def search():
    form=AddToPlaylist()
    session=User.get_type_user_session(current_user.username)
    
    song=Song.get_songs(current_user.username,current_user.type_session)

    playlist = Playlist.get_playlist_user(session,current_user.username)
    form.playlist.choices=Playlist.get_playlist_name_id(session,playlist)
    
    if form.validate_on_submit():
        for idl in form.playlist.data:
            Contains.create(form.songid.data, idl)
    
    return render_template("songs.html",user=current_user,page_name="Search Songs",add_to_playlist=True,
                           listsong=song,playlist=playlist,form=form)

@login_required
@music.route('/playlist', methods=['GET','POST'])
def playlist():
    form=PlaylistForm()
    playlistform=GetSongsPlaylist()
    deleteplaylist=DeletePlaylist()
    session=current_user.type_session
    if form.validate_on_submit():
        if Playlist.create(session,form.name.data,current_user.username):
            flash("Succesful Creation")
        else:
            flash("Creation Failed")
    
    if deleteplaylist.validate_on_submit():
        Playlist.delete_playlist(deleteplaylist.playlistid.data)
            
    return render_template("playlist.html",user=current_user, form=form,
                           playlistform=playlistform,delete_playlist=deleteplaylist,
                           playlist=Playlist.get_playlist_user(session,current_user.username))

@login_required
@music.route('/getsongfromplaylist', methods=['POST'])
def getsongfromplaylist():
    form=GetSongsPlaylist()
    delete_form=DeleteSongFromPlaylist()
    if form.validate_on_submit():
        if delete_form.validate_on_submit():
            Contains.delete_song_from_playlist(delete_form.idsong.data,delete_form.playlistid.data)

        song=Song.get_song_playlist(current_user.username,form.playlistid.data)
        return render_template("songs.html",user=current_user,page_name="Playlist",
                listsong=song,delete_from_playlist=True,delete_form=delete_form,playlistid=form.playlistid.data)

@login_required
@music.route('/getsongfromplaylist', methods=['GET'])
def getsongfromplaylist_redirect():
    return redirect(url_for('music.playlist'))

@login_required
@music.route('/getsongfromgenre', methods=['POST'])
def getsongfromgenre():
    form=AddToPlaylist()
    genre_form=GetSongsGenres()
    session=User.get_type_user_session(current_user.username)

    if genre_form.validate_on_submit():
        song = Song.get_songs(current_user.username,current_user.type_session, genre_form.genre.data)

        playlist = Playlist.get_playlist_user(session,current_user.username)
        form.playlist.choices=Playlist.get_playlist_name_id(session,playlist)
        
        if form.validate_on_submit():
            for idl in form.playlist.data:
                Contains.create(form.songid.data, idl)
        
        return render_template("songs.html",user=current_user,page_name="Search Songs",add_to_playlist=True,
                            listsong=song,playlist=playlist,form=form)

@login_required
@music.route('/getsongfromgenre', methods=['GET'])
def getsongfromgenre_redirect():
    return redirect(url_for('user.home'))