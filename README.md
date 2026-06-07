# CraftProfile - Custom Profile & Portfolio Website Builder

CraftProfile is a sleek, modern Django-based web application featuring a Material Design theme. It allows users to register, log in, and design a custom public profile or portfolio page with images, multiple dynamic templates (Material, Cyberpunk, Glassmorphism, Minimalist), colors, and typography choices. It also features a custom Administrative User Access Dashboard for staff members.

## Features
- **User Authentication**: Secure sign-in, registration, and logout.
- **Custom Profile Editor**: Edit professional title, bio, location, and social links (GitHub, LinkedIn, Twitter, Personal Website).
- **Design Customization**:
  - **Color Picker**: Change primary and accent theme colors dynamically.
  - **Dynamic Templates**: Material Theme, Cyberpunk Glow, Glassmorphism, and Minimalist Clean.
  - **Typography**: Select from Google Fonts (Roboto, Inter, Playfair Display, Fira Code).
- **Portfolio Gallery**: Upload, describe, and delete multiple showcase images/projects.
- **Image Hover Overlays**: Elegant sliding text covers inspired by Adobe Portfolio.
- **Opt-Out Toggle**: Floating button on public portfolios allowing visitors to disable all animations/FX in favor of a static, clean structure.
- **Profile Privacy**: Option to toggle profiles between Public (visible in directory) and Private (locked access screen for guests).
- **Custom Admin Panel**: Dedicated administrative interface for staff users to activate/deactivate accounts, change user roles, and delete profiles.

---

## Setup & Running on Another Computer (Mac/Linux/Windows)

Follow these steps to run the application on any other machine:

1. **Clone or Copy** the repository folder to the destination machine.
2. **Open Terminal** (or command prompt) and navigate into the project directory.
3. **Initialize Virtual Environment**:
   - **macOS/Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     py -m venv .venv
     .\.venv\Scripts\activate
     ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```
6. **Create an Admin/Staff Account** (To access the Administrative Dashboard):
   ```bash
   python manage.py createsuperuser
   ```
7. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
8. **View the Application**: Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Run Unit Tests
To verify all authentication constraints, dynamic views, privacy settings, and lock screens:
```bash
python manage.py test
```
