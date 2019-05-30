import sqlite3
import os

from . import colleges

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def add_todo(task, deadline, college_id,student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (task, deadline, 0, college_id,student_id)
    command = "INSERT INTO extra_todo (task, deadline, completed, college_id, student_id) VALUES (?, ?, ?, ?, ?)"
    c.execute(command, params)
    db.commit()
    db.close()

def get_college_todos(college_id):
    '''Get all of the todos from a specific college that is linked to a user'''
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
    params = (user_id,)
    command = "SELECT * FROM extra_todo WHERE student_id = ?"
    data = c.execute(command,params)
    all_todos = []
    for todo in data:
        todo_dict = {"id":todo[0],"task":todo[1],"deadline":todo[2],"completed":todo[3]}
        if todo[4] == -1:
            todo_dict["college_name"] = "All Colleges"
        else:
            todo_dict["college_name"] = colleges.get_college_from_database_id(todo[4])[1]
        all_todos.append(todo_dict)
    db.close()
    return all_todos

def delete_todo(todo_id):
    '''delete a specific todo'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (todo_id,)
    command = "DELETE FROM extra_todo WHERE id = ?"
    data = c.execute(command,params)
    db.commit()
    db.close()

def delete_college_todo(college_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (college_id,)
    command = "DELETE FROM extra_todo WHERE college_id = ?"
    data = c.execute(command,params)
    db.commit()
    db.close()
    return True
