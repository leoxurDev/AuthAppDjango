# Django Authentication Starter

This project is a basic Django authentication app with:

- local username/password login and signup
- Google sign-in support through django-allauth

## Requirements

- Python 3.9+
- pip

## Run on another computer

1. Clone or copy this project folder.
2. Open a terminal in the project root.
3. Create and activate a virtual environment:
   - macOS/Linux:
     python3 -m venv .venv
     source .venv/bin/activate
   - Windows:
     py -m venv .venv
     .\.venv\Scripts\activate
4. Install dependencies:
   pip install -r requirements.txt
5. Apply database migrations:
   python manage.py migrate
6. Start the app:
   python manage.py runserver
7. Open the app in your browser:
   http://127.0.0.1:8000/

## Google login setup

1. Create a Google OAuth client in Google Cloud Console.
2. Add this authorized redirect URI:
   http://127.0.0.1:8000/accounts/google/login/callback/
3. In the Django admin, create a Social Application for Google and add your client ID and secret.

## Notes

- The app uses SQLite by default, so the database file will be created locally.
- For production use, replace the default secret key and enable proper security settings.
