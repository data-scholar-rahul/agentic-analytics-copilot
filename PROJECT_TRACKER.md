# Agentic Analytics Copilot Tracker


# Sprint 1: Backend Foundation

## Sprint Log

### Sprint 1: Backend Foundation

Status: In progress

Goal:
- Create FastAPI backend skeleton
- Add config loading from .env
- Add Basic Auth
- Add /health endpoint
- Add /ask endpoint with dummy response

## Mental Models

### FastAPI
Backend API layer that receives requests from frontend and returns structured responses.

### pyproject.toml
Python project metadata, dependencies, and tooling config.

### .env
Local runtime configuration and secrets. Must not be committed.

### Pydantic request and response models
Request models define incoming JSON body shape.
Response models define outgoing API response shape.

## Decisions Locked

- Backend: FastAPI
- Database: PostgreSQL
- Frontend: Next.js
- LLM provider: OpenAI
- Auth for MVP: Basic Auth
- Config: .env plus pydantic-settings

## Questions / Confusions

## Mistakes and Fixes

## Code Files and Responsibilities

- backend/app/main.py:
- backend/app/api/routes.py:
- backend/app/api/auth.py:
- backend/app/core/config.py:
- backend/app/schemas/ask.py:
- backend/app/schemas/responses.py:
- backend/.env:
- backend/pyproject.toml:

Sprint 2 Understanding

1. psycopg
What it is:
Why we need it:

2. Database connection string
What it is:
Example:
What can go wrong:

3. Connection vs cursor
Connection:
Cursor:

4. fetchall
What it does:
When it can be risky:

5. postgres_client.py
Why DB code belongs here:

6. routes.py
What routes.py should do:
What routes.py should not do:

7. Resource handling
What happens if connections are not closed:

8. My Sprint 2 mental model
/ask request → auth → route → PostgresClient → query → rows → AskResponse