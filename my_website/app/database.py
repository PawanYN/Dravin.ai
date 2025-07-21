# --------------------------------------------------
# Imports & Constants
# --------------------------------------------------

import os
import sqlite3
import hashlib
import traceback
import qrcode

DB_NAME = 'database.db'
RECORDS_PER_PAGE = 50

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def generate_user_id(first_name, last_name, phone):
    """Generate a unique user ID based on name and phone number."""
    first_name_clean = first_name.strip().lower()
    last_name_clean = last_name.strip().lower()
    phone_clean = phone.strip()
    full_name = f"{first_name_clean}{last_name_clean}"
    hash_part = hashlib.sha256(full_name.encode()).hexdigest()[:8]
    return f"{phone_clean}_{first_name_clean}_{last_name_clean}_{hash_part}"

def get_db_connection():
    """Get a SQLite database connection with row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

def init_db():
    """Create or update the users and attendance tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            preacher TEXT NOT NULL,
            center TEXT NOT NULL,
            message TEXT,
            payment_id TEXT,
            is_pending INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            user_id TEXT PRIMARY KEY,
            qr_code_location TEXT NOT NULL,
            day_1 INTEGER DEFAULT 0,
            day_2 INTEGER DEFAULT 0,
            day_3 INTEGER DEFAULT 0,
            day_4 INTEGER DEFAULT 0,
            day_5 INTEGER DEFAULT 0,
            day_6 INTEGER DEFAULT 0,
            day_7 INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# --------------------------------------------------
# User Management
# --------------------------------------------------

def insert_user(first_name, last_name, email, phone, age, preacher, center, payment_id, message=None, is_pending=1):
    """Insert a new user into the database."""
    user_id = generate_user_id(first_name, last_name, phone)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (id, first_name, last_name, email, phone, age, preacher, center, message, payment_id, is_pending)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, first_name, last_name, email, phone, age, preacher, center, message, payment_id, is_pending))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("User already exists.")
        return False
    finally:
        conn.close()

def get_users():
    """Retrieve users with pending status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE is_pending = 1')
    records = cursor.fetchall()
    conn.close()
    return records

def check_id_exists(first_name, last_name, phone, db_file='database.db', table_name='users'):
    """Check if a user ID already exists in the database."""
    user_id = generate_user_id(first_name, last_name, phone)
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = ? LIMIT 1", (user_id,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

# --------------------------------------------------
# Attendance Management
# --------------------------------------------------

def generate_qr_code(user_id: str, attendance_endpoint: str = "http://127.0.0.1:5000/attendance", save_dir: str = "app/static/qr_codes"):
    """Generate a QR code for the user's attendance endpoint."""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"{user_id}.png")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=2,
    )
    qr.add_data(f"{attendance_endpoint}/{user_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)

    return path

def create_attendance_record(first_name, last_name, phone):
    """Create an attendance record and generate a QR code."""
    try:
        user_id = generate_user_id(first_name, last_name, phone)
        qr_code_path = generate_qr_code(user_id)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO attendance (
                user_id, qr_code_location,
                day_1, day_2, day_3, day_4, day_5, day_6, day_7
            )
            VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0)
        ''', (user_id, qr_code_path))

        conn.commit()
        print(f"[INFO] Attendance record created for user_id: {user_id}")
        return user_id, qr_code_path

    except sqlite3.IntegrityError:
        print(f"[WARNING] Attendance already exists for user_id: {user_id}")
        raise
    except Exception as e:
        print(f"[ERROR] Failed to create attendance record: {e}")
        print(traceback.format_exc())
        raise
    finally:
        conn.close()

# --------------------------------------------------
# Attendance Viewer / Pagination & Search
# --------------------------------------------------

def fetch_attendance_records(page, search_query):
    """Fetch paginated attendance records with optional search."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        offset = (page - 1) * RECORDS_PER_PAGE
        search_param = f'%{search_query}%' if search_query else '%'

        # Count total matching records
        cursor.execute('''
            SELECT COUNT(*) as total
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            WHERE (u.first_name || ' ' || u.last_name LIKE ? OR u.phone LIKE ?)
        ''', (search_param, search_param))
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + RECORDS_PER_PAGE - 1) // RECORDS_PER_PAGE

        # Clamp page within range
        page = max(1, min(page, total_pages))
        offset = (page - 1) * RECORDS_PER_PAGE

        # Fetch records
        cursor.execute('''
            SELECT a.user_id,
                   a.day_1, a.day_2, a.day_3, a.day_4, a.day_5, a.day_6, a.day_7,
                   u.first_name || ' ' || u.last_name as name,
                   u.phone
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            WHERE (u.first_name || ' ' || u.last_name LIKE ? OR u.phone LIKE ?)
            ORDER BY a.user_id
            LIMIT ? OFFSET ?
        ''', (search_param, search_param, RECORDS_PER_PAGE, offset))

        records = [
            {**dict(row), 'qr_code_url': f'static/qr_codes/{row["user_id"]}.png', 'qr_code_location': f"{row['user_id']}.png"}
            for row in cursor.fetchall()
        ]

        return records, page, total_pages, search_query

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return [], page, 0, search_query
    finally:
        conn.close()
