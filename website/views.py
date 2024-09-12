from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Show
import requests

views = Blueprint('views', __name__) 

TMDB_API_KEY = '4323ffb7f4c395731b13371f9442fb68'

@views.route('/')
def home():
    if current_user.is_authenticated:
        user_shows = Show.query.filter_by(user_id=current_user.id).all()
        return render_template('home.html', shows=user_shows)
    else:
        return render_template('home_to_login.html')

def fetch_show_data(title):
    base_url = "https://api.themoviedb.org/3/search/tv"
    
    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'language': 'en-US',
        'page': 1,
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            show = data['results'][0]
            description = show.get('overview', '')[:500]  # Get first 500 characters
            poster_path = show.get('poster_path', '')
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # Construct the poster URL
            else:
                poster_url = ''  # Default to empty string if no poster found
            
            return description, poster_url
        else:
            return None, None
    else:
        return None, None

@views.route('/add_show', methods = ['POST'])
@login_required
def add_show():
    show_title = request.form.get('show_title')
    status = request.form.get('status')

    if show_title:
        description, poster_url = fetch_show_data(show_title)
        
        new_show = Show(title=show_title, poster_url=poster_url, status=status, description=description, user_id=current_user.id)
        
        db.session.add(new_show)
        db.session.commit()
        
        flash('Show added successfully!', category='success')

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