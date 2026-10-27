
# ⚡ ShadowMCP Gateway

> Enterprise-grade Security Gateway and Policy Enforcement Firewall for Model Context Protocol (MCP) and Agentic AI workflows.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 🛡️ Overview
ShadowMCP acts as a lightweight, zero-latency security proxy sitting directly between LLM clients (such as Claude Desktop, Cursor AI, or custom agents) and upstream FastMCP tool servers. It intercepts JSON-RPC 2.0 tool calls, inspects payloads against malicious signature vectors, enforces enterprise security policies, and streams live telemetry to a real-time operations dashboard.

### Key Features
1. Real-Time Threat Detection: Regex-based deep inspection catching Path Traversal (`../../`), Prompt Injection (`ignore previous instructions`), and SQL Injection vectors.
2. Sub-Millisecond Overhead: Built on asynchronous FastAPI middleware ensuring $<1\text{ms}$ latency impact on tool execution.
Operations & Telemetry Dashboard: A modern, dark-mode Tailwind CSS interface tracking inspected call volume, block rates, and live request streams.
3. Upstream Reverse-Proxy Mode: Safely forwards sanitized requests to downstream FastMCP servers via `httpx`.

---

## 🏗️ Architecture Flow
      text
[LLM Client: Claude / Cursor] 
       │ (JSON-RPC 2.0)
       ▼
[ShadowMCP Gateway :8000] ──(Inspects & Blocks Malicious Payloads)
       │ (Sanitized & Safe)
       ▼
[Upstream FastMCP Tool Server]