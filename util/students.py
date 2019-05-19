import sqlite3
import os, json

# for scalability/hosting on Apache server
DIR = os.path.dirname(__file__) or '.'
DIR += '/../' # points to util, ../ to go back to Flask root

DATABASE_LINK = DIR + "data/database.db"

def get_user_id_from_username(username):
    db = sqlite3.connect(DATABASE_LINK)
    c = db.cursor()
    params = (username,)
    command = "SELECT id from students WHERE username =?"
    c.execute(command,params)
    data = c.fetchall()
    db.close()
    return data[0][0]
