from flask import Blueprint
from flask import render_template, request, redirect, flash
from datetime import date
from flask_login import current_user
from app.model.profile_m import Profile
from app.forms.forms import EditProfileForm
from cloudinary.uploader import upload

profile_bp = Blueprint(
    "profile_bp",
    __name__
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/<username>', methods=['GET'])
def profile(username):
    user = Profile.fetch_user_data(username)
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

@profile_bp.route('/settings/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user=current_user)
    
    if form.validate_on_submit():
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

        return render_template('edit_profile.html', status=status, form=form)
    else:
        return render_template('edit_profile.html', form=form)

@profile_bp.route('/upload-profile-pic', methods=['POST'])
def upload_profile_pic():
    if 'profile_pic' not in request.files:
        flash('No file part', 'error')
        return redirect('/settings/edit-profile')

    file = request.files['profile_pic']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect('/settings/edit-profile')

    if file and allowed_file(file.filename):
        # Upload the profile picture to Cloudinary
        result = upload(file, folder='profilepic')

        # Update the user's profilepic in the database
        profile = Profile.fetch_user_data(current_user.username)
        status = profile.update_profile_picture(result['secure_url'])

        if status:
            flash('Profile picture updated', 'success')
        else:
            flash('Failed to update profile picture', 'error')

        return redirect('/settings/edit-profile')
    else:
        flash('Invalid file type. Allowed types: png, jpg, jpeg', 'error')
        return redirect('/settings/edit-profile')
    
@profile_bp.route('/upload-cover-pic', methods=['POST'])
def upload_cover_pic():
    if 'cover_pic' not in request.files:
        flash('No file part', 'error')
        return redirect('/settings/edit-profile')

    file = request.files['cover_pic']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect('/settings/edit-profile')

    if file and allowed_file(file.filename):
        # Upload the cover picture to Cloudinary
        result = upload(file, folder='coverpic')

        # Update the user's coverpic in the database
        profile = Profile.fetch_user_data(current_user.username)
        status = profile.update_cover_picture(result['secure_url'])

        if status:
            flash('Cover picture updated', 'success')
        else:
            flash('Failed to update cover picture', 'error')

        return redirect('/settings/edit-profile')
    else:
        flash('Invalid file type. Allowed types: png, jpg, jpeg', 'error')
        return redirect('/settings/edit-profile')
        content = Profile.fetch_post_content(user.id)