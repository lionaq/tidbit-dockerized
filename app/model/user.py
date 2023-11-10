from app import mysql, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.search_by_id(int(id))

class User(UserMixin):
    def __init__(self, id=None, email = None, fullname = None, username = None, password = None,bio = None,profilepic = None, coverpic = None):
        self.id = id
        self.email = email
        self.fullname = fullname
        self.username = username
        self.password = password
        self.bio = bio
        self.profilepic = profilepic if profilepic else 'static/img/default_profilepic.png'
        self.coverpic = coverpic if coverpic else 'static/img/default_coverpic.jpg'
        
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


    def add(self):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "INSERT INTO user(email,fullname,username,password,bio,profilepic,coverpic) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(self.email,self.fullname,self.username,self.password,self.bio,self.profilepic,self.coverpic))
        mysql.connection.commit()
        cursor.close()
