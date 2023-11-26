from flask import Blueprint
from flask import render_template, request, redirect, flash, abort, url_for
from datetime import date
from flask_login import current_user, login_required
from app.model.posts import Post
from app.model.profile_m import Profile
from app.forms.forms import EditProfileForm
from cloudinary import uploader
from cloudinary.uploader import upload
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
                first_images[cont['id']]['type'] = cont.get('type', 'image')

        posts_with_images = zip(reversed(posts), reversed(first_images.values()))
        return render_template('profile/user_profile.html', user=user, posts_with_images=posts_with_images)
    
    return render_template('profile/user_profile.html')

@profile_bp.route('/settings/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user=current_user)
    
    if form.validate_on_submit():
        profile_pic_file = request.files['profile_pic']
        if profile_pic_file:
            result = upload(profile_pic_file, folder='profilepic')
            profile = Profile.fetch_user_data(current_user.username)
            if 'static' not in current_user.profilepic:
                public_id = Post.get_public_id_from_url(current_user.profilepic)
                delete = uploader.destroy(public_id)
                print(delete, " ", current_user.profilepic, "DELETED")
            profile.update_profile_picture(result['secure_url'])

        cover_pic_file = request.files.get('cover_pic')
        if cover_pic_file:
            result = upload(cover_pic_file, folder='coverpic')
            profile = Profile.fetch_user_data(current_user.username)
            if 'static' not in current_user.coverpic:
                public_id = Post.get_public_id_from_url(current_user.coverpic)
                delete = uploader.destroy(public_id)
                print(delete, " ", current_user.coverpic, "DELETED")
            profile.update_cover_picture(result['secure_url'])
        
        username = form.username.data
        full_name = form.fullname.data
        bio = form.bio.data
        website = form.website.data

        profile = Profile.fetch_user_data(current_user.username)
        status = profile.update_profile(username, full_name, bio, website)

        if status:
            current_user.username = username
            current_user.fullname = full_name
            current_user.bio = bio
            current_user.website = website
            flash('Profile updated', 'success')
        else:
            flash('Failed to update profile', 'error')

        return redirect(url_for('profile_bp.edit_profile'))

    return render_template('profile/edit_profile.html', form=form)