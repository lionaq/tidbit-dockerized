from flask import Blueprint
from flask import Blueprint
from flask import render_template, request, redirect, flash, abort, url_for
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