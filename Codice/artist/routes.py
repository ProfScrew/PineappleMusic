from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

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
                                    flash("Upload Succesfull")
                                else:
                                    flash("Upload Failed")
        else:
            flash("Cover or content links are invalid")  
    return render_template('insertsong.html', form = form, user = current_user,user_type=User.get_type_user(current_user.username))



