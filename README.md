# TaskFlow

> An end-to-end DevOps learning project: a FastAPI task management API backed by PostgreSQL, containerized with Docker Compose, versioned with Alembic, and validated by a GitHub Actions CI pipeline.

[![CI](https://github.com/sanjayadanushka712/TaskFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/sanjayadanushka712/TaskFlow/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Ruff](https://img.shields.io/badge/lint-Ruff-D7FF64?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)

---

## Overview

TaskFlow is a small but complete CRUD service built to demonstrate the full lifecycle of a modern Python application:

- **Application:** FastAPI + Pydantic request validation
- **Persistence:** PostgreSQL + SQLAlchemy 2
- **Schema management:** Alembic migrations
- **Runtime:** Docker + Docker Compose with health checks
- **Quality:** Ruff linting/formatting and Pytest
- **Automation:** GitHub Actions for migrations, tests, and container builds
- **Client:** A Python CLI (`main.py`) and a REST API (`api.py`)

The API includes idempotent task creation through the `Idempotency-Key` header, which prevents duplicate work when clients retry requests.

---

## Features

- Create, read, update, complete, and delete tasks
- Strict request validation with Pydantic
- Idempotent `POST /tasks` using a persisted idempotency key and request hash
- PostgreSQL-backed idempotency records
- Alembic migration history for reproducible schemas
- Docker Compose stack with a private network, named volume, and health checks
- Non-root application container
- Automated linting, formatting checks, migrations, tests, and Docker image builds in CI
- Interactive OpenAPI docs at `/docs` and `/redoc`
- Simple terminal client for local use

---

## Architecture

```mermaid
flowchart LR
    Client[Client / curl / Swagger] --> API[FastAPI API]
    CLI[Python CLI] --> Service[Taskflow service]
    API --> Service

    Service --> ORM[SQLAlchemy]
    ORM --> DB[(PostgreSQL 17)]

    Compose[Docker Compose] -.-> API
    Compose -.-> DB

    Dev[Developer] -->|push / pull request / tag| CI[GitHub Actions]
    CI --> Lint[Ruff]
    CI --> Tests[Pytest against PostgreSQL]
    CI --> Image[Docker image build]
```

### Request flow

1. A request reaches FastAPI in `api.py`.
2. Pydantic validates the payload.
3. The route calls the `Taskflow` service in `app.py`.
4. SQLAlchemy translates the operation into SQL for PostgreSQL.
5. Alembic keeps the database schema aligned with `models.py`.

---

## Tech stack

| Layer | Tool | Purpose |
| --- | --- | --- |
| Language | Python 3.14 | Application runtime |
| API | FastAPI | HTTP endpoints and OpenAPI docs |
| Validation | Pydantic 2 | Request/response validation |
| ORM | SQLAlchemy 2 | Database access |
| Driver | psycopg 3 | PostgreSQL adapter |
| Database | PostgreSQL 17 | Persistent storage |
| Migrations | Alembic | Versioned schema changes |
| Tests | Pytest + HTTPX | Unit, API, and database tests |
| Lint/format | Ruff | Code quality and formatting |
| Containers | Docker + Compose | Reproducible local environment |
| CI/CD | GitHub Actions | Automated verification and image builds |

---

## Project structure

```text
TaskFlow/
├── api.py                     # FastAPI application and routes
├── app.py                     # Taskflow service layer
├── main.py                    # Interactive CLI
├── database.py                # Engine and session factory
├── models.py                  # SQLAlchemy models
├── create_tables.py           # Legacy quick schema bootstrap
├── alembic.ini                # Alembic configuration
├── migrations/
│   ├── env.py                 # Runtime migration environment
│   └── versions/              # Versioned schema migrations
├── test/
│   ├── test_api.py            # API tests, including idempotency
│   ├── test_app.py            # Service-layer tests
│   └── test_database.py       # Database integration tests
├── .github/workflows/ci.yml   # CI pipeline
├── compose.yaml               # API + PostgreSQL stack
├── Dockerfile                 # Non-root application image
├── requirements.txt           # Runtime dependencies
├── requirements-dev.txt       # Test and lint dependencies
├── pyproject.toml             # Ruff and Pytest configuration
├── .env.example               # Environment template
└── README.md
```

---

## Quick start with Docker Compose

### Prerequisites

- Docker Engine 24+
- Docker Compose v2+
- `curl` (optional, for smoke testing)

### 1. Configure the environment

```bash
cp .env.example .env
```

The defaults in `.env.example` are ready for local use:

```dotenv
POSTGRES_USER=taskflow
POSTGRES_PASSWORD=taskflow_dev
POSTGRES_DB=taskflow
POSTGRES_PORT=5433
API_PORT=8000
DATABASE_URL=postgresql+psycopg://taskflow:taskflow_dev@db:5432/taskflow
```

> The API container uses the internal hostname `db`. If you run the API directly on your host, use `localhost:${POSTGRES_PORT}` instead.

### 2. Start the stack

```bash
docker compose up --build -d
```

On startup, the API container runs `alembic upgrade head` before launching Uvicorn. The database is exposed on host port `5433` by default to avoid clashes with a local PostgreSQL server.

### 3. Verify

```bash
docker compose ps
curl http://localhost:8000/
```

Expected response:

```json
{"message":"TaskFlow API is running"}
```

Open the interactive docs:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### 4. View logs and stop

```bash
docker compose logs -f api
docker compose down
```

To remove the database volume as well:

```bash
docker compose down -v
```

---

## Local development

### Prerequisites

- Python 3.14
- PostgreSQL 17 (or use the Compose database on port `5433`)
- A database and user matching your `DATABASE_URL`

### 1. Create a virtual environment

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Start PostgreSQL

Use your local server or start only the database container:

```bash
docker compose up -d db
```

### 3. Point the app at the database

For a locally running API:

```bash
export DATABASE_URL="postgresql+psycopg://taskflow:taskflow_dev@localhost:5433/taskflow"
```

If you use a local PostgreSQL instance, replace the host, port, user, password, and database name as needed.

### 4. Apply migrations

```bash
alembic upgrade head
```

### 5. Run the API

```bash
uvicorn api:app --reload
```

### 6. Run the CLI (optional)

```bash
python main.py
```

The CLI talks directly to the database through the `Taskflow` service.

---

## Configuration

| Variable | Default | Used by | Description |
| --- | --- | --- | --- |
| `POSTGRES_USER` | `taskflow` | `db` | PostgreSQL user |
| `POSTGRES_PASSWORD` | `taskflow_dev` | `db` | PostgreSQL password |
| `POSTGRES_DB` | `taskflow` | `db` | PostgreSQL database name |
| `POSTGRES_PORT` | `5433` | Compose | Host port mapped to PostgreSQL |
| `API_PORT` | `8000` | Compose | Host port mapped to the API |
| `DATABASE_URL` | see `.env.example` | API, Alembic, tests | SQLAlchemy connection string |

**Important:** `.env` is ignored by Git. Never commit real credentials.

---

## API reference

Base URL: `http://localhost:8000`

| Method | Path | Description | Success |
| --- | --- | --- | --- |
| `GET` | `/` | Health check | `200` |
| `POST` | `/tasks` | Create a task | `201` |
| `GET` | `/tasks` | List all tasks | `200` |
| `GET` | `/tasks/{task_id}` | Get one task | `200` |
| `PUT` | `/tasks/{task_id}` | Update a task title | `200` |
| `PATCH` | `/tasks/{task_id}/complete` | Mark a task complete | `200` |
| `DELETE` | `/tasks/{task_id}` | Delete a task | `200` |

### Create a task

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: create-task-001" \
  -d '{"task_id": 1, "title": "Learn Docker"}'
```

```json
{"id":1,"title":"Learn Docker","completed":false}
```

### List tasks

```bash
curl http://localhost:8000/tasks
```

```json
[
  {"id": 1, "title": "Learn Docker", "completed": false}
]
```

### Get a task

```bash
curl http://localhost:8000/tasks/1
```

### Update a task title

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Advanced Docker"}'
```

### Complete a task

```bash
curl -X PATCH http://localhost:8000/tasks/1/complete
```

### Delete a task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

### Idempotent creation

Send an `Idempotency-Key` header with `POST /tasks`:

| Scenario | Result |
| --- | --- |
| First request with a key | Task is created, `201` |
| Retry with the same key and same payload | Original response is replayed, `201` |
| Same key with a different payload | `409 Conflict` |
| Duplicate `task_id` without a key | `409 Conflict` |

Idempotency records are stored in the `idempotency_records` table with a SHA-256 hash of the normalized request body.

---

## Database and migrations

Alembic is the source of truth for the schema. The migration chain is:

1. `dc9d6a45afb7` - initial `tasks` and `idempotency_records` tables
2. `f4689dfad058` - nullable `tasks.description` column

Common commands:

```bash
alembic upgrade head
alembic downgrade -1
alembic current
alembic history
alembic revision --autogenerate -m "describe change"
```

After changing `models.py`, generate a migration, review the generated file, and commit it with the model change.

`create_tables.py` remains available as a legacy quick bootstrap, but Alembic is recommended for all environments.

---

## Testing and code quality

Run the same checks used by CI:

```bash
ruff check .
ruff format --check .
pytest -q
```

Apply formatting automatically:

```bash
ruff format .
```

The tests require a reachable PostgreSQL database with the migrations applied:

```bash
export DATABASE_URL="postgresql+psycopg://taskflow:taskflow_dev@localhost:5433/taskflow"
alembic upgrade head
pytest -q
```

Test coverage includes:

- Service-layer CRUD behavior
- API validation, status codes, and error paths
- Idempotent creation and concurrent retry handling
- Database constraints and transaction behavior

---

## CI pipeline

The workflow lives in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and runs on:

- Pushes to `main`
- Pull requests targeting `main`
- Tags matching `v*`

| Stage | What it does |
| --- | --- |
| Checkout | Fetches the repository |
| Set up Python | Installs Python 3.14 with pip caching |
| Install dependencies | Installs `requirements-dev.txt` |
| Apply migrations | Runs `alembic upgrade head` against PostgreSQL 17 |
| Lint | Runs `ruff check .` |
| Format check | Runs `ruff format --check .` |
| Tests | Runs the full Pytest suite |
| Docker build | Builds the application image with Buildx and GitHub Actions cache |

The Docker job only runs after the test job succeeds.

---

## Docker details

- The API runs as a non-root `app` user.
- PostgreSQL data persists in the `taskflow-data` named volume.
- The API waits for the database health check before starting.
- Both services share the private `taskflow-net` bridge network.
- The API container applies pending migrations on startup.
- Health checks are defined for both services.

Useful commands:

```bash
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f
docker compose exec db psql -U taskflow -d taskflow
docker compose down
```

---

## Releasing a new version

```bash
git checkout main
git pull
git tag -a v1.0.0 -m "TaskFlow v1.0.0"
git push origin main
git push origin v1.0.0
```

Tag pushes trigger the same CI pipeline, which validates the release commit and builds the container image.

---

## Troubleshooting

### Port already in use

Change the host ports in `.env`:

```dotenv
API_PORT=8001
POSTGRES_PORT=5434
```

Then restart:

```bash
docker compose up -d
```

### API cannot connect to PostgreSQL

1. Check the database health: `docker compose ps`
2. Read the logs: `docker compose logs db`
3. Confirm the API uses `db:5432` inside Compose, not `localhost`
4. Confirm `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` match `DATABASE_URL`

### Alembic says a table already exists

This can happen if `create_tables.py` created the schema before Alembic was introduced. For a disposable local database, remove the volume and start again:

```bash
docker compose down -v
docker compose up --build -d
```

For a database you want to keep, inspect the schema and use `alembic stamp` only after confirming it matches the target revision.

### A retry returns `409 Conflict`

- If the payload changed, use a new `Idempotency-Key`.
- If no key was supplied, `task_id` must be unique.

---

## Security notes

- `.env` is ignored and must never be committed.
- Development credentials in `.env.example` are placeholders; rotate them outside local development.
- The container runs as a non-root user.
- The API currently has no authentication or authorization. Add an auth layer and TLS termination before exposing it to the public internet.
- Revoke any credential that has ever been pasted into a terminal, issue, or chat.

---

## Contributing

1. Create a feature branch: `git checkout -b feature/my-change`
2. Make the change and add or update tests.
3. Run `ruff check .`, `ruff format --check .`, and `pytest -q`.
4. Open a pull request against `main`.

---

## Author

**Sanjaya Danushka** - [@sanjayadanushka712](https://github.com/sanjayadanushka712)

Built as an end-to-end DevOps practice project covering Python, PostgreSQL, containers, migrations, testing, and CI automation.
