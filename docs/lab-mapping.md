# Lab Mapping Notes

## ADK Foundation

Use the ADK foundation lab as the local development baseline:

- Python virtual environment
- local auth with ADC or API key
- one root agent with a clear instruction contract
- iterative local testing before deployment

Mapped files:

- `app/agents/root_agent.py`
- `app/main.py`

## ADK to Cloud Run

Use the Cloud Run deployment lab as the runtime target:

- HTTP service entrypoint
- environment-based configuration
- containerized deployment
- Vertex AI credentials through the runtime environment

Mapped files:

- `deployment/Dockerfile`
- `app/main.py`
- `app/config.py`

## ADK + MCP + BigQuery + Maps

Use the BigQuery and Maps lab as the tool orchestration pattern:

- agent delegates analytics work to tools
- remote MCP servers are represented as external capabilities
- BigQuery remains read-only for analytics workloads

Mapped files:

- `app/mcp/registry.py`
- `app/integrations/bigquery_client.py`
- `app/agents/root_agent.py`

## MCP Toolbox for Databases

Use the toolbox lab as the contract for exposing BigQuery datasets to MCP clients:

- keep the toolbox external to the app
- configure its URL through environment variables
- preserve a clear boundary between app logic and dataset exposure

Mapped files:

- `.env.example`
- `app/mcp/registry.py`

## AlloyDB Setup and AI App

Use the AlloyDB labs as the data-plane direction:

- PostgreSQL-compatible transactional storage
- secure connector-based access
- AI functions and embeddings can move closer to SQL later
- Cloud Run remains a valid application host

Mapped files:

- `app/db/alloydb.py`
- `.env.example`
- `app/workflows/synapse_flow.py`

## Recommended Sequence

1. Fill in `.env` and verify BigQuery access locally.
2. Stand up the MCP Toolbox for BigQuery and add its endpoint.
3. Create the first remote Maps MCP server entry.
4. Provision AlloyDB and validate a read-only query through the connector.
5. Expand the ADK root agent into multiple specialized agents.
