from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import random
import string

# Import 'db' directly from the client package (__init__.py)
# Import 'User' from the models module
from . import db
from .models import User

# Import the mail sending utility from the server package
from server.tools.mail_sender import send_verification_email

# Create a Blueprint for authentication routes, with a URL prefix
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.investigate_page'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.is_verified:
            flash('Your account is not verified. Please check your email for the verification code.', 'warning')
            return redirect(url_for('main.verify'))

        login_user(user)
        return redirect(url_for('main.investigate_page'))

    # For a GET request, render the auth template
    return render_template('auth.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles new user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.investigate_page'))

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account with this email address already exists.', 'danger')
            return redirect(url_for('auth.signup'))

        verification_code = ''.join(random.choices(string.digits, k=6))

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            verification_code=verification_code,
            is_verified=False
        )

        db.session.add(new_user)
        db.session.commit()

        try:
            send_verification_email(new_user.email, verification_code)
            flash('Registration successful! Please check your email for a verification code.', 'success')
        except Exception as e:
            print(f"Error sending signup email: {e}")
            flash('Registration successful, but the verification email could not be sent.', 'warning')

        # Redirect to the verification page after signup
        return redirect(url_for('main.verify'))

    # For a GET request, render the auth template
    return render_template('auth.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handles user logout."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
