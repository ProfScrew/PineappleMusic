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
    cover = StringField("Cover", validators=[DataRequired(),Length(max=120)])
    content=StringField("Content", validators=[DataRequired(),Length(max=120)])
    release_date=DateField("Release Date", validators=[DataRequired()])
    genre=SelectField("Genre")
    
    #album = QuerySelectField("Album",validators=[Optional()],query_factory=Album.get_albums('JackSparrow'))

    album = QuerySelectField("Album")
    #album = SelectField("Album", choices=Album.get_albums(current_user.username), validate_choice=True )
    
    premium = SelectField("Premium", choices=[' ','The song will be premium','The song will be available to everyone'],
                          validate_choice=True )
    
    #https://drive.google.com/file/d/1HMKIjUQ5g_ABZVPfVGNWh0q2o10aYoK9/view?usp=sharing
    
    
    
    submit = SubmitField("Upload")
    
        
    
    
    ################### SISTEMARE STA MERDA