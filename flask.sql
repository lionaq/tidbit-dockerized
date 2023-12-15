DROP DATABASE IF EXISTS `tidbit`;
CREATE DATABASE IF NOT EXISTS `tidbit`;
USE `tidbit`;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    fullname VARCHAR(255),
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    bio TEXT,
    website VARCHAR(255),
    profilepic VARCHAR(255),
    coverpic VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS post (
	id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    title VARCHAR(255),
    caption TEXT,
    ingredients TEXT,
    instructions TEXT,
    tag VARCHAR(99),
    subtags VARCHAR(255),
    likes INT NOT NULL DEFAULT '0',
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS post_url (
    id INT auto_increment PRIMARY KEY,
    url VARCHAR(255),
    post_id INT,
    type VARCHAR(10),
    FOREIGN KEY (post_id) 
        REFERENCES post(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS follow (
    id INT auto_increment PRIMARY KEY,
    follower INT,
    following INT,
    FOREIGN KEY (follower)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (following)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS like_post (
  like_id int NOT NULL AUTO_INCREMENT,
  liker_id int DEFAULT NULL,
  post_id int DEFAULT NULL,
  PRIMARY KEY (like_id),
  KEY fk2_idx (liker_id),
  KEY fk1_idx (post_id),
  CONSTRAINT like_fk1 FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT like_fk2 FOREIGN KEY (liker_id) REFERENCES user (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS save_post (
  save_id INT NOT NULL AUTO_INCREMENT,
  saver_id INT NULL,
  post_id INT NULL,
  PRIMARY KEY (save_id),
  CONSTRAINT save_fk1 FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT save_fk2 FOREIGN KEY (saver_id) REFERENCES user (id) ON DELETE CASCADE ON UPDATE CASCADE
  );

CREATE TABLE IF NOT EXISTS comment (
  comment_id int NOT NULL AUTO_INCREMENT,
  post_id int DEFAULT NULL,
  user_id int DEFAULT NULL,
  comment_body text,
  comment_time timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (comment_id),
  KEY comment_fk1_idx (post_id),
  KEY comment_fk2_idx (user_id),
  CONSTRAINT comment_fk1 FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT comment_fk2 FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS notification (
    id INT auto_increment PRIMARY KEY,
    notifier INT NOT NULL,
    notifying INT NOT NULL,
    TYPE VARCHAR(255) NOT NULL,
    post_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (notifier) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (notifying) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES post(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notification_setting (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    receive_post_notifications BOOLEAN DEFAULT TRUE,
    receive_like_notifications BOOLEAN DEFAULT TRUE,
    receive_save_notifications BOOLEAN DEFAULT TRUE,
    receive_comment_notifications BOOLEAN DEFAULT TRUE,
    receive_follow_notifications BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE
);

