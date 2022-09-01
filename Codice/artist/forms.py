from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField,DateField,SubmitField,SelectField,EmailField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, Optional


from Codice.models import *
from Codice.database import *
from Codice.artist.forms import *



class ModifyProfileForm(FlaskForm):
    
    
    name = StringField("Name", validators=[DataRequired(),Length(max=20)])
    surname = StringField("Surname", validators=[DataRequired(),Length(max=20)])
    birthdate = DateField("Birthdate", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Optional(), Length(min=8)])
    
    phone = StringField("Phone", validators=[DataRequired(),Length(min=6,max=6)])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    
    submit = SubmitField("Update")
    

class SongForm(FlaskForm):
    
    
    
    name = StringField("Name", validators=[DataRequired(),Length(max=40)])
    cover = StringField("Cover", validators=[Optional(),Length(max=120)])
    content=StringField("Content", validators=[DataRequired(),Length(max=120)])
    genre=SelectField("Genre", validators=None)
    album = SelectField("Album", validators=None)
    
    release_date=DateField("Release Date", validators=[DataRequired()])
    premium = SelectField("Premium", choices=['','The song will be premium',
                                              'The song will be available to everyone'],
                          validate_choice=True )
    
    submit = SubmitField("Upload")
    
    