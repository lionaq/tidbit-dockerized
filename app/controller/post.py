from cloudinary import uploader
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from datetime import date
from flask_login import current_user, login_required
from app.forms.forms import CreatePost, EditPost
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

from flask import render_template

@post_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    form = EditPost()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.content.data:
                print('Pass 2')
                # Upload images/videos to Cloudinary, if any
                uploaded_content = []
                for file in form.content.data:
                    resource_type = 'video' if file.filename.endswith(('.mp4', '.mov')) else 'image'
                    upload_result = upload(file, folder="Tidbit-web", resource_type=resource_type)
                    secure_url = upload_result['secure_url'] if resource_type == 'image' else cloudinary_url(upload_result['public_id'], resource_type='video')[0]
                    type = 'image' if resource_type == 'image' else 'video'
                    uploaded_content.append({'url': secure_url, 'type': type})

                # Create one Post instance and change it
                post = Post(
                    id = post_id,
                    content=uploaded_content,
                    title=form.title.data,
                    caption=form.caption.data,
                    ingredients=form.ingredients.data,
                    instructions=form.instructions.data,
                    tag=",".join(form.tag.data),
                    subtags=",".join(form.subtag.data)
                )

                # Modify the post on the database
                post.edit()

                flash("Post modified successfully!", 'info')
                return redirect('/loggedin')
            
            else:
                # Create one Post instance and change it
                post = Post(
                    id = post_id,
                    title=form.title.data,
                    caption=form.caption.data,
                    ingredients=form.ingredients.data,
                    instructions=form.instructions.data,
                    tag=",".join(form.tag.data),
                    subtags=",".join(form.subtag.data)
                )

                # Modify post on the database
                post.edit()

                flash("Post modified successfully!", 'info')
                return redirect('/loggedin')
            
        else:
            print(form.errors)
            flash("Form validation failed", 'danger')
            
        
    else:
        flash(form.errors, 'danger')

    # Fetch post data
    post = Post.fetch_post(post_id)
    content = Post.fetch_post_content(post_id)

    # Populate the form with existing data
    form.title.data = post['title']
    form.caption.data = post['caption']
    form.ingredients.data = post['ingredients']
    form.instructions.data = post['instructions']

    # Set data for tag and subtag
    form.tag.data = post['tag'].split(',') if post['tag'] else []
    form.subtag.data = post['subtags'].split(',') if post['subtags'] else []

    userName = current_user.username
    return render_template('posts/edit.html', form=form, post=post, content=content, userName = userName)


@post_bp.route('/<string:user_name>/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete(user_name, post_id):
    if request.method == 'POST':
        # Get the file URL/s from the request
        content = Post.fetch_post_content(post_id)
            
        try:
            goods = False
            # Delete the file from Cloudinary
            for cont in content:
                print(f"Deleting file from Cloudinary:", cont['url'])
                public_id = Post.get_public_id_from_url(cont['url'])
                print(f"Deleting file from Cloudinary:", public_id)
                print(cont['type'])
                
                result = uploader.destroy(public_id, resource_type = cont['type'])

                print(result)

                if 'result' in result and result['result'] == 'ok':
                    print(f"Deleted file {cont['url']} from Cloudinary successfully.")
                    goods = True
                else:
                    print(f"Failed to delete file {public_id} from Cloudinary. Result: {result}")
                    goods = False

            if goods == True:
                # Delete post from post table
                Post.delete(post_id)
                return redirect(url_for('profile_bp.profile', username = user_name))
            else:
                print(public_id)
                print('Deletion failed!')
                return f'Deletion failed!'

        except Exception as e:
            print(f'Error: {str(e)}')
            # Handle the exception, maybe redirect to an error page or show an error message to the user
            return f'Error: {str(e)}'






