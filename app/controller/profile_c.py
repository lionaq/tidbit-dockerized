from flask import Blueprint
from flask import render_template, request, redirect, flash
from datetime import date
from flask_login import current_user
from app.model.profile_m import Profile

profile_bp = Blueprint(
    "profile_bp",
    __name__
)

@profile_bp.route('/<username>', methods=['GET'])
def profile(username):
    user = Profile.fetch_user_by_username(username)
    if user:
        return render_template('user_profile.html', user=user)
    else:
        flash('User not found', 'error')
        return redirect(url_for('home')) 