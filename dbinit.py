# init_db.py
from website import create_app, db
from website.models import User

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized!")