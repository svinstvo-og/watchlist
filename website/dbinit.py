# create_db.py
from __init__ import create_app, db
from models import User

app = create_app()

print()

'''with app.app_context():
    db.create_all()
    print("Database tables created successfully.")'''