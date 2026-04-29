"""
Google Sheets integration with SQLite fallback.

Agar Google Sheets credentials set nahi hain ya connection fail ho,
tab registrations local SQLite database mein save ho jaati hain.
"""

import os
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = os.environ.get('SQLITE_DB_PATH', 'registrations.db')

def _get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _ensure_db():
    with _get_db_conn() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT,
                full_name       TEXT,
                email           TEXT UNIQUE,
                phone           TEXT,
                cnic            TEXT,
                degree          TEXT,
                department      TEXT,
                graduation_year TEXT,
                gpa             TEXT,
                skills          TEXT,
                job_type        TEXT,
                cv_link         TEXT,
                linkedin        TEXT,
                message         TEXT
            )
        ''')
        conn.commit()

_ensure_db()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def _is_sheets_configured():
    creds_file = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
    spreadsheet_id = os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID', '')
    return bool(spreadsheet_id) and os.path.isfile(creds_file)

def _get_spreadsheet():
    import gspread
    from google.oauth2.service_account import Credentials
    creds_file = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
    creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID'))

def _ensure_sheet_exists(spreadsheet, sheet_name, headers):
    try:
        return spreadsheet.worksheet(sheet_name)
    except Exception:
        ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers))
        ws.append_row(headers)
        return ws

HEADERS = [
    'Timestamp', 'Full Name', 'Email', 'Phone', 'CNIC',
    'Degree', 'Department', 'Graduation Year', 'GPA/CGPA',
    'Skills', 'Job Type', 'CV Link', 'LinkedIn', 'Message'
]

def _build_row(data, timestamp):
    return [
        timestamp,
        data.get('full_name', ''),
        data.get('email', ''),
        data.get('phone', ''),
        data.get('cnic', ''),
        data.get('degree', ''),
        data.get('department', ''),
        data.get('graduation_year', ''),
        data.get('gpa', ''),
        data.get('skills', ''),
        data.get('job_type', ''),
        data.get('cv_link', ''),
        data.get('linkedin', ''),
        data.get('message', ''),
    ]

def _sqlite_save(data, timestamp):
    try:
        with _get_db_conn() as conn:
            conn.execute('''
                INSERT OR IGNORE INTO registrations
                (timestamp,full_name,email,phone,cnic,degree,department,
                 graduation_year,gpa,skills,job_type,cv_link,linkedin,message)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', _build_row(data, timestamp))
            if conn.total_changes == 0:
                logger.warning(f"Duplicate email in SQLite: {data.get('email')}")
                return False
            conn.commit()
        logger.info(f"Saved to SQLite: {data.get('email')}")
        return True
    except Exception as e:
        logger.error(f"SQLite save error: {e}")
        return False

def save_registration(data: dict) -> bool:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if _is_sheets_configured():
        try:
            sp = _get_spreadsheet()
            ws = _ensure_sheet_exists(sp, 'Registrations', HEADERS)
            ws.append_row(_build_row(data, timestamp))
            logger.info(f"Saved to Sheets: {data.get('email')}")
            _sqlite_save(data, timestamp)   # mirror backup
            return True
        except Exception as e:
            logger.error(f"Sheets save failed: {e}. Using SQLite fallback.")
    else:
        logger.warning("Google Sheets not configured — using SQLite.")

    return _sqlite_save(data, timestamp)

def _sqlite_get_all():
    try:
        with _get_db_conn() as conn:
            rows = conn.execute('SELECT * FROM registrations ORDER BY id DESC').fetchall()
        return [{
            'Timestamp': r['timestamp'],
            'Full Name': r['full_name'],
            'Email': r['email'],
            'Phone': r['phone'],
            'CNIC': r['cnic'],
            'Degree': r['degree'],
            'Department': r['department'],
            'Graduation Year': r['graduation_year'],
            'GPA/CGPA': r['gpa'],
            'Skills': r['skills'],
            'Job Type': r['job_type'],
            'CV Link': r['cv_link'],
            'LinkedIn': r['linkedin'],
            'Message': r['message'],
        } for r in rows]
    except Exception as e:
        logger.error(f"SQLite fetch error: {e}")
        return []

def get_all_registrations() -> list:
    if _is_sheets_configured():
        try:
            sp = _get_spreadsheet()
            ws = sp.worksheet('Registrations')
            records = ws.get_all_records()
            logger.info(f"Fetched {len(records)} from Sheets.")
            return records
        except Exception as e:
            logger.error(f"Sheets fetch failed: {e}. Using SQLite fallback.")
    return _sqlite_get_all()

def get_registration_count() -> int:
    try:
        return len(get_all_registrations())
    except Exception:
        return 0

def check_email_exists(email: str) -> bool:
    if not email:
        return False
    email = email.strip().lower()
    # Fast SQLite check first
    try:
        with _get_db_conn() as conn:
            row = conn.execute(
                'SELECT 1 FROM registrations WHERE LOWER(email)=?', (email,)
            ).fetchone()
            if row:
                return True
    except Exception as e:
        logger.error(f"SQLite email check error: {e}")

    # Also check Sheets if configured (covers old data)
    if _is_sheets_configured():
        try:
            for reg in get_all_registrations():
                if reg.get('Email', '').lower() == email:
                    return True
        except Exception as e:
            logger.error(f"Sheets email check error: {e}")

    return False
