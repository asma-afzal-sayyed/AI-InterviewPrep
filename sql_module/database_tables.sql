CREATE DATABASE interviewprep;

USE interviewprep;

CREATE TABLE users(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100),
email VARCHAR(100),
password VARCHAR(100)
);

CREATE TABLE scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    score INT
);

select * from users;

CREATE TABLE leaderboard(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    score INT
);