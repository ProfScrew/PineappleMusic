from flask_wtf import FlaskForm
from wtforms import  StringField,SubmitField,SelectMultipleField,HiddenField
from flask_login import current_user
from wtforms.validators import DataRequired, Length


from Codice.models import *
from Codice.database import *
from Codice.artist.forms import *

class PlaylistForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),Length(1,20)])
    submit = SubmitField("Create")

class AddToPlaylist(FlaskForm):
    playlist = SelectMultipleField()
    songname = HiddenField("Song Name")
    submit = SubmitField("Add")
    
    