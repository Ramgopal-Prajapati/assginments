# 🎓 Samyak Computer Classes By Ram sir — Assignment System
### Ram Sir | Indore | Full Django Assignment Portal

A complete assignment management system for students and faculty.  
Built with **Django 4.2 · HTML · CSS · JavaScript**

---

## ✨ Features

| Feature | Student | Faculty | Admin |
|---|---|---|---|
| Login / Logout | ✅ | ✅ | ✅ |
| Dashboard with stats | ✅ | ✅ | — |
| View assigned work | ✅ | — | — |
| Submit assignment + GitHub link | ✅ | — | — |
| Refuse/reject assignment | ✅ | — | — |
| Resubmit after rejection | ✅ | — | — |
| Assign work to students (category-filtered) | — | ✅ | — |
| Review submissions (Accept / Reject) | — | ✅ | — |
| Add remarks on review | — | ✅ | — |
| Real-time notifications | ✅ | ✅ | — |
| Add / manage students | — | — | ✅ |
| Add / manage faculty | — | — | ✅ |
| Full user CRUD | — | — | ✅ |

---

## 🗂 Project Structure

```
samyak_assignments/
├── manage.py
├── requirements.txt
├── Procfile                    ← Railway/Heroku deploy
├── railway.json                ← Railway config
├── runtime.txt                 ← Python version
├── .gitignore
│
├── samyak_assignments/         ← Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── assignments/                ← Main app
│   ├── models.py               ← CustomUser, Assignment, Submission, Notification
│   ├── views.py                ← All page views + error handlers
│   ├── forms.py                ← Login, Assignment, Submission, Review forms
│   ├── urls.py                 ← URL routes
│   ├── admin.py                ← Django admin config
│   └── management/
│       └── commands/
│           └── setup_demo.py   ← Creates demo users & assignments
│
├── templates/
│   ├── 404.html
│   ├── 500.html
│   └── assignments/
│       ├── base.html           ← Sidebar + topbar + notification panel
│       ├── login.html          ← Split-screen login page
│       ├── student_dashboard.html
│       ├── faculty_dashboard.html
│       ├── submit_assignment.html
│       ├── review_submission.html
│       ├── assignment_detail.html
│       └── all_assignments.html
│
└── static/
    ├── css/main.css
    └── js/main.js
```

---

## ⚙️ Local Setup (Step by Step)

### Step 1 — Clone / download the project
```bash
cd samyak_assignments
```

### Step 2 — Create a virtual environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run database migrations
```bash
python manage.py makemigrations assignments
python manage.py migrate
```

### Step 5 — Create demo users (optional but recommended for testing)
```bash
python manage.py setup_demo
```

This creates:
| Username    | Password      | Role    | Category |
|-------------|---------------|---------|----------|
| admin       | admin@123     | Admin   | —        |
| ramsir      | ram@123       | Faculty | Tech     |
| priyamam    | priya@123     | Faculty | Non-Tech |
| rahul001    | student@123   | Student | Tech     |
| anita002    | student@123   | Student | Tech     |
| mohit003    | student@123   | Student | Tech     |
| pooja004    | student@123   | Student | Non-Tech |
| suresh005   | student@123   | Student | Non-Tech |

### Step 6 — Run the development server
```bash
python manage.py runserver
```

Open your browser:
- **Login Page** → http://127.0.0.1:8000/
- **Admin Panel** → http://127.0.0.1:8000/admin/

---

## 👨‍💼 Admin Panel Usage

### Adding a New Student
1. Go to `/admin/` → login as admin
2. Users → **Add User**
3. Set username, password
4. Fill: First name, Last name, Email, Phone
5. Set **Role = Student**
6. Set **Student ID** (e.g. STU-010)
7. Set **Course Name** (e.g. Python + Django)
8. Set **Category** = Tech or Non-Tech
9. Save ✅

### Adding a New Faculty
1. Go to `/admin/` → Users → **Add User**
2. Set username, password
3. Fill: First name, Last name, Email
4. Set **Role = Faculty**
5. Set **Category** = Tech or Non-Tech (faculty sees students of their category only)
6. Check **Staff status** = ✅ (so they can log in to admin if needed)
7. Save ✅

### Assigning Assignments from Admin
1. Go to Assignments → **Add Assignment**
2. Fill: Number, Title, Details, Due Date
3. Select **Assigned To** (student) and **Assigned By** (faculty)
4. Save ✅

---

## 🚀 Deploy on Railway

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit — Samyak Assignment System"
git remote add origin https://github.com/YOUR_USERNAME/samyak-assignments.git
git push -u origin main
```

### Step 2 — Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your repository

### Step 3 — Add PostgreSQL (Recommended for production)
1. In Railway dashboard → **+ Add Plugin** → **PostgreSQL**
2. Railway auto-sets `DATABASE_URL` environment variable ✅

### Step 4 — Set Environment Variables
In Railway → your service → **Variables** tab:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (generate one: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DEBUG` | `False` |
| `DJANGO_SETTINGS_MODULE` | `samyak_assignments.settings` |

### Step 5 — Deploy
Railway automatically runs the `Procfile` command:
```
python manage.py migrate && python manage.py collectstatic && gunicorn samyak_assignments.wsgi
```

### Step 6 — Create superuser on Railway
Using Railway CLI:
```bash
npm install -g @railway/cli
railway login
railway run python manage.py createsuperuser
# or
railway run python manage.py setup_demo
```

### Step 7 — Your app is live! 🎉
Railway gives you a URL like: `https://samyak-assignments.up.railway.app`

---

## 🔑 URL Reference

| URL | Page | Access |
|-----|------|--------|
| `/` | Login page | Public |
| `/login/` | Login page | Public |
| `/logout/` | Logout | Authenticated |
| `/dashboard/` | Student or Faculty dashboard | Authenticated |
| `/assignment/<id>/` | Assignment detail | Authenticated |
| `/assignment/<id>/submit/` | Submit assignment | Student |
| `/assignment/<id>/reject/` | Refuse assignment | Student |
| `/submission/<id>/review/` | Review submission | Faculty |
| `/assignments/` | All assignments list | Authenticated |
| `/admin/` | Django admin | Admin/Staff |

---

## 🎨 UI Overview

- **Dark theme** with purple/cyan gradient accents
- **Syne** font for headings, **DM Sans** for body
- **Animated stats** with count-up effect
- **Tabbed dashboard** — Pending / Submitted / Completed / Rejected
- **Notification bell** with unread indicator
- **Responsive** — works on mobile with hamburger sidebar
- **Modal dialogs** for assignment creation and review actions

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | Django custom user model |
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Fonts | Google Fonts (Syne + DM Sans) |
| Icons | Font Awesome 6 |
| Static files | WhiteNoise |
| Production server | Gunicorn |
| Deployment | Railway |

---

## 🛠 Troubleshooting

**Static files not loading?**
```bash
python manage.py collectstatic --noinput
```

**Migrations error?**
```bash
python manage.py makemigrations assignments
python manage.py migrate
```

**Password reset for a user?**
```bash
python manage.py shell
>>> from assignments.models import CustomUser
>>> u = CustomUser.objects.get(username='ramsir')
>>> u.set_password('newpassword')
>>> u.save()
```

**Reset everything (dev only)?**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py setup_demo
```

---

Built with ❤️ for Samyak Computer Classes students By Ram sir, Indore
