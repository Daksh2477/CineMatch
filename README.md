# CineMatch

CineMatch is a full-stack movie discovery and recommendation platform built with React, Django REST Framework, SQLite, and scikit-learn.

## Features

- Search and filter movies
- View movie details
- Receive content-based, genre, popularity, and hybrid recommendations
- Create a personal watchlist
- Rate movies
- Review recommendation history

## Technology Stack

- Frontend: React, Vite, JavaScript, CSS
- Backend: Python, Django, Django REST Framework
- Machine learning: Pandas, NumPy, scikit-learn, TF-IDF, cosine similarity
- Database: SQLite
- Testing: pytest, Django test runner, Vitest
- CI: GitHub Actions

## Project Structure

```text
CineMatch/
├── backend/
├── frontend/
├── docs/
├── .github/workflows/
└── screenshots/
```

## Development Setup

### Prerequisites

- Python 3.12 or newer
- Node.js 20 or newer
- npm
- Git

### Backend

```powershell
cd backend
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

The frontend uses `VITE_API_BASE_URL`, defaulting to `http://127.0.0.1:8000/api`.

## Dataset

The application ships with a small, curated sample dataset so it can run immediately. Dataset ingestion is also designed for MovieLens-compatible CSV files. Official sources and import instructions are documented in `docs/ML_EXPLANATION.md`.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API documentation](docs/API_DOCUMENTATION.md)
- [Machine learning](docs/ML_EXPLANATION.md)
- [Development log](docs/DEVELOPMENT_LOG.md)
- [Contributing](CONTRIBUTING.md)
