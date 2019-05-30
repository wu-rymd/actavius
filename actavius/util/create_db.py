import sqlite3
import os

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def setup():
    """Creates the table the following tables if they do not already exist:
    students
        id         INTEGER PRIMARY KEY AUTOINCREMENT
        name       TEXT NOT NULL
        username   TEXT NOT NULL UNIQUE
        password   TEXT NOT NULL
    colleges
        id               INTEGER PRIMARY KEY AUTOINCREMENT
        name             TEXT NOT NULL
        deadline         TEXT NOT NULL
        submitted        BOOLEAN NOT NULL
        additional_info  STRING
        student_id       INTEGER NOT NULL
        rank             INTEGER UNIQUE
    questions
        id          INTEGER PRIMARY KEY AUTOINCREMENT
        question    TEXT
        answer      TEXT
        college_id  INTEGER NOT NULL
        user_id     INTEGER NOT NULL
    extra_todo
        id          INTEGER PRIMARY KEY AUTOINCREMENT
        task        TEXT NOT NULL
        deadline    TEXT NOT NULL
        completed   BOOLEAN NOT NULL
        college_id  INTEGER NOT NULL
    finaids
        id           INTEGER PRIMARY KEY AUTOINCREMENT
        description  TEXT NOT NULL
        deadline     TEXT NOT NULL
        completed    BOOLEAN NOT NULL
        college_id   INTEGER NOT NULL
    """

    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS colleges (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, deadline TEXT NOT NULL, submitted BOOLEAN NOT NULL, additional_info STRING, student_id INTEGER NOT NULL, rank INTEGER UNIQUE)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, college_id INTEGER NOT NULL, user_id INTEGER NOT NULL)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS extra_todo (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, deadline TEXT NOT NULL, completed BOOLEAN NOT NULL, college_id INTEGER NOT NULL, student_id INTEGER NOT NULL)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS finaids (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, deadline TEXT NOT NULL, completed BOOLEAN NOT NULL, college_id INTEGER NOT NULL)"
    c.execute(command)
    db.commit()
    db.close()
