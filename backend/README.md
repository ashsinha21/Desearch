# DESearch Backend

A FastAPI-based search service for programming questions with Meilisearch and PostgreSQL.

## Features

- Full-text search with filters
- Metrics and analytics
- Extensible crawler system
- RESTful API

## Prerequisites

- Python 3.11
- PostgreSQL 13+
- Meilisearch 1.0+
- Docker (optional)

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`
5. Run database migrations (Alembic will be added in a future update)
6. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Running with Docker

```bash
docker-compose up --build
```

## API Endpoints

- `GET /` - Health check
- `GET /api/search?q=query` - Search questions
- `GET /api/metrics` - Get search metrics

## Development

- Format code with Black and isort:
  ```bash
  black .
  isort .
  ```

## License

MIT
