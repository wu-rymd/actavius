from passlib.hash import sha256_crypt
import sqlite3
import os

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def register(username, password, name):
    '''This function adds the user to the database.
    If username already exists, returns false. Otherwise, the function inserts a row in users and returns true.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    data = c.execute("SELECT * FROM students;")
    for row in data:
        if username == row[2]:
            return False
    params = (username, sha256_crypt.hash(password), name)
    c.execute("INSERT INTO students (username, password, name) VALUES (?, ?, ?)", params)

    db.commit()
    db.close()
    return True

def authenticate(username, password):
    '''This function checks user login. If username and encrypted password match, the function returns true. The function returns false otherwise.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    data = c.execute("SELECT * FROM students")
    for row in data:
        if row[2] == username and sha256_crypt.verify(password, row[3]):
            db.close()
            return True
    db.close()
    return False

def get_name_from_username(username):
    """This function returns the name of the user from the given username. Returns False if username not found, returns name otherwise."""
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    data = c.execute("SELECT * FROM students WHERE username=?", [username])
    for row in data:
        return row[1]
    return False
