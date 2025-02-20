from app import mysql
from flask_login import UserMixin
from flask import url_for
class Profile(UserMixin):
    def __init__(self, id=None, email=None, fullname=None, username=None, password=None, bio=None, website=None, profilepic=None, coverpic=None):
        self.id = id
        self.email = email
        self.fullname = fullname
        self.username = username
        self.password = password
        self.bio = bio
        self.website = website
        self.profilepic = profilepic if profilepic else url_for('static', filename='img/default_profilepic.png')
        self.coverpic = coverpic if coverpic else url_for('static', filename='img/default_coverpic.jpg')
        
    @classmethod
    def fetch_user_data(cls, username):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE username = %s"
        cursor.execute(sql, (username,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return cls(
                id=user_data['id'],
                email=user_data['email'],
                fullname=user_data['fullname'],
                username=user_data['username'],
                password=user_data['password'],
                bio=user_data['bio'],
                website=user_data['website'],
                profilepic=user_data['profilepic'],
                coverpic=user_data['coverpic']
            )
        else:
            return None
           
    def fetch_post_content(user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.id, post_url.url, post_url.type FROM user INNER JOIN post ON user.id = post.user_id INNER JOIN post_url ON post.id = post_url.post_id WHERE user.id = %s"
        cursor.execute(sql, (user_id,))
        content = cursor.fetchall()
        cursor.close()
        return content
    
    def fetch_liked_post_content(user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.id, post_url.url, post_url.type FROM user JOIN like_post ON user.id = like_post.liker_id JOIN post ON like_post.post_id = post.id JOIN post_url ON post.id = post_url.post_id WHERE user.id = %s;"
        cursor.execute(sql, (user_id,))
        content = cursor.fetchall()
        cursor.close()
        return content

    def fetch_saved_post_content(user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.id, post_url.url, post_url.type FROM user JOIN save_post ON user.id = save_post.saver_id JOIN post ON save_post.post_id = post.id JOIN post_url ON post.id = post_url.post_id WHERE user.id = %s;"
        cursor.execute(sql, (user_id,))
        content = cursor.fetchall()
        cursor.close()
        return content
    
    @classmethod
    def fetch_user_posts(cls, user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM post WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        posts = cursor.fetchall()
        cursor.close()
        return posts
    def update_profile(self, new_username, new_fullname, new_bio, new_website):
        cursor = mysql.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s", (new_username,))
        result = cursor.fetchone()

        if result and result['id'] != self.id:
            return False
        else:
            sql = "UPDATE user SET username = %s, fullname = %s, bio = %s, website = %s WHERE id = %s"
            cursor.execute(sql, (new_username, new_fullname, new_bio, new_website, self.id))
            mysql.connection.commit()
            cursor.close()
            return True

    def update_profile_picture(self, new_profilepic):
        cursor = mysql.connection.cursor(dictionary=True)

        sql = "UPDATE user SET profilepic = %s WHERE id = %s"
        cursor.execute(sql, (new_profilepic, self.id))
        mysql.connection.commit()

        cursor.close()
        return True
    
    def update_cover_picture(self, new_coverpic):
        cursor = mysql.connection.cursor(dictionary=True)

        sql = "UPDATE user SET coverpic = %s WHERE id = %s"
        cursor.execute(sql, (new_coverpic, self.id))
        mysql.connection.commit()

        cursor.close()
        return True