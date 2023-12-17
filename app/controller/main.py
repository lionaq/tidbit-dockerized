from flask import Blueprint
from flask_login import current_user, login_required
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.model.user import User
from app.model.posts import Post
import random
from app import socketio

main_bp = Blueprint(
    "main_bp",
    __name__
)


@main_bp.route('/explore/posts')
def get_posts_explore():
    index = request.args.get('index', 1, type=int)
    limit = request.args.get('limit', 1, type=int)
    posts = Post.fetch_post_paginated_explore(limit, index, current_user.id)

    return jsonify(data=posts, has_next=len(posts) == limit)

@main_bp.route('/home/posts')
def get_posts_feed():
    index = request.args.get('index', 1, type=int)
    limit = request.args.get('limit', 1, type=int)
    posts = Post.fetch_post_paginated_feed(limit, index, current_user.id)

    return jsonify(data=posts, has_next=len(posts) == limit, current_user_id = current_user.id)


@main_bp.route('/home')
@login_required
def home():
    return render_template('main/loggedin.html')
    
@main_bp.route('/explore')
@login_required
def explore():
    return render_template('main/explore.html')

@main_bp.route('/getnotif/update/<notification_id>', methods=['GET'])
@login_required
def update_read_notification(notification_id):
    post_id = Post.update_read_notification(notification_id)
    print(notification_id)
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
    notification_setting = User.get_notif_settings(user_id)

    filtered_notifications = [
        notif for notif in notification 
        if notification_setting.get(f"receive_{notif['type'].lower()}_notifications", False)
    ]

    count = sum(1 for notif in filtered_notifications if notif['is_read'] == 0)
    data = {'html': render_template('main/notification.html', notification=filtered_notifications, setting=notification_setting), 'unread_count': count}
    socketio.emit('update_notification_dom', data=data, room=request.sid)
