import sqlite3   #enable control of an sqlite database
from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import urandom

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
    app.run()
