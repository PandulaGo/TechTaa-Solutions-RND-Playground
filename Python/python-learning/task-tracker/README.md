# Task Tracker

A small full-stack app I built to learn the Python web stack (FastAPI, SQLAlchemy, PostgreSQL), React with TypeScript, and Docker. I come from a .NET background, so I kept a mapping of the concepts I already knew to their Python equivalents (see below).

## What it does

A simple task list: add a task, mark it done, edit it, delete it. The React frontend talks to a REST API backed by PostgreSQL.

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI, Pydantic |
| Database access | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Frontend | React + TypeScript (Vite) |
| Tests | pytest, FastAPI TestClient |
| Tooling | Docker, Docker Compose |

## Project structure

```
task-tracker/
  docker-compose.yml
  backend/
    Dockerfile
    requirements.txt
    alembic.ini
    app/
      main.py        # routes (list, create, update, delete)
      database.py    # engine, session, get_db dependency
      models.py      # SQLAlchemy table (Task)
      schemas.py     # Pydantic request/response shapes
    migrations/      # Alembic migration scripts
    tests/
      test_tasks.py
  frontend/
    src/App.tsx
```

## API

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/db-check` | Checks the database connection |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task (`{"title": "..."}`) |
| PUT | `/tasks/{id}` | Update `title` and/or `done` |
| DELETE | `/tasks/{id}` | Delete a task |

Interactive docs (Swagger) are available at http://localhost:8000/docs.

## Running it

### Option 1: Docker (API + database)

```
docker compose up --build
docker compose exec api alembic upgrade head
```

The API is then available at http://localhost:8000.

### Option 2: Local development (API outside Docker)

Start only the database, then run the API with a virtual environment.

```
docker compose up -d db

cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate         # macOS / Linux
python -m pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```

### Frontend

```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The API must be running, and CORS is configured to allow this origin.

## Database migrations

```
alembic revision --autogenerate -m "describe the change"   # create a migration
alembic upgrade head                                        # apply migrations
alembic downgrade -1                                        # undo the last one
```

Alembic reads the SQLAlchemy models through `Base.metadata` (set in `migrations/env.py`), compares them with the database, and generates a versioned script.

## Tests

```
cd backend
python -m pytest -v
```

The tests use a temporary SQLite database, so they never touch the PostgreSQL data. Each test starts with empty tables.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg2://app:app@localhost:5432/tasks` | Database connection string |

In Docker Compose the host is `db` (the service name) instead of `localhost`. The credentials here are for local development only. In a real deployment, secrets would come from the environment or a secrets manager, never from the code.

## Design notes

- **Models and schemas are separate.** The SQLAlchemy model is the database table. The Pydantic schemas define what the API accepts and returns, so internal fields are never exposed by accident.
- **One database session per request**, provided through FastAPI dependency injection (`Depends(get_db)`).
- **Validation is automatic.** Invalid input (for example, an empty title) returns a 422 response without extra code.
- **Missing records return 404.**
- **The API waits for the database health check** before starting in Docker Compose.

## Coming from .NET: concept mapping

| .NET | This project |
|---|---|
| ASP.NET Core | FastAPI |
| Dependency injection | `Depends()` |
| DTOs and validation attributes | Pydantic schemas |
| EF Core, `DbContext` | SQLAlchemy, `Session` |
| EF migrations | Alembic |
| xUnit, `WebApplicationFactory` | pytest, `TestClient` |
| NuGet | pip, `requirements.txt` |
| `appsettings` and configuration | Environment variables |

## Known limitations and next steps

- Error and loading states in the frontend (a failed request currently shows an empty list)
- Authentication
- Pin dependency versions in `requirements.txt`
- Continuous integration to run the tests on every push
- Background jobs with Redis (for example, reminder emails)
- Browser tests with Playwright
- Deploy to AWS (container service plus managed PostgreSQL)
