from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User

def name_exists(form, feild):
    if User.select().where(User.username == feild.data).exists():
        raise ValidationError("User with that name already exists.")

def email_exists(form, feild):
    if User.select().where(User.email == feild.data).exists():
        raise ValidationError("User with that email already exists.")



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Regexp(r'^[a-zA-Z0-9_]+$', 
            message=("Username should be one word, letters,"
             "numbers and underscores only.")),
        name_exists
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        email_exists
    ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ]
    )


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])


class CigarForm(FlaskForm):
    """Form to add new cigar"""
    cigar_name = StringField('Cigar Name', validators=[
        DataRequired()
    ])
    brand = StringField('Brand Name', validators=[
        DataRequired()
    ])
    body = StringField('Body', validators=[
        DataRequired()
    ])
    wrapper = StringField('Wrapper')
    binder = StringField('Binder')
    filler = StringField('Filler')
    orgin = StringField('Orgin')

