from app import mysql
from flask_login import UserMixin

class Post(UserMixin):
    def __init__(self, id=None, user_id=None, date=None, title=None, content=None, caption=None, ingredients=None, instructions=None, tag=None, subtags=None, type=None):
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
