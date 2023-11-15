from cloudinary.uploader import upload
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
        content_urls = []
        for file in form.content.data:
            upload_result = upload(file, folder="Tidbit-web")
            content_urls.append(upload_result['secure_url'])

        # Other form field data
        title = form.title.data
        caption = form.caption.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data
        tag = ",".join(form.tag.data)
        selected_tags = ",".join(form.subtag.data)

        post = Post(
            user_id=user_id,
            date=today,
            content=content_urls,  # Save list of content URLs
            title=title,
            caption=caption,
            ingredients=ingredients,
            instructions=instructions,
            tag=tag,
            subtags=selected_tags
        )
        post.add()

        flash("Post created successfully!", 'info')
        return redirect('/loggedin')

    return render_template('posts/create.html', form=form)


