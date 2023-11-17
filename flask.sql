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
    coverpic VARCHAR(255)
);