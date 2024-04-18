--Creating an SQL schema to create the database 
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS questions;
--The above drops tables if they exist

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_address TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    verified BOOLEAN NOT NULL
);

--Creating a users table which will store info about users
-- id (unique id for the user) email, and password

CREATE TABLE questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    right_answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL,
    wrong_answer3 TEXT NOT NULL
);
--Created table with questions that contain the text question, right answer and 3 wrong answers
--Optimisation on datatypes tbd


