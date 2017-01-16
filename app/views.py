# -*- coding: utf-8 -*-

from app import app
import db
import time
from flask import render_template, redirect, session, request
from functools import wraps

def login_required(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if not session.get('user', None):
            return redirect('/login')
        return func(*args, **kwargs)
    return func_wrapper

def getFields():
    fopen = open('app/static/fields.csv', 'r')
    fields = []
    content = fopen.read()  

    for row in content.split("\n")[:-1]:
        fields.append(row.split(','))

    fopen.close()

    return fields

def checkFields(fieldsToCheck):
    fopen = open('app/static/fields.csv', 'r')
    correctFields = fopen.read().split("\n")[:-1] 

    isFormCorrect = True

    for cor_field in correctFields:
        check_field = fieldsToCheck.get(cor_field.split(',')[0], None) 
        print "CheckF: {0} == CorrectF: {1}".format(check_field, cor_field.split(',')[1])
        if not check_field or check_field != cor_field.split(',')[1]:
            isFormCorrect = False
            break

    return isFormCorrect


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/users/<userId>')
def get_user(userId):
    userTries = db.getUserTries(userId) 
    user = db.getUser(userId)

    context = {
        "user": user,  
        "tries": userTries
    }

    return render_template('user_detail.html', context=context)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session and session['user'] is not None:
            # Proceed to prova
            return redirect('/prova')
        else:
            return render_template('login.html')

    if request.method == "POST":

        login = {} 

        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if email and password:
            # Look for this user in the db
            user = db.loginUser(email, password)

            if user:
                session['user'] = user
                return redirect('/prova')
            else:
                login['login_error'] = 'user_not_found'
        else:
            login['login_error'] = 'no_credential_provided'

        return render_template('login.html', context=login)

@app.route('/logout')
def logout():
    if session['user']:
        session.pop('user', None)
        return redirect('/login')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email', None)
    name = request.form.get('name', None)
    pwd = request.form.get('password', None)
    rep_pwd = request.form.get('repeat_password', None)

    if not (name and email):
        context['signup_error'] = 'no_name_or_email_provided'
    else:
        if pwd and rep_pwd:
            if pwd != rep_pwd:
                context['signup_error'] = 'password_mismatch'
            else:
                # User is correct! Create it
                db.insertUser(name, email, pwd)
                # User is correct! Login it
                user = db.loginUser(email, pwd)
                if user:
                    session['user'] = user
                    return redirect('/prova')
        else:
            context['signup_error'] = 'no_pass_provided'

    return render_template('login.html', context=context)

@app.route('/prova')
@login_required
def get_prova():
    fields = getFields()

    return render_template('prova.html', context=fields)

@app.route('/register-try', methods=['POST'])
@login_required
def register_try():
    if checkFields(request.form) and request.form['time-elapsed']:
        # Add this try to the DB
        db.insertTry(request.form['time-elapsed'], 
                     time.strftime("%d/%m/%yT%H:%M:%S"),
                     session['user']['id'])
        context = {
            "success": True,
            "time": request.form['time-elapsed']
        } 
        
        return render_template('try-success.html', context=context)

    else:
        context = {
            "success": False,
            "error": "Some fields are missing or wrong! Try again!"
        } 

        return render_template('try-success.html', context=context)

@app.route('/ranking')
def get_ranking():
    ranking = db.getRanking()

    return render_template('ranking.html', context=ranking) 
