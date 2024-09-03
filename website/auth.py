from flask import Blueprint, render_template, request
from . import db
from .models import User

auth = Blueprint('auth', __name__) 

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return 'logout'

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/submit_signup', methods=['POST'])
def submit_signup():
    username = request.form['username']
    pwd = request.form['pwd']

    new_user = User(username=username, pwd=pwd)

    db.session.add(new_user)
    db.session.commit()

    return f'Username: {username}, password: {pwd}'