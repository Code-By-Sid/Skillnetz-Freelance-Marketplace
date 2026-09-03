# SkillNetz — Freelance Marketplace

SkillNetz started with a question: why is finding good work — or good talent — so hard? Traditional job boards feel cold, and big marketplaces feel impersonal. SkillNetz is a Django-based freelance marketplace that pairs job posting and hiring with a professional networking layer (profiles, posts, resumes, and follows), plus in-app chat, file sharing, and payments for the work itself.

## ✨ Features

**Accounts & onboarding**
- Custom user model (`CustomUser`) with `freelancer` / `client` / `admin` roles
- Email OTP verification at signup (4-digit code emailed to the user)
- Skill selection during signup, backed by a shared `Skills` taxonomy
- Profile picture upload and LinkedIn ID field

**Job marketplace**
- Clients post jobs (title, budget, description, image, required skills)
- Freelancers browse/search jobs by keyword or filter by skill (`findwork`)
- Freelancers apply to jobs; clients view and accept applicants
- Accepting an application converts the `Job` into an `ActiveJob` (assigned to the freelancer) and auto-emails the freelancer
- "My Jobs" / "Active Jobs" (client side) and "My Work" / "Working Jobs" (freelancer side) dashboards
- Save/bookmark jobs for later (`SavedJob`)

**Active job workspace**
- Per-job dashboard shared by the client and assigned freelancer
- Built-in chat/messaging thread scoped to the job
- File attachments upload
- Freelancer work submissions
- Client-side payment request flow and Razorpay checkout integration
- Freelancer payout collection via the Razorpay Payouts API (bank contact + fund account creation)

**Networking**
- Directory of all freelancer/client profiles (`mynetwork`)
- Follow / unfollow other users, followers & following lists
- Public post feed (short status updates)
- Editable resume (personal info, experience, achievements) with a public resume view

**Other**
- Site-wide feedback/rating form
- Custom 404 error page
- Django admin configured for all core models

## 🏗️ Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 5.0 (Python) |
| Database | SQLite (`db.sqlite3`) |
| Payments | Razorpay (`razorpay`, plus raw REST calls for contacts/fund accounts/payouts), `paypalrestsdk` |
| Email | Django SMTP backend (Gmail) for OTP & notification emails |
| Frontend | Django templates, custom CSS/JS (`static/`) |
| Media | User-uploaded images/files served from `media/` |
| Config | `python-dotenv`-style `.env` file loaded manually in `settings.py` |

## 📁 Project structure

```
Skillnetz-Freelance-Marketplace/
├── Freelancer/            # Django project (settings, root URLs, WSGI/ASGI)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── skillnetz/             # Core app: auth, jobs, applications, payments, chat
│   ├── models.py          # CustomUser, Job, ActiveJob, Skills, JobApplication,
│   │                       # Message, PaymentApplication, Payment, Fileattachment,
│   │                       # Work, SavedJob, Feedback
│   ├── views.py           # Signup/OTP/login, job CRUD & search, dashboards,
│   │                       # chat, Razorpay payments/payouts, saved jobs, feedback
│   ├── urls.py
│   ├── utils.py           # OTP generation + email helpers
│   ├── admin.py
│   └── templates/         # home, signup, login, otp, findwork, findtalent,
│                           # job details/applications, dashboards, payments, about, 404
├── network/                # Networking app: profiles, posts, resumes, follows
│   ├── models.py           # profile, posts, Resume, SavedProfile, Skills
│   ├── views.py            # profile list/detail, follow/unfollow, posts, resume
│   ├── forms.py
│   ├── admin.py
│   └── templates/          # network, profile, followers/following, posts, resume
├── static/                 # Global CSS/JS and page-specific asset folders
├── media/                  # Uploaded profile pictures, job images, attachments
├── manage.py
├── requirements.txt
├── .env.example             # Template for required environment variables
└── db.sqlite3               # Default SQLite database
```

## 🚀 Getting started

### Prerequisites
- Python 3.10+ (Django 5.0 requirement)
- pip / virtualenv
- A Gmail account (or other SMTP provider) for sending OTP/notification emails
- A Razorpay account (test mode is fine) if you want to exercise the payment features

### 1. Clone and set up a virtual environment

```bash
git clone https://github.com/Code-By-Sid/Skillnetz-Freelance-Marketplace.git
cd Skillnetz-Freelance-Marketplace
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and fill in real values — **never commit your actual `.env`**:

```bash
cp .env.example .env
```

```
DJANGO_SECRET_KEY=your-secret-key
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

> Note: the repository currently ships an `.env` and a populated `db.sqlite3`. For any real or public deployment, remove/rotate those, add `.env` and `db.sqlite3` to `.gitignore`, and generate a fresh `DJANGO_SECRET_KEY`.

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for `/admin/`)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 🔑 Key URLs

| Path | Purpose |
|---|---|
| `/` | Home page |
| `/signup/`, `/signup/client/`, `/otp/` | Registration & OTP verification |
| `/login/`, `/logout/` | Authentication |
| `/findwork/` | Browse/search jobs (freelancers) |
| `/findtalent/` | Post a job (clients) |
| `/job/<id>` | Job detail & apply |
| `/job/<id>/applications/` | Review applicants (client) |
| `/myjobs/`, `/myjobs/active/` | Client's posted / active jobs |
| `/mywork/`, `/mywork/working/` | Freelancer's applications / active work |
| `/dashboard/<job_id>` | Shared workspace: chat, files, payments |
| `/jobs/saved/` | Bookmarked jobs |
| `/mynetwork/` | Browse other users |
| `/profile/<id>` | View a profile, follow/unfollow |
| `/posts/`, `/addpost/` | Community feed |
| `/edit/`, `/resume/<user_id>/` | Edit & view resume |
| `/aboutus/` | About page |
| `/admin/` | Django admin |

## ⚠️ Notes & known considerations

This looks like a student/portfolio project, so a few things are worth flagging before using it beyond local development:

- **Secrets in the repo**: an `.env` file and a pre-populated `db.sqlite3` are committed. Treat any keys inside as compromised and rotate them.
- **`DEBUG = True`** and **`ALLOWED_HOSTS = ['*']`** are hardcoded in `settings.py` — fine for local dev, unsafe for production.
- **CSRF exemption**: the `success` (payment confirmation) view is marked `@csrf_exempt`.
- **Payout flow**: `collect_money` makes direct, unauthenticated-looking REST calls to the Razorpay Payouts API with a hardcoded `account_number` — review and adapt before using with real funds.
- No automated test coverage beyond the default empty `tests.py` stubs in each app.

## 🤝 Contributing

Issues and pull requests are welcome. If you plan to work on payments or auth, please do so against a Razorpay **test** account and a disposable email account.

## 📄 License

No license file is currently included in the repository — treat the code as "all rights reserved" until a license is added.