from flask import Blueprint, render_template, request

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

    return f'Username: {username}, password: {pwd}'