import sqlite3
import os, json

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def add_colleges(college, deadline, submitted, student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    command = c.execute("SELECT * FROM colleges;")
    data = c.fetchall()
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
    command = "DELETE FROM colleges WHERE ( student_id = {} ) AND ( name = {} )".format(student_id,repr(college))
    # c.execute(command, params)
    c.execute(command)
    db.commit()
    c.execute("SELECT * FROM colleges;")
    data = c.fetchall()
    for row in data:
        if college == row[1] and student_id == row[5]:
            return False
    db.close()
    return True

def get_college_database_id_from_college_name_and_student_id(college_name,student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (student_id,college_name)
    command = "SELECT id from colleges WHERE student_id =? AND name=?"
    c.execute(command,params)
    data = c.fetchall()
    db.close()
    return data

def get_student_colleges(student_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (student_id,)
    command = "SELECT * from colleges WHERE student_id =?"
    c.execute(command,params)
    data = c.fetchall()
    db.close()
    return data

def get_college_from_database_id(college_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (college_id,)
    command = "SELECT * from colleges WHERE id =?"
    c.execute(command,params)
    data = c.fetchone()
    db.close()
    return data

def get_college_from_id(college_id):
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root

    FILE_LINK = DIR + "data/colleges.json"
    try:
        id_converter = json.loads(open(FILE_LINK,'r').read())['id']
        return id_converter[str(college_id)]
    except KeyError:
        return False

def get_id_from_college_name(college_name):
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root

    FILE_LINK = DIR + "data/colleges.json"

    name_converter = json.loads(open(FILE_LINK,'r').read())['names']
    return name_converter[str(college_name)]

def get_info_from_college_name(college_name):
    # for scalability/hosting on Apache server
    FILE_DIR = os.path.dirname(__file__) or '.'
    FILE_DIR += '/../' # points to util, ../ to go back to Flask root

    FILE_LINK = DIR + "data/college_data.json"

    f = open(FILE_LINK, 'r').read()
    try:
        college_data = json.loads(f)[college_name]
        return college_data
    except KeyError:
        return False

def get_finaid_from_college_name(college_name):
    college_data = get_info_from_college_name(college_name)
    if not college_data:
        return False
    output = {}
    output['unitid'] = college_data['unitid']
    output['avg_grant_aid'] = college_data['SFA1617.Average amount of federal, state, local or institutional grant aid awarded']
    output['avg_federal_grant'] = college_data['SFA1617.Average amount of federal grant aid awarded to full-time first-time undergraduates']
    output['avg_pell_grant'] = college_data['SFA1617.Average amount of Pell grant aid awarded to full-time first-time undergraduates']
    output['avg_institutional_grant'] = college_data['SFA1617.Average amount of institutional grant aid awarded to full-time first-time undergraduates']
    output['avg_student_loan'] = college_data['SFA1617.Average amount of student loans awarded to full-time first-time undergraduates']
    return output

def edit_deadline(college_id,deadline):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (deadline,college_id)
    command = "UPDATE colleges SET deadline = ? WHERE id = ?"
    c.execute(command, params)
    db.commit()
    db.close()

def toggle_complete(college_id,status):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (status,college_id)
    command = "UPDATE colleges SET submitted = ? WHERE id = ?"
    c.execute(command, params)
    db.commit()
    db.close()
