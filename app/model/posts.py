from app import mysql
from flask_login import UserMixin
import re

class Post(UserMixin):
    def __init__(self, id=None, user_id=None, date=None, title=None, content=None, caption=None, ingredients=None, instructions=None, tag=None, subtags=None, type=None, likes = None):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.title = title
        self.content = content
        self.caption = caption
        self.ingredients = ingredients
        self.instructions = instructions
        self.tag = tag
        self.subtags = subtags
        self.type = type  # Add the type field
        self.likes = likes
    def add(self):
        cursor = mysql.connection.cursor(dictionary=True)
        sql_post = "INSERT INTO post(user_id, date, title, caption, ingredients, instructions, tag, subtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_urls = "INSERT INTO post_url (post_id, url, type) VALUES (%s, %s, %s)"

        # Insert post data into the `post` table
        cursor.execute(sql_post, (self.user_id, self.date, self.title, self.caption, self.ingredients, self.instructions, self.tag, self.subtags))

        # Get the post_id of the inserted post
        post_id = cursor.lastrowid

        # Insert URLs into the `post_urls` table
        for entry in self.content:
            cursor.execute(sql_urls, (post_id, entry['url'], entry['type']))

        # Commit changes
        mysql.connection.commit()
        cursor.close()

    def edit(self):
        if self.content:
            # If there's new content to be added in
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "UPDATE post SET title = %s, caption = %s, ingredients = %s, instructions = %s, tag = %s, subtags = %s WHERE id = %s"
            sql_urls = "INSERT INTO post_url (post_id, url, type) VALUES (%s, %s, %s)"

            # Modify post data in the post table
            cursor.execute(sql, (self.title, self.caption, self.ingredients, self.instructions, self.tag, self.subtags, self.id))

            # Delete old content
            sql_del = "DELETE FROM post_url WHERE post_id = %s"
            cursor.execute(sql_del, (self.id,))

            # Insert new content into the `post_urls` table
            for entry in self.content:
                cursor.execute(sql_urls, (self.id, entry['url'], entry['type'],))

            # Commit changes
            mysql.connection.commit()
            cursor.close()
        else:
            # If no new content
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "UPDATE post SET title = %s, caption = %s, ingredients = %s, instructions = %s, tag = %s, subtags = %s WHERE id = %s"

            # Modify post data in the post table
            cursor.execute(sql, (self.title, self.caption, self.ingredients, self.instructions, self.tag, self.subtags, self.id))

            # Commit changes
            mysql.connection.commit()
            cursor.close()
            

    def delete(post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "DELETE FROM post WHERE id = %s"

        # Delete post
        cursor.execute(sql, (post_id,))

        # Commit changes
        mysql.connection.commit()
        cursor.close()


    
    def fetch_post(post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM post WHERE id = %s"
        cursor.execute(sql, (post_id,))
        post = cursor.fetchone()
        cursor.close()

        return post
    
    @classmethod
    def fetch_post_content(cls, post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM post_url WHERE post_id = %s"
        cursor.execute(sql, (post_id,))
        content = cursor.fetchall()

        cursor.close()
        return content
    
    @classmethod
    def fetch_view_post_img(cls, post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.id, post_url.url, post_url.type FROM user INNER JOIN post ON user.id = post.user_id INNER JOIN post_url ON post.id = post_url.post_id WHERE post.id = %s"
        cursor.execute(sql, (post_id,))
        content = cursor.fetchall()

        cursor.close()
        return content

    @classmethod
    def get_by_id(cls, id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM post WHERE id=%s"
        cursor.execute(sql, (id,))
        post = cursor.fetchone()
        cursor.close()
        return cls(**post) if post else None
    
    def get_public_id_from_url(url):
        match = re.search(r'/v\d+/(Tidbit-web/[^/]+)\.\w+', url)  # for images in Tidbit-web
        if not match:
            match = re.search(r'/v\d+/(Tidbit-web/[^/]+)', url)  # for videos in Tidbit-web
        if not match:
            match = re.search(r'/v\d+/(profilepic/[^/]+)\.\w+', url)  # for images in profilepic
        if not match:
            match = re.search(r'/v\d+/(coverpic/[^/]+)\.\w+', url)  # for images in coverpic

        return match.group(1) if match else None


    def fetch_liked_posts(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post_id FROM like_post WHERE liker_id = %s"
        cursor.execute(sql,(id,))
        likes = cursor.fetchall()

        liked_posts = [entry['post_id'] for entry in likes]

        return liked_posts

    def fetch_saved_posts(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post_id FROM save_post WHERE saver_id = %s"
        cursor.execute(sql,(id,))
        saves = cursor.fetchall()

        saved_posts = [entry['post_id'] for entry in saves]

        return saved_posts


    def like(liker, post):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "INSERT INTO like_post(liker_id, post_id) VALUES (%s,%s)"
            cursor.execute(sql,[liker,post])
            mysql.connection.commit()

            update = "UPDATE post SET likes = likes+1 WHERE id = %s"
            cursor.execute(update,[post])
            mysql.connection.commit()
            cursor.close()
        except:
            print("liking post failed!")

    def unlike(liker, post):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "DELETE FROM like_post WHERE liker_id = %s AND post_id = %s"

            checking = Post.like_check(liker,post)

            if checking:
                cursor.execute(sql, (liker, post))
                update = "UPDATE post SET likes = likes-1 WHERE id = %s"
                cursor.execute(update,[post])
                mysql.connection.commit()

                cursor.close()
            else:
                # Handle the case where the relationship does not exist
                # You can raise a custom exception or log a message, depending on your needs
                raise Exception("The relationship does not exist.")
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Error: {e}")
            # You might want to rollback the transaction in case of an error
            mysql.connection.rollback()
        finally:
            # Close the cursor in the 'finally' block to ensure it happens regardless of success or failure
            if cursor:
                cursor.close()

    def like_check(liker,post):
        cursor = mysql.connection.cursor(dictionary=True)
        check = "SELECT * FROM like_post WHERE liker_id = %s AND post_id = %s"
        cursor.execute(check, (liker, post))
        checking = cursor.fetchone()

        if checking:
            return True
        else:
            return False
        
    def like_amount(post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT likes FROM post WHERE id = %s"
        cursor.execute(sql, (post_id,))
        post = cursor.fetchone()
        cursor.close()

        return post
    

    def save_check(saver,post):
        cursor = mysql.connection.cursor(dictionary=True)
        check = "SELECT * FROM save_post WHERE saver_id = %s AND post_id = %s"
        cursor.execute(check, (saver, post))
        checking = cursor.fetchone()
        if checking:
            return True
        else:
            return False

    def save(saver, post):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "INSERT INTO save_post(saver_id, post_id) VALUES (%s,%s)"
            cursor.execute(sql,[saver,post])
            mysql.connection.commit()
            cursor.close()
        except:
            print("saving post failed!")

    def unsave(saver, post):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "DELETE FROM save_post WHERE saver_id = %s AND post_id = %s"

            checking = Post.save_check(saver,post)

            if checking:
                cursor.execute(sql, (saver, post))
                mysql.connection.commit()
                cursor.close()
            else:
                raise Exception("The relationship does not exist.")
        except Exception as e:
            print(f"Error: {e}")
            mysql.connection.rollback()
        finally:
            if cursor:
                cursor.close()
    
    def fetch_saved_posts(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post_id FROM save_post WHERE saver_id = %s"
        cursor.execute(sql,(id,))
        likes = cursor.fetchall()

        liked_posts = [entry['post_id'] for entry in likes]

        return liked_posts