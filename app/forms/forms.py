from flask_wtf import FlaskForm

from flask_wtf.file import MultipleFileField, FileAllowed, FileField

from wtforms import validators,StringField,SubmitField,PasswordField, SelectMultipleField, widgets, TextAreaField

from app.model.user import User

import re

class RegisterForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email(message="Please enter a valid email")])
    fullname = StringField('Fullname', [validators.DataRequired(), validators.Length(min=5,message="Minumum of 5 Characters")])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=5,max=20,message="Username must be between 5-20 Characters")])
    password = PasswordField('Password', [validators.InputRequired(),validators.EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Repeat Password', [validators.InputRequired()]) 
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        if not re.match("^[a-zA-Z0-9_]*$", username.data):
            raise validators.ValidationError('Username should only contain letters, numbers, and underscores.')
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

class CreatePost(FlaskForm):
    content = MultipleFileField('Content', validators=[FileAllowed(['jpg', 'png', 'gif', 'mp4', 'mov']), validators.DataRequired()])
    title = StringField('Title', validators=[validators.DataRequired(), validators.Length(max=255)])
    caption = TextAreaField('Caption', validators=[validators.DataRequired(), validators.Length(max=255)] )
    ingredients = TextAreaField('Ingredients', [validators.DataRequired()])
    instructions = TextAreaField('Instructions', [validators.DataRequired()])
    tag =  SelectMultipleField('Tag', choices=[('American Cuisine', 'American Cuisine'), ('Filipino Cuisine', 'Filipino Cuisine'), ('French Cuisine', 'French Cuisine'), ('Japanese Cuisine', 'Japanese Cuisine'), ('Chinese Cuisine', 'Chinese Cuisine'), ('Greek Cuisine', 'Greek Cuisine'), ('Mexican Cuisine', 'Mexican Cuisine'), ('Indian Cuisine', 'Indian Cuisine'), ('Thai Cuisine', 'Thai Cuisine')], widget=widgets.ListWidget(prefix_label=False))
    subtag = SelectMultipleField('Subtags', choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('snack', 'Snack'), ('dinner', 'Dinner'), ('dessert', 'Dessert')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Create Post')

class EditPost(FlaskForm):
    content = MultipleFileField('Content', validators=[FileAllowed(['jpg', 'png', 'gif', 'mp4', 'mov']), validators.Optional()])
    title = StringField('Title', [validators.DataRequired()])
    caption = TextAreaField('Caption', [validators.DataRequired()] )
    ingredients = TextAreaField('Ingredients', [validators.DataRequired()])
    instructions = TextAreaField('Instructions', [validators.DataRequired()])
    tag =  SelectMultipleField('Tag', choices=[('American Cuisine', 'American Cuisine'), ('Filipino Cuisine', 'Filipino Cuisine'), ('French Cuisine', 'French Cuisine'), ('Japanese Cuisine', 'Japanese Cuisine'), ('Chinese Cuisine', 'Chinese Cuisine'), ('Greek Cuisine', 'Greek Cuisine'), ('Mexican Cuisine', 'Mexican Cuisine'), ('Indian Cuisine', 'Indian Cuisine'), ('Thai Cuisine', 'Thai Cuisine')], widget=widgets.ListWidget(prefix_label=False))
    subtag = SelectMultipleField('Subtags', choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('snack', 'Snack'), ('dinner', 'Dinner'), ('dessert', 'Dessert')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Edit Post')
