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

def get_college_todos(college_id):
    '''Get all fo the todos from a specific college that is linked to a user'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (college_id,)
    command = "SELECT * FROM extra_todo WHERE college_id = ?"
    data = c.execute(command,params)
    return data


def get_user_todos(user_id):
    '''Get all of the todos of the users based on their id'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    user_colleges = colleges.get_student_colleges(user_id)
    all_todos = []
    for college in user_colleges:
        for todo in get_college_todos(college[0]):
            all_todos.append({"id":todo[0],"task":todo[1],"deadline":todo[2],"completed":todo[3],"college_name":colleges.get_college_from_database_id(todo[4])[1]})
    db.close()
    return all_todos
