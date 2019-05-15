import sqlite3
import os

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
