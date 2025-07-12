from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask import current_app as app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import os
from client.models import db, User

# Flask Blueprint for auth
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Google OAuth blueprint (register with Flask app in web_app.py)
google_bp = make_google_blueprint(
    client_id=os.environ.get('GOOGLE_OAUTH_CLIENT_ID', 'your-google-client-id'),
    client_secret=os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', 'your-google-client-secret'),
    scope=["profile", "email"],
    redirect_url="/auth/google_callback"
)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class UserLogin(UserMixin, User):
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password_hash and user.check_password(password):
            login_user(user)
            session['user'] = {
                'email': user.email,
                'name': user.name,
                'picture': user.picture,
                'google_id': user.google_id
            }
            flash('Logged in successfully!', 'success')
            return redirect(url_for('landing_page'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth.html', mode='login')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = email.split('@')[0]
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered. Please sign in.', 'warning')
        else:
            user = User(email=email, name=name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session['user'] = {
                'email': user.email,
                'name': user.name,
                'picture': user.picture,
                'google_id': user.google_id
            }
            flash('Account created successfully!', 'success')
            return redirect(url_for('landing_page'))
    return render_template('auth.html', mode='signup')

@auth_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    if resp.ok:
        user_info = resp.json()
        # Find or create user in DB
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                email=user_info['email'],
                name=user_info.get('name'),
                google_id=user_info.get('id'),
                picture=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        session['user'] = {
            'email': user.email,
            'name': user.name,
            'picture': user.picture,
            'google_id': user.google_id
        }
        return redirect(url_for('landing_page'))
    flash('Failed to log in with Google.', 'danger')
    return redirect(url_for('auth.login'))

@auth_bp.route('/google_callback')
def google_callback():
    # This route is handled by flask-dance
    return redirect(url_for('auth.google_login')) 