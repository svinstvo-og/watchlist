from . import db, create_app

class User(db.Model):
    __tablename__ = 'users'  # Optional: explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(32), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'