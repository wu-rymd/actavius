import sqlite3
import os

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def add_colleges(college, deadline, submitted, student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (college, deadline, submitted, student_id)
    command = "INSERT INTO colleges (name, deadline, submitted, student_id) VALUES (?, ?, ?, ?)"
    c.execute(command, params)
    db.commit()
    db.close()

def remove_colleges(college, student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    command = "DELETE FROM colleges WHERE student_id = {} AND name = {}".format(student_id, repr(college))
    c.execute(command)
    db.commit()
    db.close()

def get_student_colleges(student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    command = "SELECT name, deadline, submitted, additional_info from colleges WHERE student_id ={}".format(student_id)
    c.execute(command)
    data = c.fetchall()
    db.close()
    return data
