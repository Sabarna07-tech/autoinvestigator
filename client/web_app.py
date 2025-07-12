from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import json
import uuid
import re
import threading
import time
from client.agent import AutoInvestigatorAgent
import os
from client.models import db
from client.auth import auth_bp, google_bp, login_manager
from flask_login import current_user

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autoinvestigator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# SQLAlchemy and Flask-Login setup
db.init_app(app)
login_manager.init_app(app)

# Global agent instance
agent = AutoInvestigatorAgent()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(google_bp, url_prefix='/login')

# Protect main pages (scaffold)
def login_required(view):
    def wrapped_view(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view

@app.route('/')
def landing_page():
    """Main landing page with immersive animations"""
    return render_template('landing.html')

@app.route('/investigate')
def investigate_page():
    """Interactive investigation interface"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('investigate.html')

@app.route('/api/investigate', methods=['POST'])
def investigate():
    """API endpoint for running investigations"""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        selected_tool = data.get('tool', 'all')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # For now, return a structured response
        # In a real implementation, this would call the agent and process results
        response_data = {
            'status': 'success',
            'message': f'Investigation completed for: {user_query}',
            'results': {
                'financial': f'Financial analysis for {user_query} shows strong performance indicators with positive growth trends.',
                'news': f'Recent news sentiment analysis for {user_query} indicates positive market reception.',
                'sentiment': f'Sentiment analysis reveals optimistic outlook for {user_query} based on social media and news coverage.',
                'risk': f'Risk assessment for {user_query} shows moderate risk profile with manageable challenges.'
            },
            'tool_used': selected_tool,
            'timestamp': time.time()
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Check investigation status"""
    return jsonify({'status': 'ready'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Only for local dev, never in production!
    app.run(debug=True, host='0.0.0.0', port=5000) 