# SynapseOps

Starter repository for a Google Cloud agent system built from these codelab tracks:

- ADK foundation and local development
- ADK deployment to Cloud Run
- MCP-based BigQuery and Google Maps tooling
- MCP Toolbox for Databases with BigQuery datasets
- AlloyDB setup and AlloyDB AI integration patterns

This repo starts with a Python-first layout that can grow into a multi-agent operations platform. The current scaffold gives you:

- a Cloud Run-friendly FastAPI entrypoint
- an ADK root agent factory
- read-only BigQuery and AlloyDB tool wrappers
- MCP server registry placeholders for BigQuery Toolbox and Maps
- environment-driven configuration

## Project Layout

```text
app/
	agents/        ADK agent factories
	api/           FastAPI service surface
	db/            AlloyDB access layer
	integrations/  BigQuery and cloud service clients
	mcp/           MCP server registry and metadata
	schemas/       Request and response models
	services/      Bootstrap and orchestration helpers
	utils/         Shared utilities
	workflows/     Workflow definitions and roadmap metadata
```

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies.
3. Copy `.env.example` to `.env` and fill in your Google Cloud values.
4. Authenticate for local development with Application Default Credentials.
5. Start the local API.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
gcloud auth application-default login
python -m app.main
```

The service starts on `http://127.0.0.1:8000` by default.

## Lab Mapping

- ADK Foundation: `app/agents/root_agent.py` defines the initial agent contract and local tool wiring.
- ADK Cloud Run Deployment: `deployment/Dockerfile` and `app/main.py` provide the service bootstrap path.
- ADK + MCP + BigQuery + Maps: `app/mcp/registry.py` and `app/integrations/bigquery_client.py` establish the starter integration points.
- MCP Toolbox for Databases: `MCP_BIGQUERY_TOOLBOX_URL` in `.env.example` is the handoff point for a remote MCP toolbox endpoint.
- AlloyDB setup and AI app labs: `app/db/alloydb.py` and `ALLOYDB_*` env vars prepare the relational and AI-data layer.

## Current Endpoints

- `GET /` basic service metadata
- `GET /health` health response and configured integrations
- `GET /mcp/servers` MCP server registry snapshot
- `POST /agent/chat` simple agent endpoint (Gemini-backed when configured, fallback otherwise)
- `POST /bigquery/query` execute a read-only BigQuery query
- `POST /alloydb/query` execute a read-only AlloyDB query

## Cloud Run Starter

Build and run locally with Docker:

```powershell
docker build -f deployment/Dockerfile -t synapseops .
docker run --env-file .env -p 8080:8080 synapseops
```

The container listens on `PORT`, which defaults to `8080` in Cloud Run.

## Next Build-Out

- replace placeholder MCP URLs with real BigQuery Toolbox and Maps endpoints
- add ADK session management and streaming responses
- add AlloyDB AI SQL workflows for semantic retrieval and recommendation logic
- add Cloud Build or GitHub Actions deployment automation

See `docs/lab-mapping.md` for the architecture notes derived from the codelabs.

