from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField,DateField,SubmitField,SelectField,EmailField
from wtforms.validators import DataRequired, Length, Email

from Codice.models import Genre

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 40)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')




class RegisterForm(FlaskForm):
    
    username = StringField("Username", validators=[DataRequired(),Length(1,40)])
    name = StringField("Name", validators=[DataRequired(),Length(max=20)])
    surname = StringField("Surname", validators=[DataRequired(),Length(max=20)])
    birthdate = DateField("Birthdate", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8)])
    
    gender = SelectField("Gender", choices=[' ','M','F'], validate_choice=True )
    phone = StringField("Phone", validators=[DataRequired(),Length(min=10, max = 13)])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    
    artist = SelectField('Artist', choices=[' ','True','False'])
    
    submit = SubmitField("Register")
    
    


class SongForm(FlaskForm):
    
    username = StringField("Username", validators=[DataRequired(),Length(1,40)])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8)])
    
    name = StringField("Name", validators=[DataRequired(),Length(max=40)])
    cover = StringField("Cover", validators=[DataRequired(),Length(max=120)])
    content=StringField("Content", validators=[DataRequired(),Length(max=120)])
    release_date=DateField("Release Date", validators=[DataRequired()])
    genre=SelectField("Genre", choices=Genre.get_genre_list_database(), validate_choice=True)
    premium = SelectField("Premium", choices=[' ','The song will be premium','The song will be available to everyone'],
                          validate_choice=True )
    
    #https://drive.google.com/file/d/1HMKIjUQ5g_ABZVPfVGNWh0q2o10aYoK9/view?usp=sharing
    
    
    submit = SubmitField("Upload")
    
    
    
