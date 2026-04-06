# Parallel Life Tracker

Parallel Life Tracker is a Django web application that allows users to explore "what-if" life scenarios by creating and managing alternative life paths. Users can track milestones, reflect on decisions, and compare different life trajectories.

---

## Features

### User Management

* User registration, login, and logout
* Extended user profile with additional fields
* Editable profile with read-only username

### Parallel Lives

* Create, update, and delete parallel life scenarios
* Visibility control (Public, Private, Unlisted)
* Realism score with visual star representation
* Slug-based URLs for clean navigation

### Milestones

* Track progress within each life path
* Status updates (Planned, In Progress, Completed)
* Progress percentage tracking
* Read-only association with parent life

### Reflections

* Personal reflections tied to a life path
* Mood scoring system
* Privacy control (public/private reflections)

### Access Control

* Owner-only edit/delete permissions
* Private content hidden from other users
* Unauthorized access returns 403/404

### API (Django REST Framework)

* List parallel lives
* Retrieve single life
* Create new life via API

### Async Processing

* Welcome email sent asynchronously using Celery

### Testing

* 20+ unit tests covering models, views, and forms

### UI & UX

* Bootstrap styling
* Responsive layout
* Custom error pages (403, 404, 500)
* Custom template filter (realism stars)

---

## Technologies Used

* Python 3
* Django
* Django REST Framework
* PostgreSQL
* Celery
* Redis
* Bootstrap
* Whitenoise

---

## Deployment

The project is deployed on Azure.

You can access it through here: 
https://parallel-life-tracker-dk-gha3bbh2f7bmfpcr.polandcentral-01.azurewebsites.net/

## Installation & Setup (Local - Optional)

If you wish to run the project locally, follow these steps.

### 1. Clone the repository

```bash
git clone <repository-url>
cd parallel-life-tracker
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create `.env` file

Create a file named `.env` in the project root and add:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=your_database_name
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

### 5. Apply migrations

```bash
python manage.py migrate
```

---

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

---

### 7. Run the project

```bash
python manage.py runserver
```

---

## Running Tests

```bash
python manage.py test
```

---

## API Endpoints

* `/api/parallel-lives/` — List all parallel lives
* `/api/parallel-lives/<id>/` — Retrieve a specific life
* `/api/parallel-lives/create/` — Create a new life

---

## Access & Permissions

* Users can only modify their own content
* Private lives and reflections are hidden from other users
* Unauthorized actions are blocked with proper error responses

---

## Environment Configuration

* Sensitive data is stored using environment variables
* `.env` file is not included in the repository
* `.env.example` provides a template for setup

