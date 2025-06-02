from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class LogisticsForm(FlaskForm):
    car_brand = StringField('car_brand', validators=[DataRequired(), Length(min=3, max=20)])
    mileage = StringField('mileage', validators=[DataRequired(), Length(min=3, max=20)])
    man_year = StringField('man_year', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Predict')