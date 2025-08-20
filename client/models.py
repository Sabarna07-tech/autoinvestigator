from flask_login import UserMixin
import time
from . import db

class User(UserMixin, db.Model):
    """User model for storing user details and authentication status."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    
    # Fields for email verification
    verification_code = db.Column(db.String(10), nullable=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)


class ChatMessage(db.Model):
    """Store individual chat messages for each user."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'ai'
    content = db.Column(db.Text, nullable=False)
    results = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.Float, default=lambda: time.time(), nullable=False)

    user = db.relationship('User', backref=db.backref('messages', lazy=True))

