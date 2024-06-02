from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for, session  # (secure coding principles) session management
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash  # (secure coding principles) Password hashing and verification
from .models import User
from . import db

auth = Blueprint('auth', __name__)

MAX_FAILED_ATTEMPTS = 5  # Maximum number of failed attempts 
LOCK_TIME = timedelta(minutes=30)  # setting: account lock time (30mins)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.is_locked:
                if user.locked_until and datetime.utcnow() < user.locked_until:
                    flash('Your account is locked for 30 minutes due to too many failed login attempts.', category='error')
                    return render_template('login.html')
                else:
                    user.is_locked = False
                    user.failed_attempts = 0
                    user.locked_until = None
                    db.session.commit()
                    
            if check_password_hash(user.password, password): # (secure coding principles) password verification
                user.failed_attempts = 0  # (secure coding principles) reset failed attempts
                login_user(user)
                session['user_id'] = user.id  # (secure coding principles) Save user id in session
                flash('Login successful!', category='success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.homepage'))
            else:
                user.failed_attempts += 1  # (secure coding principles) increasing failed attempts count
                if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
                    user.is_locked = True  # (secure coding principles) lock account 
                    user.locked_until = datetime.utcnow() + LOCK_TIME  # (secure coding principles) lock duration **should be random time for security.
                db.session.commit()
                flash('Invalid credentials. Please try again.', category='error')
        else:
            flash('Invalid credentials. Please try again.', category='error')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)  #(secure coding principles) Remove user id from session
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')  # Add phone number field
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)  # (secure coding principles) Password hashing
        new_user = User(email=email, phone=phone, password=hashed_password)  # Store phone number
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful!', category='success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')