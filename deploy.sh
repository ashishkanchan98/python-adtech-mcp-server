#!/bin/bash
# ============================================================
#  python-adtech-mcp-server — GCP Build & Deploy Script
#  Deploy this BEFORE python-adtech-mcp-client.
#
#  Dev deploy (default):
#    ./deploy.sh
#
#  Production deploy:
#    export PROD=true
#    ./deploy.sh
#
#  Optional:
#    export REGION=us-central1
# ============================================================
set -e

REGION="${REGION:-us-central1}"
SERVICE="python-adtech-mcp-server"

# ── Production vs dev settings ───────────────────────────────
if [ "${PROD:-false}" = "true" ]; then
  ENV="prod"
  MIN_INSTANCES="1"
  MAX_INSTANCES="10"
  MEMORY="256Mi"
  CPU="2"
  echo ">>> PRODUCTION mode"
else
  ENV="dev"
  MIN_INSTANCES="0"
  MAX_INSTANCES="3"
  MEMORY="256Mi"
  CPU="1"
fi

# ── Validate GCP project ─────────────────────────────────────
export PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
  echo "ERROR: No active GCP project."
  echo "  Run: gcloud config set project YOUR_PROJECT_ID"
  exit 1
fi

echo ""
echo "============================================"
echo "  python-adtech-mcp-server  →  GCP Deploy"
echo "  Project        : $PROJECT_ID"
echo "  Region         : $REGION"
echo "  Environment    : $ENV"
echo "  Service        : $SERVICE"
echo "  Min Instances  : $MIN_INSTANCES"
echo "  Memory         : $MEMORY  CPU: $CPU"
echo "============================================"
echo ""

# ── Step 1: Enable required APIs ─────────────────────────────
echo "[1/4] Enabling APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  --quiet

# ── Step 2: Build + push + deploy via Cloud Build ────────────
echo "[2/4] Building and deploying via Cloud Build..."
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions "_REGION=$REGION,_MIN_INSTANCES=$MIN_INSTANCES,_MAX_INSTANCES=$MAX_INSTANCES,_MEMORY=$MEMORY,_CPU=$CPU" \
  --timeout=15m \
  .

# ── Step 3: Verify ───────────────────────────────────────────
echo "[3/4] Verifying deployment..."
SERVER_URL=$(gcloud run services describe "$SERVICE" \
  --region "$REGION" \
  --format "value(status.url)" 2>/dev/null || echo "")

if [ -z "$SERVER_URL" ]; then
  echo "ERROR: Service URL not found. Check Cloud Build logs."
  exit 1
fi

# ── Step 4: Health check ─────────────────────────────────────
echo "[4/4] Health check..."
sleep 3
HEALTH=$(curl -sf "$SERVER_URL/mcp/health" 2>/dev/null || echo '{"status":"DOWN"}')
echo "  Health: $HEALTH"

TOOL_COUNT=$(curl -sf "$SERVER_URL/mcp/tools" 2>/dev/null \
  | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
echo "  Tools registered: $TOOL_COUNT"

echo ""
echo "============================================"
echo "  Python MCP Server is LIVE [$ENV]"
echo "  URL: $SERVER_URL"
echo ""
echo "  Save this URL for the client deploy:"
echo "  export MCP_SERVER_URL=$SERVER_URL"
echo ""
echo "  Then deploy client:"
echo "  cd ../python-adtech-mcp-client && ./deploy.sh"
echo "============================================"
echo ""
