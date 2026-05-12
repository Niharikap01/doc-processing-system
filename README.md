# DocAI — Intelligent Document Processing System

A full-stack real-time document processing platform built using FastAPI, React, PostgreSQL, Redis, Celery, and WebSockets.

---

# Features

- Upload PDF documents
- Real-time processing updates
- Background task processing using Celery
- Redis Pub/Sub live events
- WebSocket live status updates
- Extract text from PDF files
- Review and edit extracted data
- Finalize processed documents
- Export JSON and CSV
- Modern responsive UI

---

# Tech Stack

## Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Celery
- WebSockets
- Docker
- PyMuPDF (fitz)
## Frontend
- React
- TypeScript
- Tailwind CSS
- Vite

---

# Architecture

Frontend → FastAPI → Celery Worker → Redis → PostgreSQL
# Real-Time Processing Flow

1. User uploads PDF document
2. FastAPI stores document metadata
3. Background processing starts using Celery
4. Redis Pub/Sub streams live events
5. WebSocket pushes real-time updates to frontend
6. Extracted data is stored in PostgreSQL
7. User can review, edit, finalize, and export results
---

# Installation

## Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

---

## Celery Worker

```bash
celery -A app.core.celery_app.celery_app worker --pool=solo --loglevel=info
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# Future Improvements

- OCR support for scanned documents
- AI summarization
- Authentication system
- Role-based access
- Cloud deployment

---

# Author

Niharika Pareek
