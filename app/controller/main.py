from flask import Blueprint
from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, flash
from app.model.user import User
from app.model.posts import Post
import random
from app import socketio

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
        user_following = User.fetch_following_ids(user.id)
        liked_posts = Post.fetch_liked_posts(user.id)
        saved_posts = Post.fetch_saved_posts(current_user.id)
        comments = Post.fetch_all_comment_ids()
        print(comments)
        if user_following:
            following_posts = User.fetch_following_posts(user.id)
            print(user_following)
            # Check if following_posts is not empty before extending posts
            if following_posts:
                posts.extend(following_posts)
                random.shuffle(posts)
        return render_template('main/loggedin.html', comments = comments, name=username, user=user, posts=posts, content=content, following=user_following, liked = liked_posts, saved = saved_posts)
    
@main_bp.route('/explore')
@login_required
def explore():
    data = User.fetch_ALL_posts_except_user(current_user.username)
    cont = User.fetch_ALL_content_except_user(current_user.username)
    following = User.fetch_following_ids(current_user.id)
    liked_posts = Post.fetch_liked_posts(current_user.id)
    saved_posts = Post.fetch_saved_posts(current_user.id)
    print("saved", saved_posts)
    random.shuffle(data)
    comments = Post.fetch_all_comment_ids()
    return render_template('main/explore.html', comments = comments, postData = data, postCont = cont, following = following, liked = liked_posts, saved = saved_posts)

@main_bp.route('/settings/guidelines')
@login_required
def guidelines():
    return render_template('main/guidelines.html')

@main_bp.route('/getnotif/update/<notification_id>', methods=['GET'])
@login_required
def update_read_notification(notification_id):
    post_id = Post.update_read_notification(notification_id)
    socketio.emit('get_notification')
    if post_id['type'] == 'FOLLOW':
        username = User.search_by_id(post_id['notifier'])
        return redirect(url_for('profile_bp.profile', username = username.username))
    if post_id['type'] == 'COMMENT':
        return redirect(url_for('post_bp.view_post_comment', postid = post_id['post_id']))
    
    return redirect(url_for('post_bp.view_post', postid = post_id['post_id']))

@socketio.on('get_notification')
@login_required
def get_notification(data):
    user_id = data.get('user_id')
    notification = Post.get_notification_post(user_id)
    count = sum(1 for notif in notification if notif['is_read'] == 0)    
    data = {'html' : render_template('main/notification.html', notification=notification), 'unread_count' : count}
    socketio.emit('update_notification_dom', data=data,room=request.sid)
