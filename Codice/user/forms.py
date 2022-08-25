from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField,DateField,SubmitField,SelectField,EmailField
from wtforms.validators import DataRequired, Length, Email, Optional


class ModifyProfileForm(FlaskForm):
    
    
    name = StringField("Name", validators=[DataRequired(),Length(max=20)])
    surname = StringField("Surname", validators=[DataRequired(),Length(max=20)])
    birthdate = DateField("Birthdate", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Optional(), Length(min=8)])
    
    phone = StringField("Phone", validators=[DataRequired(),Length(min=6)])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    
    submit = SubmitField("Update")
    
    