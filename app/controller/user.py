from flask import Blueprint
from flask import Blueprint
from flask import request, abort, jsonify, flash
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
        check_following = User.check_if_following(follower, following)
        # Check if User is already following
        if check_following == False:
            User.follow(follower, following)
            following_list = User.fetch_following_ids(follower)
            following_followers_list = User.fetch_followers_ids(following)
            return jsonify({"following": check_following, 'following_count': len(following_list), 'following_followers': len(following_followers_list)})
        else:
            return jsonify({"following": check_following})
    else:
        abort(405)

@user_bp.route('/unfollow/<int:following>', methods=['POST'])
@login_required
def unfollow(following):
    if request.method == 'POST':
        follower = current_user.id
        check_following = User.check_if_following(follower, following)
        if check_following == True:
            User.unfollow(follower, following)
            following_list = User.fetch_following_ids(follower)
            print(following)
            following_followers_list = User.fetch_followers_ids(following)
            return jsonify({"following": check_following, 'following_count': len(following_list), 'following_followers': len(following_followers_list)})
        else:
            return jsonify({"following": check_following})
    else:
        abort(405)