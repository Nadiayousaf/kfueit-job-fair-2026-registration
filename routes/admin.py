import csv
import io
from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify, Response
from functools import wraps
from utils.google_sheets import get_all_registrations, get_registration_count, _is_sheets_configured

admin_bp = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please login to access the admin panel.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@login_required
def dashboard():
    try:
        registrations = get_all_registrations()
        count = len(registrations)
    except Exception as e:
        registrations = []
        count = 0
        flash(f'Could not load data: {str(e)}', 'danger')

    departments = {}
    job_types = {}
    for reg in registrations:
        dept = reg.get('Department', '') or 'Unknown'
        departments[dept] = departments.get(dept, 0) + 1
        jt = reg.get('Job Type', '') or 'Not specified'
        job_types[jt] = job_types.get(jt, 0) + 1

    storage_mode = 'Google Sheets' if _is_sheets_configured() else 'Local Database (SQLite)'

    return render_template('admin.html',
        registrations=registrations,
        count=count,
        departments=departments,
        job_types=job_types,
        storage_mode=storage_mode,
    )

@admin_bp.route('/admin/export/csv')
@login_required
def export_csv():
    """Export all registrations as a downloadable CSV file."""
    try:
        registrations = get_all_registrations()
    except Exception as e:
        flash(f'Export failed: {str(e)}', 'danger')
        return redirect(url_for('admin.dashboard'))

    if not registrations:
        flash('No registrations to export.', 'warning')
        return redirect(url_for('admin.dashboard'))

    fieldnames = [
        'Timestamp', 'Full Name', 'Email', 'Phone', 'CNIC',
        'Degree', 'Department', 'Graduation Year', 'GPA/CGPA',
        'Skills', 'Job Type', 'CV Link', 'LinkedIn', 'Message'
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for reg in registrations:
        writer.writerow(reg)

    csv_bytes = output.getvalue().encode('utf-8-sig')  # utf-8-sig for Excel compatibility
    return Response(
        csv_bytes,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=KFUEIT-Job-Fair-2026-Registrations.csv'}
    )

@admin_bp.route('/admin/api/registrations')
@login_required
def api_registrations():
    try:
        registrations = get_all_registrations()
        return jsonify({'success': True, 'data': registrations, 'count': len(registrations)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
