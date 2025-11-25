# MCP Custom HTTP Wrapper Build Log
**Date**: 2025-11-15
**Objective**: Build custom Docker images that wrap stdio MCP servers with HTTP/SSE transport

---

## Background

The Docker Hub images (mcp/github, mcp/playwright) use stdio transport only, which is incompatible with Azure Container Instances that require HTTP endpoints.

**Solution**: Create custom Docker images that:
1. Run the stdio MCP server as a subprocess
2. Wrap it with a Python FastAPI HTTP/SSE bridge
3. Expose HTTP endpoints for Container Instance deployment

---

## Build Progress

### 1. MCP HTTP Bridge Script ✅

Created `mcp_http_bridge.py` - A generic Python FastAPI server that:
- Starts MCP server as subprocess (configurable via env vars)
- Exposes `/health` endpoint
- Exposes `/messages` endpoint for JSON-RPC
- Exposes `/sse` endpoint for Server-Sent Events
- Forwards stdin/stdout between HTTP and MCP server subprocess

**Key Features**:
- Async subprocess communication
- Request/response queuing
- Session management with Mcp-Session-Id header
- Configurable via environment variables:
  - `MCP_COMMAND`: Command to run (e.g., "npx")
  - `MCP_ARGS`: Arguments (e.g., "-y @playwright/mcp")
  - `PORT`: HTTP port (default 8080)

---

### 2. GitHub MCP HTTP Wrapper ✅

**Dockerfile**: `mcp-http-wrappers/github-mcp/Dockerfile`

**Base Image**: `node:20-slim`
**Packages Installed**:
- @modelcontextprotocol/server-github (official GitHub MCP server)
- Python 3 + pip + venv
- FastAPI + Uvicorn + Starlette

**Build Status**: ✅ COMPLETED
- ACR Image: `acrpavavy6pu5hpa.azurecr.io/github-mcp-http:v1`
- Build Time: ~2 minutes
- Image Size: ~1.2 GB (with all dependencies)

---

### 3. Playwright MCP HTTP Wrapper 🔄

**Dockerfile**: `mcp-http-wrappers/playwright-mcp/Dockerfile`

**Base Image**: `mcr.microsoft.com/playwright:v1.40.0-jammy`
**Packages Installed**:
- @playwright/mcp (official Microsoft Playwright MCP server)
- Python 3 + pip + venv
- FastAPI + Uvicorn + Starlette

**Build Status**: 🔄 IN PROGRESS
- ACR Image: `acrpavavy6pu5hpa.azurecr.io/playwright-mcp-http:v1`
- Status: Installing dependencies (Step 2/12)
- Expected completion: 3-4 minutes

**Note**: Initial build failed due to incorrect npm package name. Fixed to use `@playwright/mcp` instead of `@modelcontextprotocol/server-playwright`.

---

## Next Steps

1. ✅ Complete Playwright MCP build
2. ⏳ Deploy GitHub MCP to Container Instance
3. ⏳ Deploy Playwright MCP to Container Instance
4. ⏳ Test HTTP endpoints (health, messages, sse)
5. ⏳ Update configuration files (master-lab.env, .mcp-servers-config)
6. ⏳ Update notebook cells to use new MCP servers
7. ⏳ Test MCP initialization in notebook

---

## Technical Notes

### Why stdio → HTTP wrapping needed?

**Problem**: Azure Container Instances expect HTTP-listening services, not stdio-based processes.

**MCP Transport Types**:
- **stdio**: Communication via standard input/output (used by Claude Desktop)
- **HTTP/SSE**: Communication via HTTP Server-Sent Events (used by web clients, remote access)

Docker Hub MCP images (mcp/github, mcp/playwright) only support stdio, making them incompatible with ACI.

**Solution Architecture**:
```
HTTP Request → FastAPI Bridge → stdin → MCP Server
HTTP Response ← FastAPI Bridge ← stdout ← MCP Server
```

### Environment Variables

Each container needs:
```bash
MCP_COMMAND="npx"
MCP_ARGS="-y @playwright/mcp"  # or @modelcontextprotocol/server-github
PORT="8080"
GITHUB_PERSONAL_ACCESS_TOKEN="<token>"  # For GitHub MCP only
```

---

## Deployment Configuration

### GitHub MCP Container
```bash
az container create \
  --resource-group lab-master-lab \
  --name github-mcp-master \
  --image acrpavavy6pu5hpa.azurecr.io/github-mcp-http:v1 \
  --dns-name-label github-mcp-master \
  --ports 8080 \
  --cpu 1 --memory 2 \
  --os-type Linux \
  --location eastus \
  --registry-login-server acrpavavy6pu5hpa.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --environment-variables \
    MCP_COMMAND=npx \
    MCP_ARGS="-y @modelcontextprotocol/server-github" \
    PORT=8080
```

### Playwright MCP Container
```bash
az container create \
  --resource-group lab-master-lab \
  --name playwright-mcp-master \
  --image acrpavavy6pu5hpa.azurecr.io/playwright-mcp-http:v1 \
  --dns-name-label playwright-mcp-master \
  --ports 8080 \
  --cpu 2 --memory 4 \
  --os-type Linux \
  --location eastus \
  --registry-login-server acrpavavy6pu5hpa.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --environment-variables \
    MCP_COMMAND=npx \
    MCP_ARGS="-y @playwright/mcp" \
    PORT=8080
```

---

## Expected Endpoints

All MCP servers will expose:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check (returns JSON status) |
| `/messages` | POST | JSON-RPC message handling |
| `/sse` | GET | Server-Sent Events stream |

**Health Check Response**:
```json
{
  "status": "healthy",
  "service": "mcp-http-bridge",
  "mcp_running": true
}
```

---

## Files Created

1. `mcp-http-wrappers/mcp_http_bridge.py` - Generic HTTP/SSE bridge (137 lines)
2. `mcp-http-wrappers/github-mcp/Dockerfile` - GitHub MCP wrapper
3. `mcp-http-wrappers/github-mcp/mcp_http_bridge.py` - Copy of bridge script
4. `mcp-http-wrappers/playwright-mcp/Dockerfile` - Playwright MCP wrapper
5. `mcp-http-wrappers/playwright-mcp/mcp_http_bridge.py` - Copy of bridge script
6. `project-execution-logs/MCP-CUSTOM-BUILD-LOG.md` - This file

---

## Troubleshooting

### If build fails:
1. Check ACR access: `az acr show --name acrpavavy6pu5hpa`
2. Check build logs: `az acr build --logs` output
3. Verify package names exist in npm registry

### If deployment fails:
1. Check ACR credentials are valid
2. Verify resource group exists
3. Check region availability (eastus recommended)

### If MCP connection fails:
1. Check container logs: `az container logs --name <container-name> --resource-group lab-master-lab`
2. Test health endpoint: `curl http://<fqdn>:8080/health`
3. Verify environment variables in container

---

**Status**: GitHub MCP ✅ Complete | Playwright MCP 🔄 Building
**Last Updated**: 2025-11-15 23:54 UTC
