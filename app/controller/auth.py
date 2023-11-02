from flask import Blueprint
from flask import render_template, request,redirect,url_for, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from app.forms.forms import RegisterForm, LoginForm
from app.model.user import User

auth_bp = Blueprint(
    "auth_bp",
    __name__
)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('loggedin'))
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        user = User.check_username(username)

        if user:
            # User is found, so let's check the password
            if user.check_password(form.password.data):
                login_user(user)
                return redirect('/loggedin')#You can change this so it redirects to wherever after login
            else:
                flash("Wrong password")
        else:
            flash("User not found")
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('loggedin'))
    form = RegisterForm()
    if form.validate_on_submit() and request.method =='POST':
        user = User(email=form.email.data, fullname = form.fullname.data, username = form.username.data)
        print(form.email.data)
        print(form.fullname.data)
        print(form.username.data)
        print(form.password.data)
        user.set_password(form.password.data)
        user.add()
        #############################
        #message flash or smth??? idk to indicate register succesfully??
        flash('Registration successful! You can now log in.')
        return redirect(url_for('auth_bp.loggingin'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('index'))
