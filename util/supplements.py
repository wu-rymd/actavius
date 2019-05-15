import sqlite3
import os

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def add_supplement_question(question, college_id):
    '''This function adds a question to the database.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (question, college_id, "")
    c.execute("INSERT INTO questions (question, college_id, answer) VALUES (?, ?, ?)", params)

    db.commit()
    db.close()

def edit_answer(question_id, new_answer):
    '''This function changes the answer to a question.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (new_answer,question_id)
    c.execute("UPDATE questions SET answer = ? WHERE id = ? ", params)
    db.commit()
    db.close()

def edit_question(question_id, new_question):
    '''This function changes the question.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (new_question,question_id)
    c.execute("UPDATE questions SET question = ? WHERE id = ? ", params)

    db.commit()
    db.close()

def remove_question(question_id):
    '''This function removes the question.'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (question_id,)
    data = c.execute("DELETE FROM questions WHERE id = ?", params)
    db.close()

def get_question(question_id):
    '''This function returns the question, and answer given an id'''
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (question_id,)
    data = c.execute("SELECT * FROM questions WHERE id = ?", params)
    output = {}
    for row in data:
        output['id'] = row[0]
        output['question'] = row[1]
        output['answer'] = row[2]
        output['college_id'] = row[3]
    db.close()
    return output
