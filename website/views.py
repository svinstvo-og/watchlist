from flask import Blueprint, render_template

views = Blueprint('views', __name__) 

@views.route('/')
def libriary():
    return render_template('libriary.html')