from flask import Blueprint
from flask import Blueprint
from flask import request, redirect, flash, abort, render_template
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

        flash("You are now following this user.", "success")

        return redirect(request.referrer)
    else:
        abort(405)

@user_bp.route('/unfollow/<int:following>', methods=['POST'])
@login_required
def unfollow(following):
    if request.method == 'POST':
        follower = current_user.id
        User.unfollow(follower, following)

        return redirect(request.referrer)
    else:
        abort(405)

@user_bp.route('/<string:username>/following', methods=['GET'])
@login_required
def following(username):
    userID = User.fetch_id(username)
    user = User.search_by_id(userID['id'])
    following = User.fetch_following(userID['id'])
    following_num = len(following)
    user_following = User.fetch_following_ids(current_user.id)

    return render_template('profile/following.html', user=user, following=following, following_num=following_num, user_following=user_following)