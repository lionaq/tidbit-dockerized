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
    user = Profile.fetch_user_data(username)
    if user:
        posts = Profile.fetch_user_posts(user.id)
        content = Profile.fetch_post_content(user.id)

        first_images = {post['id']: None for post in posts}

        for cont in content:
            if cont['id'] in first_images and first_images[cont['id']] is None:
                first_images[cont['id']] = cont['url']

        posts_with_images = zip(posts, first_images.values())

        return render_template('user_profile.html', user=user, posts_with_images=posts_with_images)
    
    return render_template('user_profile.html')