import sqlite3
import os
from passlib.hash import sha256_crypt

DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def setup():
    """Creates the table the following tables if they do not already exist:
    student
        id         INTEGER PRIMARY KEY AUTOINCREMENT
        name       TEXT NOT NULL
        interests  TEXT
        username   TEXT NOT NULL UNIQUE
        password   TEXT NOT NULL
    college
        id               INTEGER PRIMARY KEY AUTOINCREMENT
        name             TEXT NOT NULL
        deadline         TEXT NOT NULL
        financial_aid    STRING NOT NULL
        submitted        BOOLEAN NOT NULL
        additional_info  STRING
        student_id       INTEGER NOT NULL
    questions
        id          INTEGER PRIMARY KEY AUTOINCREMENT
        question    TEXT NOT NULL
        answer      TEXT
        college_id  INTEGER NOT NULL
    extra_todo
        id          INTEGER PRIMARY KEY AUTOINCREMENT
        task        TEXT NOT NULL
        deadline    TEXT NOT NULL
        completed   BOOLEAN NOT NULL
        student_id  INTEGER NOT NULL
    """

    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, interests TEXT, username TEXT NOT NULL, password TEXT NOT NULL)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS college (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, deadline TEXT NOT NULL, financial_aid STRING NOT NULL, submitted BOOLEAN NOT NULL, additional_info STRING, student_id INTEGER NOT NULL)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, answer TEXT, college_id INTEGER NOT NULL)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS extra_todo (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, deadline TEXT NOT NULL, completed BOOLEAN NOT NULL, student_id INTEGER NOT NULL)"
    c.execute(command)
    db.commit()
    db.close()

def register(username, password, name):
    '''This function adds the user to the database.
    If username already exists, returns false. Otherwise, the function inserts a row in users and returns true.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    data = c.execute("SELECT * FROM student;")
    for row in data:
        if username == row[2]:
            return False
    params = (username, sha256_crypt.hash(password), name)
    c.execute("INSERT INTO student (username, password, name) VALUES (?, ?, ?)", params)

    db.commit()
    db.close()
    return True

def authenticate(username, password):
    '''This function checks user login. If username and encrypted password match, the function returns true. The function returns false otherwise.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    data = c.execute("SELECT * FROM student")
    for row in data:
        if row[3] == username and sha256_crypt.verify(password, row[4]):
            db.close()
            return True
    db.close()
    return False
