from flask import Blueprint
from flask import render_template, request,redirect,url_for, flash
from flask_login import login_user, logout_user, current_user ,login_required
from app.forms.forms import RegisterForm
from app.model.user import User

auth_bp = Blueprint(
    "auth_bp",
    __name__
)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    return None


@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
