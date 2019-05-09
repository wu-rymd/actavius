import sqlite3 #stdlib
from os import urandom #stdlib

from flask import Flask, render_template, request, session, redirect, url_for, flash #pip install flask

from util import create_db


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return "hi"

@app.route("/login")
def register():
    return "hi"

@app.route("/search")
def register():
    return "hi"

@app.route("/user")
def register():
    return "hi"

@app.route("/financial")
def register():
    return "hi"

@app.route("/college")
def register():
    return "hi"

if __name__ == "__main__":
    app.debug = True
    create_db.setup() #setup database
    app.run()
