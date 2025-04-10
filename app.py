from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Abstract, Review
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Use a random secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'  # Path to our database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disables a feature we don’t need

# Initialize the database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Handle get and post requests Route to the login page,
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()  # Find user by username
        
        # Check if user exists and password matches (password checking is simplified here)
        if user and user.password == password:
            login_user(user)  # Log the user in
            return redirect(url_for('dashboard'))  # Redirect to dashboard if successful
        else:
            return 'Invalid credentials', 401  # Return error if credentials are wrong
    
    return render_template('login.html')

# Route for the dashboard (only accessible by logged-in users)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('login'))  # Redirect to login page after logout

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
