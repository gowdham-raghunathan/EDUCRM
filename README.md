# EduCRM Admission CRM

This workspace now contains a modern admissions CRM starter with:
- React + Bootstrap 5 frontend
- FastAPI backend APIs
- SQLAlchemy models and SQLite-backed schema
- Lead, follow-up, CTI, WhatsApp, and dashboard endpoints

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Backend

```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic
uvicorn main:app --reload
```

## API Docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
