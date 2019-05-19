import sqlite3
import os

from util import colleges

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def add_todo(task, deadline, completed, college_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (task, deadline, completed, college_id)
    command = "INSERT INTO extra_todo (task, deadline, completed, college_id) VALUES (?, ?, ?, ?)"
    c.execute(command, params)
    db.commit()
    db.close()

def get_user_todos(user_id):
    '''Get all of the todos of the users based on their id'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    user_colleges = colleges.get_student_colleges(user_id)
    for college in user_colleges:
        print("hi")
    db.close()
    return "hi"
