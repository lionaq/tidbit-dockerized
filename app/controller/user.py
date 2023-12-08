from flask import Blueprint
from flask import Blueprint
from flask import request, abort, jsonify
from flask_login import current_user, login_required
from app.model.user import User

user_bp = Blueprint(
    "user_bp",
    __name__
)

@user_bp.route('/follow/<int:following>', methods=['POST'])
@login_required
def follow(following):
    if request.method == 'POST':
        follower = current_user.id
        User.follow(follower, following)
        following_list = User.fetch_following_ids(follower)
        response_data = {
            #'message': 'You are now following this user.',
            'following_count': len(following_list),
        }
        return jsonify(response_data)
    else:
        abort(405)

@user_bp.route('/unfollow/<int:following>', methods=['POST'])
@login_required
def unfollow(following):
    if request.method == 'POST':
        follower = current_user.id
        User.unfollow(follower, following)
        followers = User.fetch_followers_ids(follower)
        response_data = {
            #'message': 'You have unfollowed this user.',
            'following_count': len(followers),
        }
        return jsonify(response_data)
    else:
        abort(405)