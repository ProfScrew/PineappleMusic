from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField,DateField,SubmitField,SelectField,EmailField
from wtforms_sqlalchemy.fields import QuerySelectField

from wtforms.validators import DataRequired, Length, Email, Optional

from flask_login import current_user

from Codice.models import *

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
    cover = StringField("Cover", validators=[DataRequired(),Length(max=120)])
    content=StringField("Content", validators=[DataRequired(),Length(max=120)])
    release_date=DateField("Release Date", validators=[DataRequired()])
    genre=SelectField("Genre", choices=Genre.list)
    album = QuerySelectField("Album",validators=[Optional()])
    premium = SelectField("Premium", choices=[' ','The song will be premium','The song will be available to everyone'],
                          validate_choice=True )
    
    #https://drive.google.com/file/d/1HMKIjUQ5g_ABZVPfVGNWh0q2o10aYoK9/view?usp=sharing
    
    def printUser(self):
        print(current_user)
    
    def set_album(self):
        self.album = QuerySelectField("Album",validators=[Optional()],query_factory=Album.get_albums(current_user.username))
    
    submit = SubmitField("Upload")
    
    
    ################### SISTEMARE STA MERDA