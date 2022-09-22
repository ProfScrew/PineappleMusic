from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from Codice.models import *
from Codice.database import *
from Codice.artist.forms import *

# Blueprint Configuration
artist = Blueprint('artist', __name__, static_folder='static',
                 template_folder='templates')


@artist.route('/statistics', methods=['GET','POST'])
def statistics():
    var=request.data
    print("TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",var)
    return "ciao"



@artist.route('/song', methods=['GET','POST'])
@login_required
def song():
    form = SongForm()
    modify_song=ModifySong()
    delete_song=DeleteSong()
    form.genre.choices = Genre.list
    
    #albums managment
    list_albums = Album.get_albums(current_user.username)
    list_albums_names = Album.get_albums_name(temp_username= current_user.username,albums= list_albums, choice = None)
    form.album.choices = list_albums_names
    songs= Song.get_songs_artist(current_user.username)
    
    if form.validate_on_submit():
        if Song.check_links(form.cover.data, form.content.data):
            if (form.cover.data == None) and (form.album.data == ''):
                flash("Insert a cover.")
            else:
                if form.genre.data == '':
                    flash("Select a genre")
                else:
                    if form.premium.data == '':
                        flash("Select Exclusivity")
                    else:
                        if form.album.data == '':#no album
                            if Artist.insert_song(form.name.data, None, form.cover.data.split("/")[5], form.release_date.data,
                                            form.content.data.split("/")[5],current_user.username,form.genre.data,form.premium.data):
                                flash("Upload Succesfull")
                            else:
                                flash("Upload Failed")
                        else:#album
                            album = Album.extract_id_album(list_albums,form.album.data)
                            cover = Album.extract_cover_album(list_albums, form.album.data)
                            if album == None or cover == None:
                                flash("Error Register Ablum")
                            else:
                                if Artist.insert_song(form.name.data, album, cover, form.release_date.data,
                                            form.content.data.split("/")[5],current_user.username,form.genre.data,form.premium.data):
                                    flash("Upload Successful")
                                else:
                                    flash("Upload Failed")
        else:
            flash("Cover or content links are invalid")
    return render_template('song.html', form = form, user = current_user,songs=songs,modify_song=modify_song,delete_song=delete_song)


@artist.route('/album', methods=['GET','POST'])
@login_required
def album():
    form = AlbumForm()
    delete_album=DeleteAlbum()
    modify_album=ModifyAlbum()
    
    print(current_user)
    
    if form.validate_on_submit():
        if Album.check_artist_album_name(form.name.data, current_user.username):
            flash("Album name already in use by you.")
        else:
            if Album.check_cover_link(form.cover.data):
                if Artist.insert_album(form.name.data,form.cover.data.split("/")[5],current_user.username):
                    flash("Upload Successful.")
                else:
                    flash("Upload Failed.")
            else:
                flash("Invalid cover link.")
                
    return render_template('album.html', form = form, user = current_user,
                           delete_album=delete_album,
                           modify_album=modify_album,
                           album=Album.get_albums(current_user.username))



@artist.route('/modifyalbum', methods=['GET'])
@login_required
def modifyalbum_redirect():
    return redirect(url_for('artist.album'))

@artist.route('/modifyalbum', methods=['POST'])
@login_required
def modifyalbum():
    modify_album=ModifyAlbum()
    album_form =ModifyAlbumForm()
    if album_form.validate_on_submit():
        if album_form.name.data == Album.get_albums_id(album_form.idalbum.data).name and album_form.cover.data == '':
            flash("No nodification made")
            return redirect(url_for('artist.album'))
        else:
            if Album.modify_album(album_form.idalbum.data,album_form.name.data,album_form.cover.data,current_user.username):
                flash("Successful modification.")
                return redirect(url_for('artist.album'))
            else:
                flash("Error Modification")  
    return render_template('modifyalbum.html', form = album_form, album = Album.get_albums_id(modify_album.idalbum.data), user = current_user)

@artist.route('/deletealbum', methods=['POST'])
@login_required
def deletealbum():
    delete_album=DeleteAlbum()
    if delete_album.validate_on_submit():
        if Album.delete_album(delete_album.idalbum.data):
            flash("Album Deleted.")
        else:
            flash("Error Deleting Album.")
        #delete
    return redirect(url_for('artist.album'))

@artist.route('/modifysong', methods=['GET','POST'])
@login_required
def modifysong():
    song = ModifySong()
    form = ModifySongForm()
    song_info = Song.get_song_id(song.idsong.data)
    
    #genre choice
    form.genre.choices = Belong.get_genre_list(song.idsong.data)
    
    #album managment
    list_albums = Album.get_albums(current_user.username)
    list_albums_names = Album.get_albums_name(current_user.username,list_albums,song_info.album)
    form.album.choices = list_albums_names
    
    if form.validate_on_submit():
        #modify song con campy giusti
        #verificare se codificato singolarmente
        album = 2
        if form.name.data == song_info.name:#name
            form.name.data = None        
        
        if form.genre.data == form.genre.choices[0]:#genre 
            form.genre.data = None
            
        if form.premium.data == '':#premium
            form.premium.data = None
        elif form.premium.data == 'The song will be premium':
            if not PremiumSong.check_song:
                form.premium.data = 1
            else:
                form.premium.data = None
        else:
            if not NormalSong.check_song:
                form.premium.data = 2
            else:
                form.premium.data = None
                
        if form.content.data == '':#content
            form.content.data = None
        
        if form.cover.data == '':#cover
            form.cover.data = None
        else:
            album = Album.check_link(form.cover.data)
        
        if form.album.data == list_albums_names[0]:#album
            form.album.data = None
        elif form.album.data == '':
            form.album.data = -1
        else:
            form.album.data = Album.extract_id_album(list_albums, form.album.data)
            album = Album.get_albums_id(form.album.data)
            form.cover.data = album.cover
            album = True
        if album == False: #checking cover,content and if ok calling update
            flash("Error Cover Link.")
        elif (not Album.check_link(form.content.data)) and (form.content.data != None) :
            flash("Error Content Link.")
        else:
            if album != True and form.cover.data != None:
                form.cover.data =form.cover.data.split("/")[5]
            if Song.modify_song(song_info.idsong,form.name.data,form.album.data,form.cover.data,
                                form.content.data,form.release_date.data,form.genre.data,form.premium.data):
                flash("Modification Successful")
                return redirect(url_for('artist.song'))
            else:
                flash("Error loading modification.")
    return render_template('modifysong.html', form = form, user = current_user, song = song_info)

@artist.route('/deletesong', methods=['POST'])
@login_required
def deletesong():
    delete_song = DeleteSong()
    if delete_song.validate_on_submit():
        if Song.delete_song(delete_song.idsong.data):
            flash("Delete successful.")
        else:
            flash("Error song delete.")
    return redirect(url_for('artist.song'))

