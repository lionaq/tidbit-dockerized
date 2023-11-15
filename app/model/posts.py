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
        sql = "INSERT INTO post(user_id, date, title, caption, ingredients, instructions, tag, subtags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_urls = "INSERT INTO post_url (post_id, url) VALUES (%s, %s)"

        # Insert post data into the `post` table
        cursor.execute(sql, (self.user_id, self.date, self.title, self.caption, self.ingredients, self.instructions, self.tag, self.subtag))

        # Get the post_id of the inserted post
        post_id = cursor.lastrowid

        # Insert URLs into the `post_urls` table
        for url in self.content:
            cursor.execute(sql_urls, (post_id, url))

        # Commit changes
        mysql.connection.commit()

