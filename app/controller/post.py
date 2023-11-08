from flask import Blueprint
from flask import render_template, request, redirect, flash
from datetime import date
from flask_login import current_user
from app.forms.forms import CreatePost
from app.model.posts import Post

post_bp = Blueprint(
    "post_bp",
    __name__
)

@post_bp.route('/create-post', methods=['GET', 'POST'])
def create():
    form = CreatePost()
    if form.validate_on_submit() and request.method == 'POST':
        user_id = current_user.id
        today = date.today()
        content = request.files['content'].read()  # Read the uploaded image as bytes
        
        # Other form field data
        title = form.title.data
        caption = form.caption.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data
        selected_tags = ",".join(form.tag.data)

        post = Post(user_id=user_id, date=today, content=content, title=title, caption=caption, ingredients=ingredients, instructions=instructions, tag=selected_tags)
        post.add()
        flash('Post created successfully!', 'success')
        return redirect('/')
    return render_template('posts/create.html', form=form)



