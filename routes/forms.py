from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from utils.google_sheets import save_registration, check_email_exists

forms_bp = Blueprint('forms', __name__)

@forms_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form.to_dict()

        # Normalize email
        if 'email' in data:
            data['email'] = data['email'].strip().lower()

        # Validation
        required_fields = ['full_name', 'email', 'phone', 'degree', 'department']
        errors = []
        for field in required_fields:
            if not data.get(field, '').strip():
                errors.append(f'{field.replace("_", " ").title()} is required.')

        if errors:
            if request.is_json:
                return jsonify({'success': False, 'errors': errors}), 400
            for err in errors:
                flash(err, 'danger')
            return render_template('register.html', form_data=data)

        # Duplicate email check
        if check_email_exists(data.get('email', '')):
            msg = 'This email is already registered. Please use a different email.'
            if request.is_json:
                return jsonify({'success': False, 'errors': [msg]}), 400
            flash(msg, 'warning')
            return render_template('register.html', form_data=data)

        # Save registration
        success = save_registration(data)

        if success:
            if request.is_json:
                return jsonify({'success': True, 'message': 'Registration successful!'})
            flash('Registration successful! We look forward to seeing you at KFUEIT Job Fair 2026.', 'success')
            return redirect(url_for('index'))
        else:
            msg = 'Registration could not be saved. Please check your details and try again.'
            if request.is_json:
                return jsonify({'success': False, 'errors': [msg]}), 500
            flash(msg, 'danger')
            return render_template('register.html', form_data=data)

    return render_template('register.html', form_data={})
