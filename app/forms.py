from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, BooleanField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf.file import FileField, FileAllowed
from app.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    dob = DateField('Date of Birth (DD/MM/YYYY)', format='%m/%d/%Y', validators=[DataRequired()])
    submit = SubmitField('Continue')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already registered. Try logging in.')

    def validate_dob(self, dob):
        if dob.data.year > 2001:
            raise ValidationError('You must be 18 years or older to register.')
        elif dob.data.year < 1930:
            raise ValidationError('Are you sure this is your age? Try again.')

class DetailsForm(FlaskForm):
    picture = FileField('Add Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    gender = RadioField('Gender', validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    aadhar = StringField('Aadhar Number', validators=[DataRequired(), Length(min=10, max=10)])
    about_me = TextAreaField('About Me', validators=[DataRequired(), Length(min=2, max=140)])
    submit = SubmitField('Register')

    def validate_phone_number(self, phone):
        user = User.query.filter_by(phone_number=phone.data).first()
        if user is not None:
            raise ValidationError('This phone number is already registered. Try logging in.')

    def validate_aadhar(self, aadhar):
        user = User.query.filter_by(aadhar=aadhar.data).first()
        if user is not None:
            raise ValidationError('This Aadhar card is already registered. Try logging in.')