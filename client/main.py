from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
import time
import random
import string
import uuid
import requests
from urllib.parse import urljoin

from client.config import SERVER_URL

SERVER_BASE_URL = SERVER_URL.rsplit('/', 1)[0]

# Corrected imports:
# Import 'db' directly from the client package (__init__.py)
# Import 'User' from the models module
from . import db
from .models import User

# Import the mail sending utility
from server.tools.mail_sender import send_verification_email

# Create a Blueprint for the main application routes
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def landing_page():
    """Renders the main landing page."""
    return render_template('landing.html')


@main_bp.route('/investigate')
@login_required
def investigate_page():
    """
    Renders the interactive investigation interface.
    Requires the user to be logged in and email-verified.
    """
    if not current_user.is_verified:
        flash('Please verify your email address to access the investigation page.', 'warning')
        return redirect(url_for('main.verify'))
    return render_template('investigate.html')


@main_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    """
    Renders the verification page and handles the verification code submission.
    """
    if current_user.is_authenticated and current_user.is_verified:
        return redirect(url_for('main.investigate_page'))

    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('code')

        if not email or not code:
            flash('Please provide both your email and the verification code.', 'danger')
            return render_template('verify.html')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('A user with that email address was not found.', 'danger')
            return render_template('verify.html')

        if user.is_verified:
            flash('This account has already been verified. Please log in.', 'success')
            return redirect(url_for('auth.login'))

        if user.verification_code == code:
            user.is_verified = True
            db.session.commit()
            flash('Your account has been successfully verified! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid verification code. Please try again.', 'danger')

    return render_template('verify.html')


@main_bp.route('/resend_verification')
@login_required
def resend_verification():
    """Endpoint for logged-in users to resend their verification email."""
    if current_user.is_verified:
        flash('Your account is already verified.', 'info')
        return redirect(url_for('main.investigate_page'))

    new_code = ''.join(random.choices(string.digits, k=6))
    current_user.verification_code = new_code
    db.session.commit()

    try:
        send_verification_email(current_user.email, new_code)
        flash('A new verification email has been sent to your address.', 'success')
    except Exception as e:
        flash('There was an error sending the verification email. Please try again later.', 'danger')
        print(f"Error resending verification email: {e}")

    return redirect(url_for('main.verify'))


@main_bp.route('/api/investigate', methods=['POST'])
@login_required
def investigate():
    """API endpoint for running investigations via the MCP server."""
    if not current_user.is_verified:
        return jsonify({'error': 'Email not verified.'}), 403

    try:
        data = request.get_json()
        user_query = data.get('query', '')
        selected_tool = data.get('tool', 'all')

        if not user_query:
            return jsonify({'error': 'No query provided'}), 400

        tool_map = {
            'financial': ('financial_descriptor', {'ticker': user_query, 'cik': 'Unknown'}),
            'news': ('news', {'name': user_query}),
            'websearch': ('websearch', {'query': user_query}),
            'gemini': ('gemini', {'query': user_query}),
            'all': ('gemini', {'query': user_query}),
        }

        method, params = tool_map.get(selected_tool, ('gemini', {'query': user_query}))

        payload = {
            'id': f'client-{uuid.uuid4()}',
            'requests': [
                {
                    'id': f'req-{uuid.uuid4()}',
                    'method': f'tools/{method}',
                    'params': params,
                }
            ]
        }

        server_resp = requests.post(SERVER_URL, json=payload)
        server_resp.raise_for_status()
        server_json = server_resp.json()

        result_text = ''
        results_list = server_json.get('results', [])
        if results_list:
            result_text = results_list[0].get('results', [''])[0]

        # Generate a short summary for the chat history while preserving
        # the full results for the side panel
        summary = (result_text[:200].strip() + '...') if len(result_text) > 200 else result_text

        response_data = {
            'status': 'success',
            'message': summary or 'Investigation completed successfully.',
            'results': result_text,
            'tool_used': selected_tool,
            'timestamp': time.time(),
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/upload-pdf', methods=['POST'])
@login_required
def upload_pdf():
    """Proxy PDF analysis requests to the MCP server."""
    if not current_user.is_verified:
        return jsonify({'error': 'Email not verified.'}), 403

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    analysis_type = request.form.get('analysis_type', 'comprehensive')

    files = {'file': (file.filename, file.stream, file.mimetype)}
    data = {'analysis_type': analysis_type}

    try:
        server_url = urljoin(SERVER_BASE_URL + '/', 'upload-pdf')
        resp = requests.post(server_url, files=files, data=data)
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/status')
def status():
    """Simple API endpoint to check if the service is running."""
    return jsonify({'status': 'ready'})
