# File: messaging_app/README.md

"""
# Messaging App (Django API)

A simple messaging backend built with Django + Django REST Framework.

## Features
- Custom user model (optional)
- Conversations & Messages
- REST API endpoints
- Modular structure

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API URLs
- `/api/conversations/`
- `/api/messages/`

"""

# --- requirements.txt ---
django
djangorestframework
django-environ