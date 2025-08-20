from flask_login import UserMixin
from datetime import datetime

# Import the 'db' instance from the client package's __init__.py
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

    # Relationship to chat messages
    messages = db.relationship('ChatMessage', backref='user', lazy=True)


class ChatMessage(db.Model):
    """Stores individual chat messages for each user."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'ai'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

