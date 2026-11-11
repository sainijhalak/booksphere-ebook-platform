# 📚 BookSphere – Full-Stack eBook Web Application

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20.svg)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57.svg)](https://www.sqlite.org/)
[![HTML5](https://img.shields.io/badge/Frontend-HTML5-E34F26.svg)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![CSS3](https://img.shields.io/badge/Styles-CSS3-1572B6.svg)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/Scripting-Vanilla%20JS-F7DF1E.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

> **BookSphere** is an organized full-stack eBook web application engineered for reading communities, students, and engineers. It features a RESTful Django backend handling authentication, book inventory CRUD, and user reading lists, backed by SQLite, alongside a modern mobile-responsive frontend written in pure HTML5, CSS3, and Vanilla JavaScript.

---

## 🌟 Key Features & Architecture

- 📖 **Curated eBook Catalog**: Browse foundational engineering, AI, finance, and science texts with multi-faceted search (title, author, synopsis), category domain chips, and dynamic sorting.
- 🔐 **Authentication & Security**: Django authentication system supporting secure registration, session-based login, CSRF tokens, password validation, and user profile isolation.
- ⚡ **RESTful API Backend**:
  - `GET /api/books/` – Search, filter, and paginate catalog in JSON format.
  - `GET /api/books/<id>/` – Detailed resource representation.
  - `POST /api/books/<id>/bookmark/` – Asynchronous toggle to save books to the user's reading list without page reloads.
- 📝 **Resource Management & CRUD**:
  - Add new eBooks with validation (`/books/new/`).
  - Delete or modify books with staff permissions.
  - Submit 5-star ratings and long-form reviews with real-time aggregate scoring.
- 🎨 **Responsive Frontend (HTML5 / CSS3 / Vanilla JS)**:
  - Custom responsive layout with CSS Grid & Flexbox (mobile, tablet, desktop).
  - Chapter 1 Sample Excerpt Reader modal with vanilla JS backdrop and keyboard escape listeners.
  - Asynchronous fetch API for bookmark toggles.
  - Auto-dismissing flash message alerts.

---

## 🏗️ System Architecture

```
                  ┌──────────────────────────────────────────┐
                  │       HTML5 / CSS3 / Vanilla JS UI       │
                  │   (Catalog Grid, Reader Modal, Forms)    │
                  └─────────────┬────────────────────────────┘
                                │
               HTTP Requests    │    Async Fetch (REST API)
                                ▼
                  ┌──────────────────────────────────────────┐
                  │              Django Backend              │
                  │    (Auth, Views, RESTful API Endpoints)  │
                  └─────────────┬────────────────────────────┘
                                │
                                ▼
                  ┌──────────────────────────────────────────┐
                  │            SQLite Data Layer             │
                  │  (Books, Categories, Reviews, Libraries) │
                  └──────────────────────────────────────────┘
```

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/sainijhalak/booksphere-ebook-platform.git
cd booksphere-ebook-platform

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Database Migrations & Seed Sample Catalog
```bash
python manage.py makemigrations books
python manage.py migrate
python manage.py seed_books
```
*Pre-configured demo credentials:*  
- **Username:** `jhalak`  
- **Password:** `demo12345`

### 3. Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```
Open your browser at `http://127.0.0.1:8000` to explore the catalog and REST API (`http://127.0.0.1:8000/api/books/`).

---

## 🎯 Technical Interview Talking Points

1. **Why Pure Vanilla JS and CSS3 instead of React?**  
   For a content-heavy eBook application, minimizing client-side bundle size is paramount. Pure HTML5 and CSS3 deliver sub-50ms First Contentful Paint (FCP) and near-zero JavaScript parsing overhead, while asynchronous `fetch()` delivers modern dynamic reactivity for bookmarks and modals.
2. **RESTful Architecture in Django:**  
   The application cleanly separates standard Server-Side Rendered (SSR) views for SEO-friendly page discovery with decoupled JSON endpoints (`/api/books/`) for programmatic resource access and headless clients.
3. **Relational Schema Design & SQLite:**  
   The schema leverages Django ORM relations (`ForeignKey`, `UniqueTogether`) to maintain integrity between `User`, `Book`, `Review`, and `UserLibrary`, ensuring users cannot submit duplicate bookmarks and that book deletion cascades cleanly.

---

## 📄 License
MIT License. Created by Jhalak Saini.
