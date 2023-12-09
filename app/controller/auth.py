from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import  login_user,  login_required, logout_user, current_user
from app.forms.forms import RegisterForm, LoginForm
from app.model.user import User

from app import mail
from app import SECRET_KEY
from flask_mail import Message
from itsdangerous import TimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
import time
auth_bp = Blueprint(
    "auth_bp",
    __name__
)

def generate_token(email):
    s = Serializer(SECRET_KEY)
    timestamp = int(time.time())
    token = s.dumps({'email' : email, 'timestamp': timestamp})
    return token

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        user = User.check_username(username)

        if user and user.check_password(form.password.data):
            if not user.verified:
                msg = Message("Tidbit | Verify", sender=("Tidbid Admin", "tidbid@gmail.com"), recipients=[user.email])
                token = generate_token(user.email)
                url_verify = url_for('auth_bp.verify_email', token=token, _external=True)
                msg.html = render_template('auth/sendverification.html',user=user, url=url_verify)
                mail.send(msg)
                flash('Your Email is not Verified, We have send your email a verification link','message')
            else :
                login_user(user)
                return redirect(url_for('main_bp.home'))
        else:
            flash("Invalid username or password", 'message')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = RegisterForm()
    if form.validate_on_submit() and request.method =='POST':
        user = User(email=form.email.data, fullname = form.fullname.data, username = form.username.data)
        user.set_password(form.password.data)
        user.add()
        flash('Registration successful! You can now log in.', 'register')
        return redirect(url_for('auth_bp.login'))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}', 'error')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", 'info')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/verify/<token>',  methods=['GET'])
def verify_email(token):
    try:
        s = Serializer(SECRET_KEY)
        data = s.loads(token, max_age=120)
        timestamp = data['timestamp']

        current_timestamp = int(time.time())
        if timestamp < current_timestamp - 120:
            raise SignatureExpired()  

        user = User.check_email(data["email"])
        if not user:
            raise BadSignature()  

        user.update_verify()
        flash('Email verification successful! You can now log in.', 'register')
        return redirect(url_for('auth_bp.login'))

    except SignatureExpired as e:
        return render_template('auth/verifyerror.html', reason='Your Token has expired')
    except BadSignature as e:
        return render_template('auth/verifyerror.html', reason='Token is invalid')
