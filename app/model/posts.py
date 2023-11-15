from app import mysql
from flask_login import UserMixin

class Post(UserMixin):
    def __init__(self, id=None, user_id=None, date=None, title=None, content=None, caption=None, ingredients=None, instructions=None, tag=None, subtags=None):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.title = title
        self.content = content
        self.caption = caption
        self.ingredients = ingredients
        self.instructions = instructions
        self.tag = tag
        self.subtag = subtags

    
    def add(self):
        cursor = cursor = mysql.connection.cursor(dictionary=True)
        sql = "INSERT INTO post(user_id, date, title, content, caption, ingredients, instructions, tag, subtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(self.user_id, self.date, self.title, self.content, self.caption, self.ingredients, self.instructions, self.tag, self.subtag))
        mysql.connection.commit()
        cursor.close()
