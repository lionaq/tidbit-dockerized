from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import  login_user,  login_required, logout_user, current_user
from app.forms.forms import RegisterForm, LoginForm
from app.model.user import User
from app.model.posts import Post

auth_bp = Blueprint(
    "auth_bp",
    __name__
)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.loggedin'))
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        user = User.check_username(username)

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/loggedin')#You can change this so it redirects to wherever after login
        else:
            flash("Invalid username or password", 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.loggedin'))
    form = RegisterForm()
    if form.validate_on_submit() and request.method =='POST':
        user = User(email=form.email.data, fullname = form.fullname.data, username = form.username.data)
        user.set_password(form.password.data)
        user.add()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", 'info')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/loggedin')
@login_required
def loggedin():
    username = current_user.username
    user = User.search_by_username(username)
    if user:
        posts = User.fetch_user_posts(user.id)
        content = User.fetch_user_post_content(user.id)

        return render_template('/loggedin.html', name = username, user=user, posts=posts, content=content)
    
