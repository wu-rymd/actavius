import sqlite3
import os, json

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def add_colleges(college, deadline, submitted, student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    data = c.execute("SELECT * FROM colleges;")
    for row in data:
        if college == row[1] and student_id == row[5]:
            return False
    params = (college, deadline, submitted, student_id)
    command = "INSERT INTO colleges (name, deadline, submitted, student_id) VALUES (?, ?, ?, ?)"
    c.execute(command, params)
    db.commit()
    db.close()
    return True

def remove_colleges(college, student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (student_id,repr(college))
    command = "DELETE FROM colleges WHERE student_id = ? AND name = ?"
    c.execute(command, params)
    db.commit()
    db.close()
    return True

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
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root
        
    FILE_LINK = DIR + "data/college_data.json"

    id_converter = json.loads(open(FILE_LINK,'r').read())
    # ids = {id_converter['id'][k] for k in id_converter['id'].keys()}
    # colleges = {k for k in id_converter['names'].keys()}
    # diff = colleges.difference(ids)
    # print(len(diff))
    return id_converter['id'][str(college_id)]

# get_college_from_id(101602)

def get_info_from_college_name(college_name):
    # for scalability/hosting on Apache server
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root

    FILE_LINK = DIR + "data/college_data.json"

    f = open(FILE_LINK, 'r').read()
    college_data = json.loads(f)[college_name]
    return college_data
