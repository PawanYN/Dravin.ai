# ----------------------
# Imports and Configuration
# ----------------------
import sqlite3
from datetime import datetime
import logging
import os

from flask import Blueprint, render_template, request, redirect, url_for, session, Response, flash, jsonify
from dotenv import load_dotenv

import app
from app.database import (
    insert_user, create_attendance_record, get_users, get_db_connection,
    check_id_exists, fetch_attendance_records
)
from app.email_utils import send_email

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Create blueprint
main = Blueprint('main', __name__)


# ----------------------
# Home Page
# ----------------------
@main.route('/')
def home():
    return render_template('index.html')


# ----------------------
# Registration Handlers (Multi-language)
# ----------------------
def handle_registration(form_template):
    """
    Shared logic for user registration.
    """
    if request.method == 'POST':
        if check_id_exists(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            phone=request.form['phone']
        ):
            return "User already exists"

        # Save form data to session
        data = {k: request.form.get(k) for k in ['first_name', 'last_name', 'email', 'phone', 'age', 'preacher', 'center', 'message']}
        for k, v in data.items():
            session[k] = v
            logging.info(f"{k}: {v}")

        return redirect(url_for('main.payment'))

    return render_template(form_template)


@main.route('/register', methods=['GET', 'POST'])
def register():
    return handle_registration('register.html')


@main.route('/register_hi', methods=['GET', 'POST'])
def register_hi():
    return handle_registration('register_hi.html')


@main.route('/register_ben', methods=['GET', 'POST'])
def register_ben():
    return handle_registration('register_ben.html')


# ----------------------
# Admin Login and Registration
# ----------------------
@main.route('/admin', methods=['GET', 'POST'])
def admin_login():
    """
    Admin authentication based on .env credentials.
    """
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin_username = os.getenv('FLASK_USERNAME')
        admin_password = os.getenv('FLASK_PASSWORD')

        if username == admin_username and password == admin_password:
            session['user_id'] = username
            session['is_admin'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')
            error = "Invalid username or password!"

    return render_template('admin-login.html', error=error)


@main.route('/adm_register', methods=['GET', 'POST'])
def adm_register():
    """
    Admin-only registration that bypasses payment.
    """
    if not session.get('is_admin'):
        return "You are not an admin", 400

    message = None
    if request.method == 'POST':
        data = {k: request.form.get(k) for k in ['first_name', 'last_name', 'email', 'phone', 'age', 'preacher', 'center', 'message']}
        confirmed = request.form.get('confirmed')

        if confirmed == 'yes':
            new_user = insert_user(**data, payment_id="offline_payment", is_pending=False)
            if not new_user:
                message = "User already exists"
            else:
                message = "User registered successfully"
                create_attendance_record(data['first_name'], data['last_name'], data['phone'])
        else:
            message = "User not added. Please confirm payment with admin."

    return render_template('reg_by_adm.html', message=message)


# ----------------------
# Payment and Confirmation
# ----------------------
@main.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')


@main.route('/success')
def success():
    """
    After successful payment, insert user and redirect to pending page.
    """
    user_data = {k: session.get(k) for k in ['first_name', 'last_name', 'email', 'phone', 'age', 'preacher', 'center', 'message']}
    user_data['payment_id'] = request.args.get('payment_id')

    insert_user(
        user_data['first_name'], user_data['last_name'], user_data['email'], user_data['phone'],
        int(user_data['age']), user_data['preacher'], user_data['center'],
        user_data['payment_id'], user_data['message'], is_pending=True
    )
    session.clear()
    return redirect(url_for('main.pending_page'))


@main.route('/pending_page')
def pending_page():
    return render_template("reg_pending.html")


# ----------------------
# Dashboard and Admin Controls
# ----------------------
@main.route('/dashboard')
def dashboard():
    if not session.get('is_admin'):
        return "You are not an admin", 400
    page = int(request.args.get('page', 1))
    search_query = request.args.get('search', '').strip()
    records, current_page, total_pages, search_query = fetch_attendance_records(page, search_query)
    return render_template('dashboard.html', records=records, current_page=current_page, total_pages=total_pages, search_query=search_query)


@main.route('/pending_requests', methods=['GET'])
def pending_requests():
    if not session.get('is_admin'):
        return "You are not an admin", 400

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    count_query = 'SELECT COUNT(*) FROM users WHERE is_pending = 1'
    if search:
        count_query += ' AND (first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR payment_id LIKE ?)'
        search_term = f'%{search}%'
        cursor.execute(count_query, (search_term, search_term, search_term, search_term))
    else:
        cursor.execute(count_query)

    total_records = cursor.fetchone()[0]
    total_pages = (total_records + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page = max(1, min(page, total_pages))
    offset = (page - 1) * ITEMS_PER_PAGE

    select_query = 'SELECT id, payment_id, first_name, last_name, email, phone, age, preacher, center FROM users WHERE is_pending = 1'
    if search:
        select_query += ' AND (first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR payment_id LIKE ?)' + f' LIMIT {ITEMS_PER_PAGE} OFFSET {offset}'
        cursor.execute(select_query, (search_term, search_term, search_term, search_term))
    else:
        select_query += f' LIMIT {ITEMS_PER_PAGE} OFFSET {offset}'
        cursor.execute(select_query)

    records = cursor.fetchall()
    conn.close()

    records_list = [{
        'id': r['id'], 'payment_id': r['payment_id'] or 'N/A',
        'first_name': r['first_name'], 'last_name': r['last_name'],
        'email': r['email'], 'phone': r['phone'], 'age': r['age'],
        'preacher': r['preacher'], 'center': r['center']
    } for r in records]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'records': records_list, 'page': page, 'total_pages': total_pages})
    return render_template('pending_requests.html', records=records_list, page=page, total_pages=total_pages)


# ----------------------
# Delete & Confirm Records (Admin Only)
# ----------------------
@main.route('/delete/<uid>', methods=['POST'])
def delete_record(uid):
    if not session.get('is_admin'):
        return "You are not an admin", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = ?', (uid,))
    if not cursor.fetchone():
        return jsonify({'success': False, 'message': 'Record not found'}), 404

    # cursor.execute('DELETE FROM attendance WHERE user_id = ?', (uid,))
    cursor.execute('DELETE FROM users WHERE id = ?', (uid,))
    conn.commit()
    return jsonify({'success': True, 'message': 'Record deleted successfully'})


@main.route('/confirm/<uid>', methods=['POST'])
def confirm_record(uid):
    if not session.get('is_admin'):
        return "You are not an admin", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, phone, email FROM users WHERE id = ?', (uid,))
    data = cursor.fetchone()
    if data:
        user_id, first_name, last_name, phone, email = data
        cursor.execute('UPDATE users SET is_pending = 0 WHERE id = ?', (uid,))
        conn.commit()
        create_attendance_record(first_name, last_name, phone)
        send_email(email,user_id)
        return jsonify({'success': True, 'message': 'Record confirmed successfully'})
    return jsonify({'success': False, 'message': 'Record not found'}), 404


# ----------------------
# Attendance Management
# ----------------------
dates_dict = {
    "2025-06-28": "day_1", "2025-06-29": "day_2", "2025-06-30": "day_3",
    "2025-07-01": "day_4", "2025-07-02": "day_5", "2025-07-03": "day_6",
    "2025-07-04": "day_7"
}

def update_attendance(user_id) -> bool:
    current_date = datetime.now().strftime('%Y-%m-%d')
    day = dates_dict.get(current_date)
    if not day:
        return False
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'UPDATE attendance SET {day} = 1 WHERE user_id = ?', (user_id,))
    if cursor.rowcount == 0:
        return False
    conn.commit()
    return True


@main.route('/attendance/<user_id>')
def attendance(user_id):
    if not session.get('is_admin'):
        return "You are not an admin", 400
    is_succeeded = update_attendance(user_id)
    return render_template('attendance.html', user_id=user_id, success=is_succeeded)


@main.route('/self_close')
def self_close():
    return render_template('self-close.html')


# ----------------------
# Constants
# ----------------------
ITEMS_PER_PAGE = 50
