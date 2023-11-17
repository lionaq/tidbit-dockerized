from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Blueprint
from flask import render_template, request, redirect, flash
from datetime import date
from flask_login import current_user, login_required
from app.forms.forms import CreatePost
from app.model.posts import Post

post_bp = Blueprint(
    "post_bp",
    __name__
)

@post_bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePost()
    if form.validate_on_submit() and request.method == 'POST':
        user_id = current_user.id
        today = date.today()

        # Upload images/videos to Cloudinary
        uploaded_content = []
        for file in form.content.data:
            resource_type = 'video' if file.filename.endswith(('.mp4', '.mov')) else 'image'
            upload_result = upload(file, folder="Tidbit-web", resource_type=resource_type)
            secure_url = upload_result['secure_url'] if resource_type == 'image' else cloudinary_url(upload_result['public_id'], resource_type='video')[0]
            type = 'image' if resource_type == 'image' else 'video'
            uploaded_content.append({'url': secure_url, 'type': type})

        # Create one Post instance and add it to the database
        post = Post(
            user_id=user_id,
            date=today,
            content=uploaded_content,
            title=form.title.data,
            caption=form.caption.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            tag=",".join(form.tag.data),
            subtags=",".join(form.subtag.data)
        )

        # Add the post to the database
        post.add()

        flash("Post created successfully!", 'info')
        return redirect('/loggedin')

    return render_template('posts/create.html', form=form)






