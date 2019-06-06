import sqlite3 #stdlib
import os #stdlib
import csv, json

from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash #pip install flask

from .util import create_db, database, drafts, colleges, todo, students

# TODO: check for EACH return render_template ... loggedIn=True, username=session['username'], name=session['name'] ... passed as arg!

app = Flask(__name__)
app.secret_key = "my-super-secret-key-aAS89ayg98asfhigqeu8EGE" #static to solve logout bug

def todo_key(a):
    a = [int(x) for x in a['deadline'].split("-")]
    return a[0]*10000 + a[1]*100 + a[2]


@app.route("/", methods=["GET","POST"])
def index():
    if 'username' in session: #if logged in:
        user_id = students.get_user_id_from_username(session['username'])
        if request.method == "POST":
            if request.form.get("college"):
                college_id = request.form.get("college")
                task = request.form.get("task")
                deadline = request.form.get("deadline")
                todo.add_todo(task,deadline,college_id,user_id)
            elif request.form.get("college_edit"):
                college_id = request.form.get("college_edit")
                new_deadline = request.form.get("deadline")
                colleges.edit_deadline(college_id,new_deadline)
            elif request.form.get("is_todo"):
                if request.form.get("is_todo") == "True":
                    todo.toggle_complete(request.form.get('id'),request.form.get('new_status'))
                else:
                    colleges.toggle_complete(request.form.get('id'),request.form.get('new_status'))
            else:
                delete_this = request.form.get("delete")
                if delete_this.count("delete_todo") > 0:
                    todo.delete_todo(int(delete_this.split("delete_todo")[1]))
        all_todos = todo.get_user_todos(user_id)
        for a_todo in all_todos:
            a_todo['is_todo'] = True
            if a_todo["college_name"] == "All Colleges":
                a_todo['unitid'] = -1
            else:
                a_todo['unitid'] = colleges.get_id_from_college_name(a_todo['college_name'])
        college_todo = colleges.get_student_colleges(user_id)
        college_names = [[x[0],x[1],x[2]] for x in college_todo]
        college_dict = []
        for college in college_todo:
            temp = {}
            temp['id'] = college[0]
            temp['college_name'] = college[1]
            temp['deadline'] = college[2]
            temp['completed'] = college[3]
            temp['unitid'] = colleges.get_id_from_college_name(college[1])
            temp['task'] = "Application Deadline"
            temp['is_todo'] = False
            college_dict.append(temp)
        all_todos += college_dict
        completed = list(filter(lambda x: x['completed'] == 1,all_todos))
        not_completed = list(filter(lambda x: x['completed'] == 0,all_todos))
        completed.sort(key = todo_key)
        not_completed.sort(key = todo_key)
        all_todos = not_completed + completed
        return render_template("index.html", loggedIn=True, username=session['username'], name=session['name'], all_todos = all_todos, all_colleges=college_names)
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
        for draft in drafts_list:
            college_id = draft['college']
            college_name = colleges.get_college_from_id(college_id)
            if not college_name:
                college_name = ""
            draft['college'] = college_name
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
        #get colleges
        my_student_id = database.get_id_from_username(session['username'])
        my_colleges = colleges.get_student_colleges(my_student_id)
        college_ids = []
        for college in my_colleges:
            college_ids.append( int(colleges.get_id_from_college_name(college[1])) )
        return render_template("draft_view.html", content=content, loggedIn=True, username=session['username'], name=session['name'], colleges=my_colleges, college_ids=college_ids)
    else: #POST request
        question = request.form['question']
        answer = request.form['answer']
        college_id = request.form.get('college-id')
        if not college_id: college_id = -1
        drafts.save(draft_id, question, answer, college_id)
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

@app.route("/profile", methods=['GET','POST'])
def profile():
    if 'username' not in session:
        flash("You must be logged in to view that page!", "danger")
        return redirect(url_for('login'))
    elif request.method == 'GET':
        student_id = database.get_id_from_username(session['username'])
        data = colleges.get_student_colleges(student_id)
        college_names = []
        for college in data:
            college_names.append((college[1], colleges.get_id_from_college_name(college[1])))
        return render_template("profile.html", loggedIn=True, username=session['username'], name=session['name'], all_colleges=college_names)
    else: # POST method
        delete_form = request.form.get('delete')
        college_id = delete_form[delete_form.find(" ")+1:]
        college_name = colleges.get_college_from_id(college_id)
        student_id = database.get_id_from_username(session['username'])
        if colleges.remove_colleges(college_name, student_id):
            todo.delete_college_todo(college_id)
            flash("This college has been removed from your list!", "success")
            return redirect(url_for('profile'))
        else:
            flash("You cannot remove the same college twice!", "danger")
            return redirect(url_for('profile'))

@app.route("/fin_aid")
def fin_aid():
    if 'username' not in session:
        flash("You must be logged in to view that page!", "danger")
        return redirect(url_for('login'))
    return render_template('finaid.html', loggedIn=True, username=session['username'], name=session['name'])

@app.route("/college-api")
def api():
    DIR = os.path.dirname(__file__) or '.' # points to Flask root
    JSON_LINK = DIR + "/data/colleges.json"
    f = json.load(open(JSON_LINK,'r'))
    query = request.args.get('query') # will not return KeyError if no query in URL
    if not query: # if no parameter w/ key 'query' ... good for '' too!
        return jsonify(f)
    # reach here: query exists, build new JSON...
    query_words = query.lower().split() #split by whitespace chars
    if 'university' in query_words: query_words.remove('university')
    if 'of' in query_words: query_words.remove('of')
    if 'at' in query_words: query_words.remove('at')
    if 'college' in query_words: query_words.remove('college')
    f.pop('id', None) #remove ID to college name conversion
    search_matching_names = []
    for name in f['college_names']:
        for word in query_words:
            if word in name.lower():
                search_matching_names.append(name)
                break
    results_dict = { "college_names":[] , "id":{} , "names":{} }
    for name in search_matching_names:
        results_dict["college_names"].append(name)
        results_dict["id"][ f["names"][name] ] = name
        results_dict["names"][name] = f["names"][name]
    return jsonify(results_dict)

@app.route("/college/<int:college_id>", methods=['GET','POST'])
def college(college_id):
    if 'username' in session: loggedIn = True
    else: loggedIn = False
    college_name = colleges.get_college_from_id(college_id)

    if not college_name: #returned False b/c KeyError -- malformed id
        flash("Our database has no information on this college.", "danger")
        return redirect(url_for('index'))
    if request.method == 'GET':
        college_data = colleges.get_info_from_college_name(college_name)
        finaid_data = colleges.get_finaid_from_college_name(college_name)
        if not college_data:
            flash("Invalid college ID", "danger")
            return redirect(url_for('index'))
        shown_keys = ['ADM2017.ACT Composite 25th percentile score', 'ADM2017.ACT Composite 75th percentile score', 'ADM2017.SAT Evidence-Based Reading and Writing 25th percentile score', 'ADM2017.SAT Evidence-Based Reading and Writing 75th percentile score', 'ADM2017.SAT Math 25th percentile score', 'ADM2017.SAT Math 75th percentile score', 'DRVGR2017.Graduation rate, total cohort', 'DRVIC2017.Tuition and fees, 2017-18', "ADM2017.Admissions total", 'ADM2017.Applicants total']
        counter = 0
        check_these_keys = ['ADM2017.ACT Composite 25th percentile score', 'ADM2017.ACT Composite 75th percentile score','ADM2017.SAT Evidence-Based Reading and Writing 25th percentile score', 'ADM2017.SAT Evidence-Based Reading and Writing 75th percentile score', 'ADM2017.SAT Math 25th percentile score','ADM2017.SAT Math 75th percentile score', 'DRVGR2017.Graduation rate, total cohort',  'DRVIC2017.Tuition and fees, 2017-18', "ADM2017.Admissions total", 'ADM2017.Applicants total' ]
        for key in check_these_keys:
            if college_data[key] == "":
                counter += 1
        for key in finaid_data.keys():
            if finaid_data[key] == "":
                counter += 1
        if counter > 0:
            flash("There is not enough data in our database for this college!", "warning")
        act_25 = college_data['ADM2017.ACT Composite 25th percentile score']
        act_75 = college_data['ADM2017.ACT Composite 75th percentile score']
        sat_eng_25 = college_data['ADM2017.SAT Evidence-Based Reading and Writing 25th percentile score']
        sat_eng_75 = college_data['ADM2017.SAT Evidence-Based Reading and Writing 75th percentile score']
        sat_math_25 = college_data['ADM2017.SAT Math 25th percentile score']
        sat_math_75 = college_data['ADM2017.SAT Math 75th percentile score']
        grad_rate = college_data['DRVGR2017.Graduation rate, total cohort']
        tuition = college_data['DRVIC2017.Tuition and fees, 2017-18']
        admit = college_data["ADM2017.Admissions total"]
        apply = college_data['ADM2017.Applicants total']
        tuition = str(tuition)
        for key in finaid_data.keys():
            try:
                x = int(finaid_data[key])
                finaid_data[key] = finaid_data[key][:-3] + ',' + finaid_data[key][-3:]
            except:
                continue
        if len(tuition) > 0:
            tuition = tuition[:-3] + ',' + tuition[-3:]
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
                                   finaid = finaid_data,
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
                                   finaid = finaid_data,
                                   loggedIn = loggedIn )
    else: #POST request
        student_id = database.get_id_from_username(session['username'])
        data = colleges.get_student_colleges(student_id)
        add_a_college = True
        for row in data:
            if college_name == row[1]:
                add_a_college = False
                break
        if add_a_college:
            deadline = request.form['deadline']
            # submitted = request.form['submitted']
            submitted = False
            if colleges.add_colleges(college_name, deadline, submitted, student_id):
                flash("This college has been added to your list!", "success")
                return redirect(url_for('college', college_id=college_id))
            else:
                flash("You cannot add the same college twice!", "danger")
                return redirect(url_for('college', college_id=college_id))
        else:
            todo.delete_college_todo(colleges.get_college_database_id_from_college_name_and_student_id(college_name,student_id)[0][0])
            if colleges.remove_colleges(college_name, student_id):
                flash("This college has been removed from your list!", "success")
                return redirect(url_for('college', college_id=college_id))
            else:
                flash("You cannot remove the same college twice!", "danger")
                return redirect(url_for('college', college_id=college_id))

create_db.setup() #outside b/c .wsgi not run file
            
if __name__ == "__main__":
    app.debug = True
    print("creating the db")
    app.run()
