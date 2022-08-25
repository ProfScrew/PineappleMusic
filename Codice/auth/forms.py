from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField,DateField,SubmitField,SelectField,EmailField
from wtforms.validators import DataRequired, Length, Email


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
    phone = StringField("Phone", validators=[DataRequired(),Length(min=6, max = 6)])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    
    artist = SelectField('Artist', choices=[' ','True','False'])
    
    submit = SubmitField("Registrati")
    
