# Agentic Analytics Copilot Tracker

## Current Sprint

Sprint 1: Backend Foundation

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

## Business / Domain Notes

## Next Actions
