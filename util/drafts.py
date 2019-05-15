import sqlite3
import os

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def get_all_drafts(username):
    '''This function adds the user to the database.
    If username already exists, returns false. Otherwise, the function inserts a row in users and returns true.'''
    retList = []
    
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    user_id = get_user_id_by_username(username)
    data = c.execute("SELECT * FROM questions WHERE user_id=?", [user_id])
    for row in data:
        retList.append({'id': row[0],
                        'college': row[3],
                        'question': row[1],
                        'answer': row[2], })
    db.close()
    return retList

def get_draft(username,draft_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    user_id = get_user_id_by_username(username)
    data = c.execute("SELECT * FROM questions WHERE id=?", [draft_id]).fetchone()
    # if NoneType due to no draft w/ spec. draft_id
    # OR draft_id does not belong to user...
    if not data or data[4] != user_id:
        return False

    retDict = {'id':data[0], 'question':data[1], 'answer':data[2], 'college_id':data[3]}
    db.close()
    return retDict

def save(draft_id, question, answer):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    command = c.execute("UPDATE questions SET question=? , answer=? WHERE id=?", [question, answer, draft_id])
    db.commit()
    db.close()

def create_new_draft(username):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    user_id = get_user_id_by_username(username)
    params = ("(New draft)", "", -1, user_id)
    c.execute("INSERT INTO questions (question, answer, college_id, user_id) VALUES (?, ?, ?, ?)", params)
    db.commit()
    last_row_id = c.lastrowid
    db.close()
    return last_row_id

def delete(draft_id):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    c.execute("DELETE FROM questions WHERE id=?", [draft_id])
    db.commit()
    db.close()

def get_user_id_by_username(username):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    data = c.execute("SELECT id FROM students WHERE username=?", [username]).fetchone()
    return data[0]
    db.close()

def get_dummy_drafts():
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = ("Hello?", "Hiya", 1, 1)
    c.execute("INSERT INTO questions (question, answer, college_id, user_id) VALUES (?, ?, ?, ?)", params)

    db.commit()
    db.close()
    return True
