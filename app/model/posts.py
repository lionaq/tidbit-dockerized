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

        return post_id

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
    
    def fetch_post_paginated_explore(limit, index, current_user_id):
        # Connect to the MySQL database
        cursor = mysql.connection.cursor(dictionary=True)
        # Example query, replace with your actual query
        query = f'''SELECT A.* FROM (SELECT
                        post.id,post.user_id, user.fullname, user.username, user.profilepic,
                        post.date, post.title, post.caption, post.likes,
                        GROUP_CONCAT(post_url.url) AS grouped_urls,
                        CASE 
                            WHEN EXISTS (
                                SELECT 1 
                                FROM like_post AS lp 
                                WHERE lp.liker_id = {current_user_id}
                                AND lp.post_id = post.id
                            ) THEN 1
                            ELSE 0
                        END AS liked,
                        CASE 
                            WHEN EXISTS (
                                SELECT 1 
                                FROM save_post AS sp 
                                WHERE sp.saver_id = {current_user_id}
                                AND sp.post_id = post.id
                            ) THEN 1
                            ELSE 0
                        END AS saved,
                        CASE 
                            WHEN EXISTS (
                                SELECT 1 
                                FROM follow
                                WHERE follow.follower = {current_user_id}
                                AND follow.following = post.user_id
                            ) THEN 1
                            ELSE 0
                        END AS followed,
                        (
                            SELECT COUNT(*) 
                            FROM comment
                            WHERE comment.post_id = post.id
                        ) AS comments
                    FROM
                        post
                    JOIN
                        post_url ON post.id = post_url.post_id
                    JOIN
                        user ON user.id = post.user_id
                    WHERE NOT user.id = {current_user_id}
                    GROUP BY
                        post.id, user.fullname, user.username,user.profilepic, post.user_id, post.date, post.title, post.caption, post.ingredients, post.instructions, post.tag, post.subtags, post.likes 
                    ORDER BY id LIMIT {limit} OFFSET {index}
                    ) AS A ORDER BY RAND()'''
        
        cursor.execute(query)
        posts = cursor.fetchall()
        cursor.close()
        return posts
    
    def fetch_post_paginated_feed(limit, index, current_user_id):
        # Connect to the MySQL database
        cursor = mysql.connection.cursor(dictionary=True)
        # Example query, replace with your actual query
        query = f'''
                SELECT A.* FROM (
                        SELECT *
                        FROM (
                            SELECT
                                post.id, post.user_id AS user_id, user.fullname, user.username, user.profilepic,
                                post.date, post.title, post.caption, post.likes,
                                GROUP_CONCAT(post_url.url) AS grouped_urls,
                                CASE 
                                    WHEN EXISTS (
                                        SELECT 1 
                                        FROM like_post AS lp 
                                        WHERE lp.liker_id = {current_user_id}
                                        AND lp.post_id = post.id
                                    ) THEN 1
                                    ELSE 0
                                END AS liked,
                                CASE 
                                    WHEN EXISTS (
                                        SELECT 1 
                                        FROM save_post AS sp 
                                        WHERE sp.saver_id = {current_user_id}
                                        AND sp.post_id = post.id
                                    ) THEN 1
                                    ELSE 0
                                END AS saved,
                                CASE 
                                    WHEN EXISTS (
                                        SELECT 1 
                                        FROM follow
                                        WHERE follow.follower = {current_user_id}
                                        AND follow.following = post.user_id
                                    ) THEN 1
                                    ELSE 0
                                END AS followed,
                                (
                                    SELECT COUNT(*) 
                                    FROM comment
                                    WHERE comment.post_id = post.id
                                ) AS comments
                            FROM
                                post
                            JOIN
                                post_url ON post.id = post_url.post_id
                            JOIN
                                user ON user.id = post.user_id
                            GROUP BY
                                post.id, user.fullname, user.username, user.profilepic, post.user_id, post.date, post.title, post.caption, post.likes
                        ) AS subquery
                        WHERE
                            followed = 1 OR user_id = {current_user_id}
                        ORDER BY id LIMIT {limit} OFFSET {index}
                    ) AS A ORDER BY RAND();

                '''
        
        cursor.execute(query)
        posts = cursor.fetchall()
        cursor.close()
        return posts

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
    
    def add_comment(data):
        print(data)
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "INSERT INTO comment(post_id, user_id, comment_body) VALUES (%s,%s, %s)"
        cursor.execute(sql,data)
        mysql.connection.commit()
        
    def fetch_all_comment_ids():
        cursor = mysql.connection.cursor()
        sql = "SELECT post_id FROM comment"
        cursor.execute(sql)
        content = cursor.fetchall()
        comment_ids = [comment[0] for comment in content]
        cursor.close()
        return comment_ids
    
    def fetch_all_comment_in_post(post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT user.id, user.fullname, user.username, user.profilepic, comment.comment_id, comment.comment_body, comment.comment_time FROM user JOIN comment ON user.id = comment.user_id WHERE comment.post_id = %s ORDER BY comment.comment_time DESC"
        cursor.execute(sql, post_id)
        content = cursor.fetchall()

        cursor.close()
        return content
    
    def edit_comment(data):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            print(data)
            update = "UPDATE comment SET comment_body = %s WHERE comment_id = %s AND user_id = %s"
            cursor.execute(update,data)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
    
    def delete_comment(data):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            print(data)
            delete = "DELETE FROM comment WHERE comment_id = %s AND user_id = %s"
            cursor.execute(delete,data)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
            
    @classmethod
    def fetch_ALL_content(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT post_url.url, post_url.post_id, post_url.type FROM post JOIN post_url ON post.id = post_url.post_id;"
            cursor.execute(sql)
            data = cursor.fetchall()

            cursor.close()
            return data

        except Exception as e:
            print(f"Error fetching all content: {e}")

        finally:
            if mysql.connection.is_connected():
                cursor.close()

    @classmethod
    def search_posts(cls, current_user_id, query, cuisine, meal_type, index, limit):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql_query = f'''
            SELECT post.id, post.user_id, post.date, post.title, post.caption, post.ingredients,
            post.tag, post.subtags, post.likes, user.profilepic, user.username, user.fullname,
            GROUP_CONCAT(post_url.url) AS grouped_urls,
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM like_post AS lp 
                    WHERE lp.liker_id = {current_user_id}
                    AND lp.post_id = post.id
                ) THEN 1
                ELSE 0
            END AS liked,
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM save_post AS sp 
                    WHERE sp.saver_id = {current_user_id}
                    AND sp.post_id = post.id
                ) THEN 1
                ELSE 0
            END AS saved,
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM follow
                    WHERE follow.follower = {current_user_id}
                    AND follow.following = post.user_id
                ) THEN 1
                ELSE 0
            END AS followed,
            (   
                SELECT COUNT(*) 
                FROM comment
                WHERE comment.post_id = post.id
            ) AS comments
            FROM post JOIN post_url ON post.id = post_url.post_id
            JOIN user ON user.id = post.user_id WHERE '''

            if query:
                sql_query += "(LOWER(title) LIKE %s OR LOWER(ingredients) LIKE %s OR LOWER(tag) LIKE %s OR LOWER(subtags) LIKE %s) AND "

            if cuisine:
                placeholders = ', '.join(['%s'] * len(cuisine))
                sql_query += f"(tag IN ({placeholders})) AND "

            if meal_type:
                subtags_condition = " OR ".join(["FIND_IN_SET(%s, subtags) > 0"] * len(meal_type))
                sql_query += f"({subtags_condition}) AND "

            if sql_query.endswith("AND "):
                sql_query = sql_query[:-4]

            sql_query += f'''GROUP BY post.id, post.user_id, post.date, post.title, post.caption, post.ingredients,
            post.tag, post.subtags, post.likes, user.profilepic, user.username, user.fullname LIMIT {limit} OFFSET {index}'''
            print(sql_query)
            query_with_wildcards = f"%{query.lower()}%"

            cursor.execute(sql_query, (query_with_wildcards, query_with_wildcards, query_with_wildcards, query_with_wildcards, *cuisine, *meal_type))

            results = cursor.fetchall()

            return results

        except Exception as e:
            print(f"Error: {e}")

        finally:
            if mysql.connection.is_connected():
                cursor.close()
                
    
    @classmethod
    def search_users(cls, query, current_user_id, index, limit):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = """SELECT user.id, user.username, user.fullname, user.profilepic, COUNT(follower.id) AS followers_count, 
                EXISTS(SELECT 1 FROM follow WHERE follower = %s AND following = user.id) AS is_following
                FROM user LEFT JOIN follow AS follower ON user.id = follower.following WHERE user.username 
                LIKE %s OR user.fullname LIKE %s 
                GROUP BY user.id, user.username, user.fullname, user.profilepic
                ORDER BY user.username"""
        
        sql += f" LIMIT {limit} OFFSET {index};"
        
        print(sql)
        cursor.execute(sql, (current_user_id, f"%{query}%", f"%{query}%"))
        users = cursor.fetchall()
        cursor.close()
        return users
                
    @classmethod
    def fetch_random_posts(cls, num_of_suggestions, user_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT post.id AS post_id, post.title, post_url.type, post_url.url FROM post JOIN post_url ON post.id = post_url.post_id WHERE post.user_id != %s ORDER BY RAND() LIMIT %s;"
        cursor.execute(sql, (user_id, num_of_suggestions))
        data = cursor.fetchall()
        cursor.close()
        return data
        
    def get_post_id_from_comment_id(self, comment_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT comment.post_id, post.user_id FROM comment JOIN post ON comment.post_id = post.id WHERE comment.comment_id = %s;"
        cursor.execute(sql, (comment_id,))
        comment = cursor.fetchone()
        cursor.close()
        return comment if comment else None
    

    def add_notification(self, notifier, notifying, post_id, type):
        if notifier == notifying:
            return
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "INSERT INTO notification (notifier, notifying, type, post_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (notifier, notifying, type, post_id))
        mysql.connection.commit()
        cursor.close()

    def add_notification_post(self, notifier, notifying, post_id, type='POST'):
        self.add_notification(notifier, notifying, post_id, type)

    def add_notification_like(self, notifier, notifying, post_id, type='LIKE'):
        self.add_notification(notifier, notifying, post_id, type)

    def add_notification_save(self, notifier, notifying, post_id, type='SAVE'):
        self.add_notification(notifier, notifying, post_id, type)

    def add_notification_comment(self, notifier, notifying, post_id, type='COMMENT'):
        self.add_notification(notifier, notifying, post_id, type)

    def add_notification_follow(self, notifier, notifying, post_id=None, type='FOLLOW'):
        self.add_notification(notifier, notifying, post_id, type)


        
    def remove_notification_like(notifier, notifying, post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "DELETE FROM notification WHERE notifier = %s AND notifying = %s AND post_id = %s AND type = 'LIKE'"
        cursor.execute(sql, (notifier, notifying, post_id))
        mysql.connection.commit()
        cursor.close()

    def remove_notification_follow(notifier, notifying):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "DELETE FROM notification WHERE notifier = %s AND notifying = %s AND type = 'FOLLOW'"
        cursor.execute(sql, (notifier, notifying))
        mysql.connection.commit()
        cursor.close()

    def remove_notification_save(notifier, notifying, post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "DELETE FROM notification WHERE notifier = %s AND notifying = %s AND post_id = %s AND type = 'SAVE'"
        cursor.execute(sql, (notifier, notifying, post_id))
        mysql.connection.commit()
        cursor.close()
        
    def remove_notification_comment(notifier, notifying, post_id):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "DELETE FROM notification WHERE notifier = %s AND notifying = %s AND post_id = %s AND type = 'COMMENT'"
        cursor.execute(sql, (notifier, notifying, post_id))
        mysql.connection.commit()
        cursor.close()
        
    @classmethod
    def get_notification_post(cls, id, type=None):
        cursor = mysql.connection.cursor(dictionary=True)
        if type:
            sql = "SELECT notification.id, notification.notifying, notification.type, notification.post_id, notification.created_at, notification.is_read, user.fullname FROM notification JOIN user ON notification.notifier = user.id WHERE notification.notifying = %s AND notification.type = %s ORDER BY notification.is_read ASC, notification.created_at DESC"
            cursor.execute(sql, (id, type))
        else:
            sql = "SELECT notification.id, notification.notifying, notification.type, notification.post_id, notification.created_at, notification.is_read, user.fullname FROM notification JOIN user ON notification.notifier = user.id WHERE notification.notifying = %s ORDER BY notification.is_read ASC, notification.created_at DESC"
            cursor.execute(sql, (id,))
        
        notif = cursor.fetchall()
        cursor.close()
        return notif
    
    def update_read_notification(notifid):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "UPDATE notification SET is_read = True WHERE notification.id=%s"
        cursor.execute(sql, (notifid,))
        mysql.connection.commit()
        sql = "SELECT notification.post_id,notification.type,notification.notifier FROM notification WHERE notification.id=%s"
        cursor.execute(sql, (notifid,))
        post_id = cursor.fetchone()
        cursor.close()
        return post_id
