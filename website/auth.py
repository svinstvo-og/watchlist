from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .views import home
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__) 

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/submit_login', methods=['GET', 'POST'])
def submit_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pwd, pwd):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return home()
        else:
            flash('Login failed. Check your username and/or password.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout', methods = ['POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/submit_signup', methods=['POST', 'GET'])
def submit_signup():
    username = request.form.get('username')
    pwd = request.form.get('pwd')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists. Please choose another one.', 'error')
        return redirect(url_for('auth.signup'))

    hashed_pwd = generate_password_hash(pwd, method='pbkdf2:sha256')

    new_user = User(username=username, pwd=hashed_pwd)

    db.session.add(new_user)
    db.session.commit()

    flash('User created successfully! Please log in.', 'success')

    return redirect(url_for('auth.login'))