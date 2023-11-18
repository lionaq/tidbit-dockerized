from app import mysql, login
from flask_login import UserMixin

class Profile(UserMixin):
    def __init__(self, id=None, email=None, fullname=None, username=None, password=None, bio=None, website=None, profilepic=None, coverpic=None):
        self.id = id
        self.email = email
        self.fullname = fullname
        self.username = username
        self.password = password
        self.bio = bio
        self.website = website
        self.profilepic = profilepic if profilepic else 'static/img/default_profilepic.png'
        self.coverpic = coverpic if coverpic else 'static/img/default_coverpic.jpg'
        
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
        
    @classmethod
    def fetch_user_posts(cls, user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM post WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        posts = cursor.fetchall()
        cursor.close()
        return posts
    