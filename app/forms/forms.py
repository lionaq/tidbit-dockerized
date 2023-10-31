from flask_wtf import FlaskForm

from wtforms import validators,StringField,SubmitField,PasswordField

from app.model.user import User 

class RegisterForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email(message="Please enter a valid email")])
    fullname = StringField('Fullname', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired()])
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
