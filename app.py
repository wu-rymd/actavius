import sqlite3 #stdlib
from os import urandom #stdlib

from flask import Flask, render_template, request, session, redirect, url_for, flash #pip install flask

from util import create_db, database


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def index():
    if 'username' in session: #if logged in:
        return render_template("index.html", loggedIn=True, username=session['username'], name=session['name'])
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/register_auth', methods = ['POST'])
def register_auth():
    '''This function checks the form on the signup page and calls register() to register the user into the database.'''
    name = request.form['name'].strip()
    username = request.form['username'].strip()
    password = request.form['password']
    confirmed_pass = request.form['confirmedPassword']
    if name == "" or username == "" or password == "":
        flash("All fields are required.", "danger")
        return redirect(url_for('register'))
    elif password != confirmed_pass: # checks to make sure two passwords entered are the same
        flash("Please make sure the passwords you enter are the same.", "danger")
        return redirect(url_for('register'))
    else:
        if database.register(username, password, name):
            flash("You have successfully registered.", "success")
        else:
            flash("There is already an account with that username.", "danger")
            return redirect(url_for('register'))
    return redirect('/login')

@app.route("/login")
def login():
    '''This function renders the HTML template for the login page.'''
    return render_template('login.html')

@app.route('/login_auth', methods = ['POST'])
def login_auth():
    '''This function calls authenticate() to check if the form's username and password match the database. If successful, this function redirects the user to the home page.'''
    username = request.form['username']
    password = request.form['password']

    if database.authenticate(username, password):
        session['username'] = username
        session['name'] = database.get_name_from_username(username)
        flash("You have successfully logged in.", "success")
        return redirect('/')
    else:
        flash("Invalid username and password combination", "danger")
        return render_template('login.html')

@app.route('/logout')
def logout():
    '''This function removes the username from the session, logging the user out. Redirects user to home page.'''
    session.pop('username') # ends session
    session.pop('name') # ends session
    flash("You have successfully logged out.", "success")
    return redirect('/')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/profile")
def profile():
    if 'username' in session: #if logged in:
        return render_template("profile.html", loggedIn=True)
    flash("Please log in to see your profile.", "warning")
    return redirect('/')

@app.route("/fin_aid")
def fin_aid():
    return render_template('finaid.html')

@app.route("/college")
def college():
    return "hi"

if __name__ == "__main__":
    app.debug = True
    create_db.setup() #setup database
    app.run()
