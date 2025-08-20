from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions so they can be imported by other modules
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the app using a mapping
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),
        SQLALCHEMY_DATABASE_URI='sqlite:///autoinvestigator.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Initialize extensions with the application instance
    db.init_app(app)
    login_manager.init_app(app)
    # When a user needs to log in, redirect them to the login route in the 'auth' blueprint
    login_manager.login_view = 'auth.login'

    # The user_loader function tells Flask-Login how to find a specific user
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Import the blueprints
        from .main import main_bp  # Main application routes
        from .auth import auth_bp  # Authentication routes

        # Register the blueprints with the application
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

        # Create database tables if they don't exist
        db.create_all()

        # --- Minimal migration for ChatMessage table ---
        # Older databases may lack the new columns introduced for
        # chat history persistence. We inspect the existing table and
        # add any missing columns so the application can run without
        # requiring a manual database reset.
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        if 'chat_message' in inspector.get_table_names():
            columns = {col['name'] for col in inspector.get_columns('chat_message')}

            # Older databases stored the message body in a column named
            # ``message``. SQLite's limited ALTER TABLE support makes
            # renaming unreliable across versions, so instead we add the new
            # ``content`` column when missing and copy any existing data from
            # ``message``.
            if 'content' not in columns:
                db.session.execute(text('ALTER TABLE chat_message ADD COLUMN content TEXT'))
                if 'message' in columns:
                    db.session.execute(
                        text('UPDATE chat_message SET content = message WHERE content IS NULL')
                    )

            # Ensure newer fields exist
            if 'results' not in columns:
                db.session.execute(text('ALTER TABLE chat_message ADD COLUMN results TEXT'))
            if 'timestamp' not in columns:
                db.session.execute(text('ALTER TABLE chat_message ADD COLUMN timestamp FLOAT'))
            db.session.commit()

        return app
