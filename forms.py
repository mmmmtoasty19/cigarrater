from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, RadioField
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo, NumberRange

from models import User

def name_exists(form, feild):
    if User.select().where(User.username == feild.data).exists():
        raise ValidationError("User with that name already exists.")

def email_exists(form, feild):
    if User.select().where(User.email == feild.data).exists():
        raise ValidationError("User with that email already exists.")



class RegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
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
    body = SelectField('Body', validators=[
        DataRequired()
    ], choices=[('Light','Light'),('Medium-Light','Medium-Light'),
        ('Medium', 'Medium'), ('Medium-Full', 'Medium-Full'), ('Full','Full')])
    wrapper = StringField('Wrapper')
    binder = StringField('Binder')
    filler = StringField('Filler')
    orgin = StringField('Orgin')


class RatingForm(FlaskForm):
    size = SelectField('Cigar Size', choices=[
        ('Corona','Corona'), ('Petite Corona','Petite Corona'),
        ('Corona Grand','Corona Grand'), ('Double Corona','Double Corona'),
        ('Lonsdale','Lonsdale'), ('Robusto','Robusto'),
        ('Toro','Toro'), ('Churchill','Churchill'), ('Lancero','Lancero'),
        ('Torpedo','Torpedo'), ('Pyramid','Pyramid'), ('Belicoso','Belicoso'),
        ('Perfecto','Perfecto') 
    ])
    comment = TextAreaField('Comments')
    rating = DecimalRangeField('Rating', render_kw={'min':1, 'max':10, 'step':1, 'value':5, 'class':'cigar_rating__range'})
   
    # old version of rating using radio buttons, have changed to slider.  need to remove later
    # rating = RadioField('Rating', 
    #     choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')], validators=[DataRequired()])
    
    