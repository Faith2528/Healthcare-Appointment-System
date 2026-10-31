# Healthcare AppointmentSystem

A web-based healthcare management platform designed to streamline patient scheduling, eliminate scheduling conflicts, and manage clinic workflows efficiently.

---

## Key Features

- **Smart Appointment Validation:** Prevents double-booking and enforces clinic daily booking capacity limits.
- **Automated Billing Breakdown:** Dynamically calculates itemized billing breakdowns for consultations and procedures.
- **Real-Time Email Notifications:** Automatically notifies patients regarding appointment confirmations, cancellations, and status updates.
- **Multi-Role Workflows:** Dedicated portals and views for patients, doctors, and clinic administrators.

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (migrated from initial Firebase prototype for enhanced schema validation and relational integrity)
- **Frontend:** HTML5, CSS3, JavaScript
- **Services:** SMTP / Email Service Integration

---

## Project Architecture & Evolution

1. **Phase 1 (Proof-of-Concept):** Built an initial prototype using HTML, CSS, JavaScript, and Firebase to test and validate end-to-end patient booking workflows.
2. **Phase 2 (Relational Migration & Production Logic):** Migrated backend architecture to Django and SQLite to guarantee data integrity, eliminate overlapping schedules, and enforce granular business rules.

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- `pip` and `virtualenv`

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <YOUR_REPO_URL>
   cd EHR-main
   ```

2. **Create and activate a virtual environment:**
  ```bash
  # Windows
  python -m venv venv
  venv\Scripts\activate

  # Linux/macOS
  python3 -m venv venv
  source venv/bin/activate
   ```

3. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
   ```

4. **Configure environment variables:**
  Copy the sample environment file and provide your email and database configurations:

  ```bash
  cp .env.sample .env
   ```

5. **Run database migrations:**
  ```bash
  python manage.py migrate
   ```

6. **Start the development server:**
```bash
  python manage.py runserver
```

7. **Visit http://127.0.0.1:8000/ in your browser.**


