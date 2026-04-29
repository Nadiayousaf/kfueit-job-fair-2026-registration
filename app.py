import os
from flask import Flask, render_template, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'kfueit-job-fair-2026-secret-key-change-me')

app.jinja_env.globals['enumerate'] = enumerate

from routes.auth import auth_bp
from routes.forms import forms_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(forms_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Protect dashboard — only logged-in admins
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@app.context_processor
def inject_storage_mode():
    """Tell templates whether we are using Sheets or SQLite."""
    from utils.google_sheets import _is_sheets_configured
    return dict(using_sheets=_is_sheets_configured())

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', code=404, message="Page Not Found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', code=500, message="Internal Server Error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
