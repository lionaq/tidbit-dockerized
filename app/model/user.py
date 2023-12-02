from app import mysql, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for

@login.user_loader
def load_user(id):
    return User.search_by_id(int(id))

class User(UserMixin):
    def __init__(self, id=None, email = None, fullname = None, username = None, password = None, bio = None, website = None, profilepic = None, coverpic = None, following = None, follower = None):
        self.id = id
        self.email = email
        self.fullname = fullname
        self.username = username
        self.password = password
        self.bio = bio
        self.website = website
        self.profilepic = profilepic if profilepic else url_for('static', filename='img/default_profilepic.png')
        self.coverpic = coverpic if coverpic else url_for('static', filename='img/default_coverpic.jpg')
        self.following = following
        self.follower = follower
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT password FROM user where username = %s"
        cursor.execute(sql, (self.username,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            stored_password = user_data['password']
            return check_password_hash(stored_password, password)
        else:
            return False
    
    @classmethod
    def check_username(cls, username):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user where username = %s"
        cursor.execute(sql, (username,))
        user_data = cursor.fetchone()
        cursor.close()
        return cls(**user_data) if user_data else None

    
    @classmethod
    def check_email(self, email):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user where email = %s"
        cursor.execute(sql, (email,))
        email = cursor.fetchone()
        cursor.close()
        return email is not None

    @classmethod
    def search_by_id(cls, id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE id=%s"
        cursor.execute(sql, (id,))
        user = cursor.fetchone()
        cursor.close()
        return cls(**user) if user else None
    
    @classmethod
    def search_by_username(cls, username):
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
        
    def fetch_id(username):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT id FROM user WHERE username = %s"
        cursor.execute(sql,(username,))
        id = cursor.fetchone()
        cursor.close()

        return id

    def add(self):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "INSERT INTO user(email,fullname,username,password,bio,profilepic,coverpic) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(self.email,self.fullname,self.username,self.password,self.bio,self.profilepic,self.coverpic))
        mysql.connection.commit()
        cursor.close()
        
    @classmethod
    def fetch_user_posts(cls, user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.*, user.username, user.fullname, user.profilepic FROM post JOIN user ON post.user_id = user.id WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        posts = cursor.fetchall()
        cursor.close()
        return posts
    
    @classmethod
    def fetch_user_post_content(cls):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.id, post_url.url, post_url.type FROM user INNER JOIN post ON user.id = post.user_id INNER JOIN post_url ON post.id = post_url.post_id"
        cursor.execute(sql)
        content = cursor.fetchall()

        cursor.close()
        return content
    
    @classmethod
    def fetch_ALL_posts_except_user(cls, user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT user.fullname, user.username, user.profilepic, user.coverpic, post.id, post.user_id, post.title, post.caption FROM user JOIN post ON user.id = post.user_id WHERE NOT username = %s;"
        cursor.execute(sql, (user_id,))
        data = cursor.fetchall()

        cursor.close()
        return data
    
    @classmethod
    def fetch_ALL_content_except_user(cls, user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post_url.url, post_url.post_id, post_url.type FROM user JOIN post ON user.id = post.user_id JOIN post_url ON post.id = post_url.post_id WHERE NOT username =%s;"
        cursor.execute(sql, (user_id,))
        data = cursor.fetchall()

        cursor.close()
        return data
    
    def follow(follower, following):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "INSERT INTO follow(follower, following) VALUES (%s,%s)"
        cursor.execute(sql,(follower,following))
        mysql.connection.commit()
        cursor.close()

    def unfollow(follower, following):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            check = "SELECT * FROM follow WHERE follower = %s AND following = %s"
            sql = "DELETE FROM follow WHERE follower = %s AND following = %s"

            cursor.execute(check, (follower, following))
            checking = cursor.fetchone()

            if checking:
                cursor.execute(sql, (follower, following))
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

    def fetch_following(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT user.id, user.username, user.fullname, user.profilepic, follow.following FROM user INNER JOIN follow ON user.id = follow.following WHERE follower = %s"
        cursor.execute(sql,(id,))
        following = cursor.fetchall()

        return following

    def fetch_following_ids(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT following FROM follow WHERE follower = %s"
        cursor.execute(sql,(id,))
        following = cursor.fetchall()

        following_ids = [entry['following'] for entry in following]

        return following_ids
    
    def fetch_followers(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT user.id, user.username, user.fullname, user.profilepic, follow.follower FROM user INNER JOIN follow ON user.id = follow.follower WHERE following = %s"
        cursor.execute(sql,(id,))
        followers = cursor.fetchall()

        return followers

    def fetch_followers_ids(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT follower FROM follow WHERE following = %s"
        cursor.execute(sql,(id,))
        followers = cursor.fetchall()

        follower_ids = [entry['follower'] for entry in followers]

        return follower_ids
    
    def fetch_following_posts(id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.*, user.username, user.fullname, user.profilepic FROM post JOIN follow ON post.user_id = follow.following JOIN user ON post.user_id = user.id WHERE follow.follower = %s;"
        cursor.execute(sql, (id,))
        posts = cursor.fetchall()
        cursor.close()

        return posts
