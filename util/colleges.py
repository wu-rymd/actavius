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
    command = "SELECT * from colleges WHERE student_id =?"
    c.execute(command,params)
    data = c.fetchall()
    db.close()
    return data

def get_college_from_id(college_id):
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root
        
    FILE_LINK = DIR + "data/colleges.json"
    print(json.loads(open(FILE_LINK,'r').read()).keys())
    try:    
        id_converter = json.loads(open(FILE_LINK,'r').read())['id']
        return id_converter[str(college_id)]
    except KeyError:
        return False

def get_id_from_college_name(college_name):
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root
    
    FILE_LINK = DIR + "data/college_data.json"
    
    name_converter = json.loads(open(FILE_LINK,'r').read())['name']
    return name_converter[str(college_name)]

def get_info_from_college_name(college_name):
    # for scalability/hosting on Apache server
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root

    FILE_LINK = DIR + "data/college_data.json"

    f = open(FILE_LINK, 'r').read()
    college_data = json.loads(f)[college_name]
    return college_data
