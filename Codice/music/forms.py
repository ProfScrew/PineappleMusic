from flask_wtf import FlaskForm
from wtforms import  StringField,SubmitField,SelectMultipleField,HiddenField
from wtforms.validators import DataRequired, Length


from Codice.models import *
from Codice.database import *
from Codice.artist.forms import *

class PlaylistForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),Length(1,20)])
    submit = SubmitField("Create")

class AddToPlaylist(FlaskForm):
    playlist = SelectMultipleField("Add to playlist")
    songid = HiddenField("Song Name")
    submit = SubmitField("Add")
    
class GetSongsPlaylist(FlaskForm):
    playlistid = HiddenField("id")
    name = HiddenField("name")
    submit = SubmitField("Add")

class DeleteSongFromPlaylist(FlaskForm):
    playlistid = HiddenField("id")
    idsong = HiddenField("name")
    submit = SubmitField("Delete")

class DeletePlaylist(FlaskForm):
    playlistid = HiddenField("id")
    submit = SubmitField("Delete")

class GetSongsGenres(FlaskForm):
    genre = HiddenField("genre")
    
    