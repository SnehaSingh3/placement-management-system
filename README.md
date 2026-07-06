# Placement Management System

A simple placement portal made with Flask + SQLAlchemy. Has 3 types of users - Admin, Student and Company, each with their own login and dashboard.

## What it does

- Students can register and apply to placement drives
- Companies can register (needs admin approval first) and post drives
- Admin approves companies and can see all students/companies/drives/applications
- No duplicate applications allowed for the same drive

## Tech used

- Python + Flask
- Flask-SQLAlchemy (SQLite)
- Bootstrap for the frontend

## How to run it

```bash
git clone https://github.com/SnehaSingh3/placement-management-system.git
cd placement-management-system
pip install -r requirements.txt
python app.py
```

Then go to `http://127.0.0.1:5000` in your browser. The database (`placement.db`) gets created on its own, no setup needed.

## Note on admin login

There's no signup page for admin yet, so you have to add one yourself through a python shell:

```python
from app import app, db
from models import Admin
with app.app_context():
    db.session.add(Admin(username="admin", passhash="yourpassword"))
    db.session.commit()
```

## TODO / things to improve

- passwords are stored as plain text right now, should hash them
- move secret key + db path to env variables instead of hardcoding
- add a proper admin signup

## Author

Sneha Singh — IITM BS Data Science Program
