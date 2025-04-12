from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()  # Initialize the db object here
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize db with the app instance
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'

    # Register Blueprints
    from app.routes import main
    app.register_blueprint(main, template_folder='templates')


    return app

# This loads the user based on the user ID
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import inside the function to avoid circular import
    return User.query.get(int(user_id))
