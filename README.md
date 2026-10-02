# Flask Portfolio — Complete Starter

## 1. Requirements
- Python 3.10+
- pip

## 2. Install

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows:
```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Environment
Copy `.env.example` to `.env` and change the secret/password:

```env
SECRET_KEY=put-a-long-random-secret-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me-123
```

## 4. Run

```bash
python run.py
```

Open:
- Website: http://127.0.0.1:5000/
- Admin: http://127.0.0.1:5000/admin/login

The SQLite database is created automatically at `instance/portfolio.db`.

## 5. Admin
The first run creates the admin account using the values in `.env`.
Default only if you do not create `.env`:
- Username: `admin`
- Password: `admin123`

Change the password immediately from Admin → Password.

## 6. Uploads
Project and profile images are stored in:
`app/static/uploads/`

Supported upload types: PNG, JPG, JPEG, GIF, WEBP and PDF.

## 7. Important production notes
Before deploying publicly:
- Use a strong SECRET_KEY.
- Change the admin password.
- Run Flask behind a production WSGI server such as Gunicorn.
- Set debug mode off.
- Use HTTPS.
- Add server-side rate limiting for login/contact if deploying publicly.
# My-Protfolio
