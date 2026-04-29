<<<<<<< HEAD
# KFUEIT Job Fair 2026 – Web App

A full-stack Flask web application for managing student registrations for the KFUEIT Job Fair 2026. Uses Google Sheets as the database.

---

## 🚀 Quick Start

### 1. Clone / Unzip the Project

```bash
cd KFUEIT-Job-Fair-2026
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Google Sheets (see section below)

### 5. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your values
```

### 6. Run the App

```bash
python app.py
```

Open: **http://localhost:5000**

---

## 📋 Pages

| Route | Description |
|-------|-------------|
| `/` | Homepage |
| `/register` | Student registration form |
| `/dashboard` | Event info & countdown |
| `/login` | Admin login |
| `/admin` | Admin panel (protected) |
| `/logout` | Logout |

---

## 🔑 Google Sheets Setup

### Step 1: Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (e.g. "KFUEIT-Job-Fair")
3. Enable these APIs:
   - **Google Sheets API**
   - **Google Drive API**

### Step 2: Create Service Account

1. Go to **IAM & Admin > Service Accounts**
2. Click **Create Service Account**
3. Name it (e.g. `kfueit-sheets-service`)
4. Grant role: **Editor**
5. Click **Done**

### Step 3: Download Credentials

1. Click on the service account you just created
2. Go to **Keys** tab → **Add Key** → **Create new key**
3. Choose **JSON** format
4. Download the file
5. Rename it to `credentials.json`
6. Place it in the **root folder** of the project (same level as `app.py`)

### Step 4: Create Google Spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet named **"KFUEIT Job Fair 2026"**
3. Copy the **Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```
4. Share the spreadsheet with your **service account email**:
   - Click **Share**
   - Paste the service account email (found in `credentials.json` as `client_email`)
   - Give **Editor** permission

### Step 5: Update .env

```env
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
```

The app will automatically create a **"Registrations"** worksheet with headers on first use.

---

## 🔐 Admin Login

Default credentials (change in `.env`!):
- **Username:** `admin`
- **Password:** `admin@KFUEIT2026`

---

## 📁 Project Structure

```
KFUEIT-Job-Fair-2026/
├── app.py                  # Main Flask app
├── requirements.txt
├── .env.example            # Environment template
├── credentials.json        # Google service account (YOU provide this)
├── templates/
│   ├── base.html           # Base layout with navbar/footer
│   ├── index.html          # Homepage
│   ├── register.html       # Registration form
│   ├── login.html          # Admin login
│   ├── dashboard.html      # Event dashboard
│   ├── admin.html          # Admin panel
│   └── error.html          # Error pages
├── static/
│   ├── css/style.css       # All styles
│   └── js/
│       ├── main.js         # Global JS
│       └── form.js         # Form validation
├── routes/
│   ├── auth.py             # Login/logout routes
│   ├── forms.py            # Registration form route
│   └── admin.py            # Admin panel route
└── utils/
    ├── config.py           # Configuration
    └── google_sheets.py    # Google Sheets integration
```

---

## ⚠️ Notes

- Keep `credentials.json` **out of version control** (add to `.gitignore`)
- Change `SECRET_KEY` and admin credentials in production
- The app creates the Registrations sheet automatically on first submission
=======
# kfueit-job-fair-2026-registration
KFUEIT Job Fair Registration System built with Python and SQLite for managing student registrations and admin job fair operations.
>>>>>>> c49e3b93520f22ad576c787240628acb2f644e4e
