=========================================================
  python-adtech-mcp-server  —  Build & Deploy Guide
  Python / FastAPI — Tool Provider Service
=========================================================

WHAT THIS SERVICE DOES
  Exposes 23 AdTech tools as REST endpoints so any AI agent
  (python-adtech-mcp-client or Java adtech-mcp-client) can
  discover and call them via HTTP.

  GET  /mcp/tools              — returns 23 tool definitions
  POST /mcp/tools/{toolName}   — executes a tool with given args
  GET  /mcp/health             — health check + tool count
  GET  /docs                   — FastAPI Swagger UI

  No AI logic. No database. Pure tool-provider service.
  Deploy this FIRST before python-adtech-mcp-client.

=========================================================
  DIFFERENCE FROM JAVA adtech-mcp-server
=========================================================

  Java (adtech-mcp-server)            Python (python-adtech-mcp-server)
  ─────────────────────────────       ────────────────────────────────────
  Spring Boot 3.2 / Java 21           FastAPI / Python 3.11
  ToolRegistry.java (records)         tool_registry.py (dataclasses)
  ToolDispatcher.java (switch)        tool_dispatcher.py (match statement)
  9 separate @Component classes       9 plain Python modules
  KnowledgeBaseClient (Java SDK)      knowledge_base_api.py (Python SDK)
  Port 8081                           Port 8082
  No /docs endpoint                   /docs (Swagger UI, automatic)

  Same REST contract:
    GET  /mcp/tools              — identical JSON response
    POST /mcp/tools/{toolName}   — identical mock data
    GET  /mcp/health             — same structure

=========================================================
  PREREQUISITES
=========================================================

1. gcloud CLI authenticated
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID

2. Billing linked to GCP project

=========================================================
  OPTION A — One-command deploy (recommended)
=========================================================

  cd python-adtech-mcp-server
  chmod +x deploy.sh
  ./deploy.sh

  What it does:
  1. Enables Cloud Run, Cloud Build, Container Registry, Discovery Engine APIs
  2. Submits to Cloud Build: Docker build → GCR push → Cloud Run deploy
  3. Health check + tool count verification
  4. Prints the live URL and export command for the client deploy

=========================================================
  OPTION B — Manual step-by-step
=========================================================

  export PROJECT_ID=$(gcloud config get project)

  # Enable APIs
  gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    discoveryengine.googleapis.com

  # Build + deploy
  gcloud builds submit \
    --config cloudbuild.yaml \
    --timeout=15m \
    .

  # Get the live URL
  export MCP_SERVER_URL=$(gcloud run services describe python-adtech-mcp-server \
    --region us-central1 --format "value(status.url)")
  echo $MCP_SERVER_URL

=========================================================
  TEST THE DEPLOYED SERVICE
=========================================================

  SERVER_URL=$(gcloud run services describe python-adtech-mcp-server \
    --region us-central1 --format "value(status.url)")

  # Health check
  curl $SERVER_URL/mcp/health

  # List all 23 tools
  curl $SERVER_URL/mcp/tools | python3 -m json.tool

  # Execute getCampaignStatus (delivery failure scenario)
  curl -X POST "$SERVER_URL/mcp/tools/getCampaignStatus" \
    -H "Content-Type: application/json" \
    -d '{"campaignId":"CMP-4491"}' | python3 -m json.tool

  # Execute getDealBidStream (seat ID mismatch scenario)
  curl -X POST "$SERVER_URL/mcp/tools/getDealBidStream" \
    -H "Content-Type: application/json" \
    -d '{"dealId":"DEAL-7723","hours":6}' | python3 -m json.tool

  # getSeatMapping — reveals case mismatch
  curl -X POST "$SERVER_URL/mcp/tools/getSeatMapping" \
    -H "Content-Type: application/json" \
    -d '{"dealId":"DEAL-7723"}' | python3 -m json.tool

  # Swagger UI (browser)
  open $SERVER_URL/docs

=========================================================
  MOCK DATA SCENARIOS
=========================================================

  Campaign ID suffix routing (same as Java version):
    ends with 1  → PAUSED + budget $0 + bid below floor + audience 0  (4 issues)
    ends with 2  → ACTIVE + healthy + $312 remaining                   (no issues)
    ends with 3  → ACTIVE + bid $1.80 below floor $2.50               (bid issue only)
    anything else→ PAUSED + budget exhausted (default bad state)

  Examples:
    CMP-4491 → 4 simultaneous issues (classic delivery failure)
    CMP-4492 → healthy campaign
    CMP-4493 → bid below floor only

=========================================================
  KNOWLEDGE BASE (OPTIONAL — Vertex AI Search)
=========================================================

  The searchKnowledgeBase tool uses Vertex AI Search when
  GCP_PROJECT_ID and KB_DATASTORE_ID are set.
  Without them, returns mock KB responses (still functional for testing).

  To set up real KB:
    cp ../adtech-support-poc/setup-kb.sh .
    cp -r ../adtech-support-poc/kb-docs .
    chmod +x setup-kb.sh && ./setup-kb.sh
  Wait ~10 minutes for ingestion.

  Then update the Cloud Run service:
    gcloud run services update python-adtech-mcp-server \
      --region us-central1 \
      --update-env-vars "GCP_PROJECT_ID=$PROJECT_ID,KB_DATASTORE_ID=adtech-kb"

=========================================================
  ENVIRONMENT VARIABLES
=========================================================

  Variable           | Required | Default       | Description
  -------------------|----------|---------------|----------------------------
  GCP_PROJECT_ID     | for KB   | —             | GCP project ID
  KB_DATASTORE_ID    | for KB   | adtech-kb     | Vertex AI Search datastore
  KB_SERVING_CONFIG  | no       | default_search| Serving config name
  PORT               | no       | 8082 local    | Injected by Cloud Run

=========================================================
  LOCAL RUN
=========================================================

  cd python-adtech-mcp-server
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

  cp .env.example .env   # optional — all defaults work

  uvicorn app.main:app --reload --port 8082
  # Health:   http://localhost:8082/mcp/health
  # Tools:    http://localhost:8082/mcp/tools
  # Swagger:  http://localhost:8082/docs

=========================================================
  COST MANAGEMENT
=========================================================

  # Scale to zero (no cost when idle)
  gcloud run services update python-adtech-mcp-server \
    --region us-central1 --min-instances 0

  # Delete service
  gcloud run services delete python-adtech-mcp-server --region us-central1




  Local Run — Both Services

  # Terminal 1 — Python MCP Server
  cd python-adtech-mcp-server
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8082

  # Terminal 2 — Python MCP Client
  cd python-adtech-mcp-client
  cp .env.example .env        # set GROQ_API_KEY=gsk_...
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8080
  # Dashboard: http://localhost:8080

  GCP Deploy Order

  # 1. Deploy server first
  cd python-adtech-mcp-server && ./deploy.sh

  # 2. Deploy client (auto-resolves python-adtech-mcp-server URL)
  cd python-adtech-mcp-client && export GROQ_API_KEY=gsk_... && ./deploy.sh

  To switch back to the Java server at any time: export MCP_SERVER_URL=https://<java-server-url> before deploying the client.

