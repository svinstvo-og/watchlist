from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Optional: explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(32), unique=False, nullable=False)