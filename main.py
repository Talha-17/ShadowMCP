import re
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ShadowMCP Gateway", version="2.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

THREAT_PATTERNS = [
    re.compile(r"(\.\./){2,}", re.IGNORECASE),  # Path Traversal
    re.compile(
        r"ignore previous instructions|system prompt|reveal secret",
        re.IGNORECASE,
    ),  # Prompt Injection
    re.compile(
        r"(\b(SELECT|DROP|INSERT|DELETE|UPDATE)\b.*;)", re.IGNORECASE
    ),  # SQL Injection
]


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict | None = None
    id: int | str


# Serve the web UI at the root route
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/v1/mcp/inspect")
async def inspect_mcp_payload(req: MCPRequest):
    start_time = time.time()
    payload_str = str(req.model_dump())

    threat_detected = False
    matched_rule = None

    for pattern in THREAT_PATTERNS:
        if pattern.search(payload_str):
            threat_detected = True
            matched_rule = pattern.pattern
            break

    latency = round((time.time() - start_time) * 1000, 2)

    if threat_detected:
        return {
            "status": "BLOCKED",
            "risk_score": 98,
            "latency_ms": latency,
            "reason": f"Matched malicious signature: {matched_rule}",
            "action": "Dropped by ShadowMCP Policy Firewall",
        }

    return {
        "status": "ALLOWED",
        "risk_score": 2,
        "latency_ms": latency,
        "action": "Forwarded to downstream FastMCP server",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ShadowMCP Gateway"}