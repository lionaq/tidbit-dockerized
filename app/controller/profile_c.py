from flask import Blueprint
from flask import render_template, abort, request
from flask_login import current_user
from app.model.profile_m import Profile

profile_bp = Blueprint(
    "profile_bp",
    __name__
)

@profile_bp.route('/<string:username>', methods=['GET'])
def profile(username):
    user = Profile.fetch_user_data(username)
    if user == None or request.method != 'GET':
        abort(404)
        
    if user:
        posts = Profile.fetch_user_posts(user.id)
        content = Profile.fetch_post_content(user.id)

        first_images = {post['id']: {'url': None, 'type': 'image'} for post in posts}

        for cont in content:
            if cont['id'] in first_images and first_images[cont['id']]['url'] is None:
                first_images[cont['id']]['url'] = cont['url']
                first_images[cont['id']]['type'] = cont.get('type', 'image')  # Default to 'image' if 'type' is not present or None

        posts_with_images = zip(posts, first_images.values())

        return render_template('user_profile.html', user=user, posts_with_images=posts_with_images)
    
    return render_template('user_profile.html')