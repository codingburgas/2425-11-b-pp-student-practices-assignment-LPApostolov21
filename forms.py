from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    role = SelectField(
        'Select Role',
        choices=[('admin', 'Admin'), ('user', 'User')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class LinearForm(FlaskForm):
    car_brand = StringField('Car Brand', validators=[DataRequired(), Length(min=3, max=20)])
    mileage = IntegerField('Mileage (In kilometers)', validators=[DataRequired(), NumberRange(min=100000)])
    man_year = IntegerField('Year of manufacture(1990 - 2010)', validators=[DataRequired(), NumberRange(min=1990, max=2010)])
    submit = SubmitField('Predict')
