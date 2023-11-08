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
    profilepic VARCHAR(255),
    coverpic VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS post (
	id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    content LONGBLOB,
    title VARCHAR(255),
    caption TEXT,
    ingredients TEXT,
    instructions TEXT,
    tag VARCHAR(99)
);
