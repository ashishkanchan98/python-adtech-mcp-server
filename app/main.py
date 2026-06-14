import logging
from pathlib import Path as FilePath

from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.executor.tool_dispatcher import dispatch
from app.registry.tool_registry import ToolDefinition, get_all_tools

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

_STATIC_DIR = FilePath(__file__).parent.parent / "static"

app = FastAPI(
    title="AdTech MCP Server — Python",
    description=(
        "Tool-provider service: exposes 23 AdTech tools as REST endpoints. "
        "No AI logic. No database. Called by python-adtech-mcp-client."
    ),
    version="1.0.0",
)

if _STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")


@app.get("/faq", include_in_schema=False)
def faq():
    """Serve the interactive project FAQ page."""
    faq_file = _STATIC_DIR / "faq.html"
    return FileResponse(str(faq_file), media_type="text/html")


@app.get("/mcp/health")
def health():
    tools = get_all_tools()
    return {"status": "UP", "service": "python-adtech-mcp-server", "toolCount": len(tools)}


@app.get("/mcp/tools")
def list_tools() -> list[dict]:
    """Return all tool definitions — consumed by adtech-mcp-client at startup."""
    return [
        {
            "name":             t.name,
            "description":      t.description,
            "parametersSchema": t.parameters_schema,
        }
        for t in get_all_tools()
    ]


@app.post("/mcp/tools/{tool_name}")
def execute_tool(
    tool_name: str = Path(..., description="Tool name from the registry"),
    args: dict = None,
) -> dict:
    """
    Execute a single tool with the given args.
    Called by adtech-mcp-client once per LLM tool_call (parallel requests possible).
    """
    if args is None:
        args = {}

    logger.info("POST /mcp/tools/%s  args=%s", tool_name, args)

    result = dispatch(tool_name, args)

    if "error" in result and result.get("error", "").startswith("Unknown tool"):
        raise HTTPException(status_code=404, detail=result["error"])

    return result
