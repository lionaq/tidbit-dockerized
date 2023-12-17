from cloudinary import uploader
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for, abort
from flask import jsonify
from datetime import date
from flask_login import current_user, login_required
from app.forms.forms import CreatePost, EditPost, SubmitForm
from app.model.posts import Post
from app.model.user import User
from app import socketio

post_bp = Blueprint(
    "post_bp",
    __name__
)

@post_bp.route('/<string:user_name>/create-post', methods=['GET', 'POST'])
@login_required
def create(user_name):
    if user_name != current_user.username:
        abort(418) # :)

    form = CreatePost()
    if form.validate_on_submit():
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
        post_id = post.add()
        flash("Post created successfully!", 'success')
        followers_id = User.fetch_followers_ids(current_user.id)
        for follower_id in followers_id:
            post.add_notification_post(current_user.id, follower_id, post_id)
        socketio.emit('get_notification')
        return redirect(url_for('profile_bp.profile', username = user_name))


    return render_template('posts/create.html', form=form)

@post_bp.route('/<string:user_name>/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(user_name, post_id):
    form = EditPost()
    # Fetch post data
    post = Post.fetch_post(post_id)
    content = Post.fetch_post_content(post_id)
    prev_content = content

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

            # Delete previous content
            for cont in prev_content:
                print(f"Deleting file from Cloudinary:", cont['url'])
                public_id = Post.get_public_id_from_url(cont['url'])
                print(f"Deleting file from Cloudinary:", public_id)
                print(cont['type'])
                
                result = uploader.destroy(public_id, resource_type = cont['type'])

                print(result)

                if 'result' in result and result['result'] == 'ok':
                    print(f"Deleted file {cont['url']} from Cloudinary successfully.")
                    
                else:
                    print(f"Failed to delete file {public_id} from Cloudinary. Result: {result}")
                    

        
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
        return redirect(url_for('profile_bp.profile',username = current_user.username))
                        
        
    else:

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
                flash("Post Successfully Deleted!", 'danger')
                socketio.emit('get_notification')
                return redirect(url_for('profile_bp.profile', username = user_name))
            else:
                print(public_id)
                print('Deletion failed!')
                return f'Deletion failed!'

        except Exception as e:
            print(f'Error: {str(e)}')
            # Handle the exception, maybe redirect to an error page or show an error message to the user
            return f'Error: {str(e)}'



@post_bp.route('/<int:postid>/viewpost', methods=['GET', 'POST'])
@login_required
def view_post(postid):
    form = SubmitForm()
    post = Post.get_by_id(postid)
    user = User.search_by_id(post.user_id)
    content = Post.fetch_view_post_img(post.id)
    user_following = User.fetch_following_ids(current_user.id)
    liked_posts = Post.fetch_liked_posts(current_user.id)
    saved_posts = Post.fetch_saved_posts(current_user.id)
    comments = Post.fetch_all_comment_in_post([postid])
    return render_template('posts/viewpost.html', post=post, comments = list(reversed(comments)), user=user, content=content, form=form, user_following=user_following, liked = liked_posts, saved = saved_posts)

@post_bp.route('/<int:postid>/viewpost/comment', methods=['POST', 'GET'])
@login_required
def view_post_comment(postid):
    form = SubmitForm()
    post = Post.get_by_id(postid)
    user = User.search_by_id(post.user_id)
    content = Post.fetch_view_post_img(post.id)
    user_following = User.fetch_following_ids(current_user.id)
    liked_posts = Post.fetch_liked_posts(current_user.id)
    saved_posts = Post.fetch_saved_posts(current_user.id)
    if request.method == "POST":
        print("HELLo")
        commentBody = request.form.get('commentBody')
        print(commentBody)
        if commentBody and commentBody.isspace() == False:
            print("IM IN")
            data = [postid, current_user.id, commentBody]
            Post.add_comment(data)
            Post().add_notification_comment(current_user.id, post.user_id, post.id)
            socketio.emit('get_notification')
        print(f'Textarea Data: {commentBody}')
        print("success!")
    else:
        print("GET")

    comments = Post.fetch_all_comment_in_post([postid])
    return render_template('posts/viewpost_comment.html', comments = comments, post=post, user=user, content=content, form=form, user_following=user_following, liked = liked_posts, saved = saved_posts)

@post_bp.route('/comment/config/<int:comment_id>/<int:user_id>', methods=['POST', 'DELETE'])
@login_required
def view_post_comment_config(comment_id, user_id):
    if request.method == 'POST':
        print("retrieved: ",comment_id, user_id )
        form_id = f'body-{comment_id}-{user_id}'
        print(form_id)
        commentBody = request.form.get(f'body-{comment_id}-{user_id}')
        check = Post.edit_comment([commentBody, comment_id, user_id])
        return jsonify({"edited": check, "body": commentBody})
    
    elif request.method == 'DELETE':
        print(comment_id)
        post_id = Post().get_post_id_from_comment_id(comment_id)
        check = Post.delete_comment([comment_id, user_id])
        if check:
            if post_id is not None:
                print(post_id)
                Post.remove_notification_comment(current_user.id, post_id['user_id'], post_id['post_id'])
                socketio.emit('get_notification')
        return jsonify({"deleted": check})

    else:
        print("none")

    return None


@post_bp.route('/like/<int:post>', methods=['POST'])
@login_required
def like(post):
    if request.method == 'POST':
        liker = current_user.id
        liked = Post.like_check(liker,post)
        post = Post.get_by_id(post)
        if liked != True:
            print("like")
            Post.like(liker, post.id)
            Post().add_notification_like(current_user.id, post.user_id, post.id)
            socketio.emit('get_notification')
            likeAmount = Post.like_amount(post.id)
            return jsonify({"likes": likeAmount.get('likes'), "liked": True})
        else:
            print("unlike")
            liker = current_user.id
            Post.unlike(liker, post.id)
            Post.remove_notification_like(current_user.id, post.user_id, post.id)
            socketio.emit('get_notification')
            likeAmount = Post.like_amount(post.id)
            return jsonify({"likes": likeAmount.get('likes'), "liked": False})
    else:
        abort(400)

@post_bp.route('/save/<int:post>', methods=['POST'])
@login_required
def save(post):
    if request.method == 'POST':
        saver = current_user.id
        saved = Post.save_check(saver,post)
        post = Post.get_by_id(post)
        if saved != True:
            print("save")
            Post.save(saver, post.id)
            Post().add_notification_save(current_user.id, post.user_id, post.id)
            socketio.emit('get_notification')
            return jsonify({ "saved": True})
        else:
            print("unsave")
            saver = current_user.id
            Post.unsave(saver, post.id)
            Post.remove_notification_save(current_user.id, post.user_id, post.id)
            socketio.emit('get_notification')
            return jsonify({"saved": False})
    else:
        abort(400)          
            
@post_bp.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    cuisines = request.form.getlist('cuisine')
    meal_types = request.form.getlist('meal_type')
    
    selected_cuisines = request.form.getlist('cuisine')
    selected_meal_types = request.form.getlist('meal_type')
    
    filters_selected = bool(selected_cuisines or selected_meal_types)

    index = 0
    limit = 10

    if filters_selected:
        postData = Post.search_posts(query, cuisines, meal_types, limit, index)
        postUser = None
    else:
        postData = Post.search_posts(query, cuisines, meal_types, limit, index)
        postUser = Post.search_users(query, current_user.id)
    
    if not postData and not postUser:
        num_of_suggestions = 3
        user_id = current_user.get_id()
        suggestions = Post.fetch_random_posts(num_of_suggestions, user_id)
        return render_template('main/search.html', selected_cuisines=selected_cuisines, selected_meal_types=selected_meal_types, suggestions=suggestions)

    following = User.fetch_following_ids(current_user.id)
    liked_posts = Post.fetch_liked_posts(current_user.id)
    saved_posts = Post.fetch_saved_posts(current_user.id)
    cont = Post.fetch_ALL_content(current_user.username)
    print(postData)
    return render_template('main/search.html', selected_cuisines=selected_cuisines, selected_meal_types=selected_meal_types, postData=postData, postCont=cont, postUser=postUser, following=following, liked_posts=liked_posts, saved_posts=saved_posts)