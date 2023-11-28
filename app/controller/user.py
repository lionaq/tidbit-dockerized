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

        # Assuming your User.follow method is in a class method or static method
        User.follow(follower, following)

        flash("You are now following this user.", "success")

        # Redirect back to the page the user came from
        return redirect(request.referrer)
    else:
        abort(405)  # Method Not Allowed