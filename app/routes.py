from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from app import app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Verify password
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard

        flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)
