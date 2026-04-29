import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kfueit-job-fair-2026-secret-key-change-in-production')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_SHEETS_SPREADSHEET_ID = os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID', '')
    
    # Admin credentials (change these!)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin@KFUEIT2026')
    
    # Sheet names
    REGISTRATIONS_SHEET = 'Registrations'
    COMPANIES_SHEET = 'Companies'
