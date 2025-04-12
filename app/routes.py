from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from app.models import User
from app.forms import RegistrationForm, LoginForm
from app import db
from werkzeug.security import check_password_hash
from flask_login import login_required, current_user
from app.models import Abstract, Review


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html') 

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('main.register'))
        
        # Create and save the new user
        user = User(username=form.username.data, is_admin=form.is_admin.data, subjects=form.subjects.data)
        user.set_password(form.password.data)  # Hash password
        db.session.add(user)
        db.session.commit()
        
        # Log the user in
        login_user(user)
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('dashboard'))  # Redirect to the dashboard
    
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Verify password
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))  # Redirect to the dashboard

        flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Get abstracts that the user hasn't reviewed yet
    reviewed_abstract_ids = [review.abstract_id for review in current_user.reviews]
    abstracts_to_review = Abstract.query.filter(~Abstract.id.in_(reviewed_abstract_ids)).all()

    return render_template('dashboard.html', user=current_user, abstracts=abstracts_to_review)
