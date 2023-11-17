from flask_wtf import FlaskForm

from wtforms import validators,StringField,SubmitField,PasswordField

from app.model.user import User 

class RegisterForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email(message="Please enter a valid email")])
    fullname = StringField('Fullname', [validators.DataRequired(), validators.Length(min=5,message="Minumum of 5 Characters")])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=5,message="Minumum of 5 Characters")])
    password = PasswordField('Password', [validators.InputRequired(),validators.EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Repeat Password', [validators.InputRequired()]) 
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.check_username(username.data)
        if user:
            raise validators.ValidationError('Username is already Taken')
    def validate_email(self, email):
        user = User.check_email(email.data)
        if user:
            raise validators.ValidationError('Email is already Taken')
        
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Sign in')

class EditProfileForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    fullname = StringField('Full Name', [validators.DataRequired()])
    bio = StringField('Bio')
    website = StringField('Website')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.current_user = kwargs['current_user']

    def validate_username(self, username):
        user = User.check_username(username.data)
        if user and user.id != self.current_user.id:
            raise validators.ValidationError('Username is already taken')