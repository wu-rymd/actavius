import sqlite3 #stdlib
from os import urandom #stdlib
import csv, json

from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash #pip install flask

from util import create_db, database, drafts, colleges, todo, students

# TODO: check for EACH return render_template ... loggedIn=True, username=session['username'], name=session['name'] ... passed as arg!

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def index():
    if 'username' in session: #if logged in:
        user_id = students.get_user_id_from_username(session['username'])
        all_todos = todo.get_user_todos(user_id)
        return render_template("index.html", loggedIn=True, username=session['username'], name=session['name'], all_todos = all_todos)
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

@app.route("/drafting", methods=['GET','POST']) #get for just showing list, post to process new draft
def drafts_all():
    if 'username' not in session:
        flash("You must be logged in to view that page!", "danger")
        return redirect(url_for('login'))
    elif request.method == 'GET':
        drafts_list = drafts.get_all_drafts(session['username'])
        return render_template("drafts_list.html", drafts=drafts_list, loggedIn=True, username=session['username'], name=session['name'])
    else: #POST request
        new_draft_form = request.form.get('new-draft') #None if create new draft button not clicked (must be delete button)
        if not new_draft_form:
            delete_form = request.form.get('delete')
            id_to_delete = delete_form[delete_form.find("ID ")+3 :]
            drafts.delete(id_to_delete)
            flash("Draft ID " + id_to_delete + " deleted!", "success")
            return redirect(url_for('drafts_all'))
        else:
            new_id = drafts.create_new_draft(session['username'])
            flash("New draft created!", "success")
            return redirect(url_for('draft_existing', draft_id=new_id))

@app.route("/drafting/<int:draft_id>", methods=['GET','POST'])
def draft_existing(draft_id):
    if 'username' not in session:
        flash("You must be logged in to view that page!", "danger")
        return redirect(url_for('login'))
    elif request.method == 'GET':
        #make sure draft id belongs to user
        content = drafts.get_draft(session['username'], draft_id)
        if not content: #if returned False
            flash("Unauthorized access to draft!", "danger")
            return redirect(url_for('index'))
        return render_template("draft_view.html", content=content, loggedIn=True, username=session['username'], name=session['name'])
    else: #POST request
        question = request.form['question']
        answer = request.form['answer']
        drafts.save(draft_id, question, answer)
        flash("Your draft has been saved!", "success")
        return redirect(url_for('drafts_all'))

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
    if 'username' not in session:
        flash("You must be logged in to view that page!", "danger")
        return redirect(url_for('login'))
    return render_template('search.html', loggedIn=True, username=session['username'], name=session['name'])

@app.route("/profile")
def profile():
    if 'username' not in session:
        flash("You must be logged in to view that page!", "danger")
        return redirect(url_for('login'))
    return render_template("profile.html", loggedIn=True, username=session['username'], name=session['name'])

@app.route("/fin_aid")
def fin_aid():
    if 'username' not in session:
        flash("You must be logged in to view that page!", "danger")
        return redirect(url_for('login'))
    return render_template('finaid.html', loggedIn=True, username=session['username'], name=session['name'])

@app.route("/college-api")
def api():
    f = json.load(open("./data/college_data.json",'r'))
    return jsonify(f)

@app.route("/college/<int:college_id>", methods=['GET','POST'])
def college(college_id):
    if 'username' in session: loggedIn = True
    else: loggedIn = False
    college_name = colleges.get_college_from_id(college_id)
    if not college_name: #returned False b/c KeyError -- malformed id
        flash("Invalid college ID", "danger")
        return redirect(url_for('index'))
    if request.method == 'GET':
        college_data = colleges.get_info_from_college_name(college_name)
        act_25 = college_data['ADM2017.ACT Composite 25th percentile score']
        act_75 = college_data['ADM2017.ACT Composite 75th percentile score']
        sat_eng_25 = college_data['ADM2017.SAT Evidence-Based Reading and Writing 25th percentile score']
        sat_eng_75 = college_data['ADM2017.SAT Evidence-Based Reading and Writing 75th percentile score']
        sat_math_25 = college_data['ADM2017.SAT Math 25th percentile score']
        sat_math_75 = college_data['ADM2017.SAT Math 75th percentile score']
        grad_rate = college_data['DRVGR2017.Graduation rate, total cohort']
        tuition = college_data['DRVIC2017.Tuition and fees, 2017-18']
        admit = college_data['DRVIC2017.Tuition and fees, 2017-18']
        apply = college_data['ADM2017.Applicants total']
        print(college_name,act_25,act_75,sat_eng_25,sat_eng_75,sat_math_25,sat_math_75,grad_rate,tuition,admit,apply)
        if loggedIn:
            student_id = database.get_id_from_username(session['username'])
            data = colleges.get_student_colleges(student_id)
            add = True
            for row in data:
                if college_name == row[1]:
                    add = False
                    break
            return render_template("college.html",name = college_name,
                                   act_25 = act_25,
                                   act_75 = act_75,
                                   sat_eng_25 = sat_eng_25,
                                   sat_eng_75 = sat_eng_75,
                                   sat_math_25 = sat_math_25,
                                   sat_math_75 = sat_math_75,
                                   grad_rate = grad_rate,
                                   tuition = tuition,
                                   admit = admit,
                                   apply = apply,
                                   loggedIn = loggedIn,
                                   username = session['username'],
                                   add = add)
        else:
            return render_template("college.html",name = college_name,
                                   act_25 = act_25,
                                   act_75 = act_75,
                                   sat_eng_25 = sat_eng_25,
                                   sat_eng_75 = sat_eng_75,
                                   sat_math_25 = sat_math_25,
                                   sat_math_75 = sat_math_75,
                                   grad_rate = grad_rate,
                                   tuition = tuition,
                                   admit = admit,
                                   apply = apply,
                                   loggedIn = loggedIn )
    else: #POST request
        student_id = database.get_id_from_username(session['username'])
        data = colleges.get_student_colleges(student_id)
        add_a_college = True
        for row in data:
            if college_name == row[1]:
                add_a_college = False
                break
        print(add_a_college)
        if add_a_college:
            deadline = request.form['deadline']
            # submitted = request.form['submitted']
            submitted = False
            # print(name, deadline, submitted, student_id)
            if colleges.add_colleges(college_name, deadline, submitted, student_id):
                flash("This college has been added to your list!", "success")
                return redirect(url_for('college', college_id=college_id))
            else:
                flash("You cannot add the same college twice!", "danger")
                return redirect(url_for('college', college_id=college_id))
        else:
            if colleges.remove_colleges(college_name, student_id):
                flash("This college has been removed from your list!", "success")
                return redirect(url_for('college', college_id=college_id))
            else:
                flash("You cannot remove the same college twice!", "danger")
                return redirect(url_for('college', college_id=college_id))

if __name__ == "__main__":
    app.debug = True
    print("creating the db")
    create_db.setup() #setup database
    app.run()
