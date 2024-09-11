from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Show

views = Blueprint('views', __name__) 

@views.route('/')
def home():
    if current_user.is_authenticated:
        user_shows = Show.query.filter_by(user_id=current_user.id).all()
        return render_template('home.html', shows=user_shows)
    else:
        return render_template('home_to_login.html')
    
@views.route('/add_show', methods = ['POST'])
@login_required
def add_show():
    title = request.form.get('title')
    status = request.form.get('status')
    description = request.form.get('description')

    if title and status:
        new_show = Show(
            title=title,
            status=status,
            description=description,
            user_id=current_user.id
        )
        db.session.add(new_show)
        db.session.commit()
        flash('Show added successfully!', 'success')
    else:
        flash('Please fill in all required fields.', 'error')

    return redirect(url_for('views.home'))

@views.route('/delete_show/<int:show_id>', methods = ['POST'])
@login_required
def delete_show(show_id):
    show_to_delete = Show.query.get_or_404(show_id)
    
    if show_to_delete.user_id != current_user.id:
        flash('You do not have permission to delete this show.', category='error')
        return redirect(url_for('views.home'))

    db.session.delete(show_to_delete)
    db.session.commit()
    flash('Show deleted successfully!', category='success')
    return redirect(url_for('views.home'))

#TEMP
@views.route('/check_shows')
def check_shows():
    shows = Show.query.all()
    return str([show.title for show in shows])