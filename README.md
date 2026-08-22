# Tech Blog — Full-Stack Web Application

A full-stack technology blog built with FastAPI, Next.js, PostgreSQL, Redis, and Alembic.

The project provides a modern platform for publishing and reading technical articles, with authentication, email verification, API rate limiting, and background email processing.

### 🚀 Tech Stack
- Frontend: Next.js
- Backend: FastAPI
- Database: PostgreSQL
- Cache & Persistent Storage: Redis
- Database Migrations: Alembic
- Email Service: Resend
- Background Tasks: Redis Queue
- Authentication: Token-based authentication
- API Rate Limiting: IP-based rate limiting backed by Redis

### 🏗️ Architecture
```text
┌─────────────────┐
│    Next.js      │
│    Frontend     │
└────────┬────────┘
         │ HTTP / API
         ▼
┌─────────────────┐
│     FastAPI     │
│     Backend     │
└───────┬─┬───────┘
        │ │
        │ └──────────────────┐
        ▼                    ▼
┌───────────────┐     ┌───────────────┐
│  PostgreSQL   │     │     Redis     │
│   Database    │     │ Rate Limiting │
└───────────────┘     │  + Job Queue  │
                      └───────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │    Resend    │
                       │ Email Service│
                       └──────────────┘
```

### ✨ Features
- 📝 Technology blog and article publishing
- 🔐 User authentication
- ✉️ Email verification
- 🚦 IP-based API rate limiting
- 🔴 Redis-backed rate-limit storage
- ⚙️ Background email tasks using Redis
- 📬 Email delivery through Resend
- 🗄️ PostgreSQL persistence
- 🔄 Database migrations with Alembic
- ⚡ FastAPI backend
- ⚛️ Next.js frontend
- 🧩 Modular backend architecture

### 📁 Project Structure
```text
igital_frontier/
│
├── blog_backend/
│   ├── alembic/
│   │   └── ...
│   │
│   ├── app/
│   │   ├── api/
│   │   │   └── ...
│   │   ├── core/
│   │   │   └── ...
│   │   ├── db/
│   │   │   └── ...
│   │   ├── models/
│   │   │   └── ...
│   │   ├── schemas/
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── ...
│   │   ├── tasks/
│   │   │   └── ...
│   │   └── main.py
│   │
│   ├── .env
│   ├── alembic.ini
│   └── requirements.txt
│
├── blog_frontend/
│   ├── public/
│   │   └── ...
│   │
│   ├── src/
│   │   ├── app/
│   │   │   └── ...
│   │   ├── components/
│   │   │   └── ...
│   │   ├── lib/
│   │   │   └── ...
│   │   └── types/
│   │       └── ...
│   │
│   ├── .env.local
│   ├── package.json
│   └── package-lock.json
│
└── README.md
```

### 🔴 Redis Usage
Redis is used for more than traditional caching in this project.

#### 1. IP Rate Limiting

Redis provides persistent storage for rate-limit data. Incoming requests are tracked by IP address, allowing the API to limit excessive requests without relying on in-memory application state.

This makes rate limiting more reliable when running multiple backend instances.

#### 2. Background Job Queue

Redis is also used as a queue for background tasks.

When a user registers, the API does not need to wait for the email service to finish sending the verification email. Instead, an email job is added to the Redis queue.

A background worker consumes the job and sends the email through Resend.

```text
User Registration
       │
       ▼
   FastAPI API
       │
       ▼
 Add email job
       │
       ▼
     Redis
       │
       ▼
 Background Worker
       │
       ▼
     Resend
       │
       ▼
Verification Email
```

This keeps API requests fast and prevents email delivery from blocking the main request.

### 🗄️ Database Migrations

The project uses Alembic to manage PostgreSQL schema changes.

Typical migration workflow:

Create a migration
```bash
alembic revision --autogenerate -m "describe change"
```

Apply migrations
```bash
alembic upgrade head
```

Roll back the latest migration
```bash
alembic downgrade -1
```

### 🎯 Project Goals

The project was built to explore how a modern full-stack application can combine:

- FastAPI for a high-performance backend
- Next.js for the frontend
- PostgreSQL for relational data
- Redis for rate limiting and job queues
- Alembic for database migrations
- Resend for transactional email
- Background workers for asynchronous processing

The main goal is to build a production-oriented architecture rather than a simple CRUD blog.