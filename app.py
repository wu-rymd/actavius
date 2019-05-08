import sqlite3   #enable control of an sqlite database
from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
