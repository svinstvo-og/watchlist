from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret1'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///auth.db'

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Bind Flask-Migrate to the app and database

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager.login_view = 'auth.login'

    with app.app_context():
        # Import models here after db is initialized
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app