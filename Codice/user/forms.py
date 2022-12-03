from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField,DateField,SubmitField,EmailField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Optional

months = ['',1,2,3,4,5,6,7,8,9,10,11,12]
years = ['', 2022, 2023, 2024, 2025, 2026, 2027]

class ModifyProfileForm(FlaskForm):
    
    
    name = StringField("Name", validators=[DataRequired(),Length(max=20)])
    surname = StringField("Surname", validators=[DataRequired(),Length(max=20)])
    birthdate = DateField("Birthdate", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Optional(), Length(min=8)])
    
    phone = StringField("Phone", validators=[DataRequired(),Length(min=10,max=13)])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    
    submit = SubmitField("Update")
    
    
class CrediCardForm(FlaskForm):
    
    card_number = StringField("CardNumber", validators=[DataRequired(), Length(min=16,max=16)])
    month = SelectField("Month", choices=months, validate_choice=True )
    year = SelectField("Year", choices=years, validate_choice=True )
    cvv =StringField("CVV", validators=[DataRequired(), Length(min=3,max=3)])
  
    submit = SubmitField("Update")
    
class TableChoice(FlaskForm):
    choice = HiddenField("choice")