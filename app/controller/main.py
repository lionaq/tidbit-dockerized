from flask import Blueprint
from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, flash
from app.model.user import User
import random

main_bp = Blueprint(
    "main_bp",
    __name__
)

@main_bp.route('/home')
@login_required
def home():
    username = current_user.username
    user = User.search_by_username(username)
    if user:
        posts = User.fetch_user_posts(user.id)
        content = User.fetch_user_post_content()

        return render_template('main/loggedin.html', name = username, user=user, posts=posts, content=content)
    
@main_bp.route('/explore')
@login_required
def explore():

        data = User.fetch_ALL_posts_except_user(current_user.username)
        cont = User.fetch_ALL_content_except_user(current_user.username)
        random.shuffle(data)
        return render_template('main/explore.html', postData = data, postCont = cont)