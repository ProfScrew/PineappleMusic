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
    form.genre.choices = Genre.list
    
    #albums managment
    list_albums = Album.get_albums(current_user.username)
    list_albums_names = Album.get_albums_name(current_user.username,list_albums)
    form.album.choices = list_albums_names
    
    if form.validate_on_submit():
        flash("Valid :/")
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
                        if form.album.data == '':
                            #no album
                            if Artist.insert_song(form.name.data, None, form.cover.data, form.release_date.data.split("/")[5],
                                            form.content.data.split("/")[5],current_user.username,form.genre.data,form.premium.data):
                                flash("Upload Succesfull")
                            else:
                                flash("Upload Failed")
                        else:
                            #album
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
    return render_template('song.html', form = form, user = current_user,user_type=User.get_type_user(current_user.username))


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
                           user_type=User.get_type_user(current_user.username),
                           delete_album=delete_album,modify_album=modify_album,album=Album.get_albums(current_user.username))



@artist.route('/modifyalbum', methods=['GET','POST'])
@login_required
def modifyalbum():
    modify_album=ModifyAlbum()
    album_form =AlbumForm()
    if modify_album.validate_on_submit():
        flash(modify_album.idalbum.data)
        flash("Album Modify.")
        #delete
    return render_template('song.html', form = album_form, user = current_user,user_type=User.get_type_user(current_user.username))

@artist.route('/deletealbum', methods=['GET','POST'])
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