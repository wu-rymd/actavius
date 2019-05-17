import sqlite3
import os, json

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
    params = (student_id,repr(college))
    command = "DELETE FROM colleges WHERE student_id = ? AND name = ?"
    c.execute(command, params)
    db.commit()
    db.close()

def get_student_colleges(student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (student_id,)
    command = "SELECT name, deadline, submitted, additional_info from colleges WHERE student_id =?"
    c.execute(command,params)
    data = c.fetchall()
    db.close()
    return data

def get_college_from_id(college_id):
    id_converter = json.loads(open('data/colleges.json','r').read())['id']
    return id_converter[str(college_id)]

def get_id_from_college_name(college_name):
    name_converter = json.loads(open('data/colleges.json','r').read())['name']
    return name_converter[str(college_name)]
