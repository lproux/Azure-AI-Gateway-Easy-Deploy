# 🎯 MCP Server Deployment Plan - Complete Strategy

## ✅ Phase 1: COMPLETE - Current Deployment

**Status**: Successfully deployed and tested (3 servers)
**Updated**: 2025-10-28 - Added Weather MCP

| Server | URL | Status | Port | Transport | Tools |
|--------|-----|--------|------|-----------|-------|
| Excel MCP | http://excel-mcp-72998.eastus.azurecontainer.io:8000 | ✅ Healthy | 8000 | JSON-RPC | 5 tools |
| Docs MCP | http://docs-mcp-72998.eastus.azurecontainer.io:8000 | ✅ Healthy | 8000 | JSON-RPC | 4 tools |
| **Weather MCP** | http://weather-mcp-72998.eastus.azurecontainer.io:8080 | ✅ **NEW** | 8080 | SSE | 2 tools |

**Sources**:
- Excel/Docs: Workshop `.archive/workshop-mcp/06-building-http-server/`
- Weather: `mcp-a2a-agents/src/weather/mcp-server/`

---

## 🚀 Phase 2: Additional Servers (Ready to Deploy)

### Found Server Implementations ✅

| Server | Source Path | Status | Used In | Priority |
|--------|------------|--------|---------|---------|
| **weather** | `mcp-a2a-agents/src/weather/mcp-server/` | ✅ **DEPLOYED** | 8 labs | ~~1~~ DONE |
| **oncall** | `mcp-a2a-agents/src/oncall/mcp-server/` | ⏭️ **NEXT** | 5 labs | 2 |
| **spotify** | `mcp-a2a-agents/src/spotify/mcp-server/` | ⏸️ Ready | 2 labs | 3 |

**Next Action**: Deploy OnCall MCP (after testing Weather MCP in notebook)

---

## ⚠️ Phase 3: Servers Needing Creation

| Server | Used in Labs | Status | Action Required |
|--------|--------------|--------|-----------------|
| **github** | 4 labs | ❌ Missing | Create from scratch or find npm package |
| **product-catalog** | 1 lab (master) | ❌ Missing | Create mock server |
| **place-order** | 1 lab (master) | ❌ Missing | Create mock server |
| **ms-learn** | 1 lab (master) | ❌ Missing | Create mock server or use API |

---

## 📋 Deployment Strategy

### Step-by-Step Approach

#### **Step 1: Deploy Weather MCP** ⏭️ NEXT
```bash
# Source: mcp-a2a-agents/src/weather/mcp-server/
az acr build --registry acrmcp72998 \
  --image weather-mcp:latest \
  --file Dockerfile \
  mcp-a2a-agents/src/weather/mcp-server/

az container create \
  --name weather-mcp-72998 \
  --image acrmcp72998.azurecr.io/weather-mcp:latest \
  --dns-name-label weather-mcp-72998 \
  --ports 8000 --os-type Linux \
  --location eastus \
  --resource-group lab-master-lab

# Test
curl http://weather-mcp-72998.eastus.azurecontainer.io:8000/health
```

#### **Step 2: Deploy OnCall MCP**
```bash
# Source: mcp-a2a-agents/src/oncall/mcp-server/
az acr build --registry acrmcp72998 \
  --image oncall-mcp:latest \
  --file Dockerfile \
  mcp-a2a-agents/src/oncall/mcp-server/

az container create \
  --name oncall-mcp-72998 \
  --image acrmcp72998.azurecr.io/oncall-mcp:latest \
  --dns-name-label oncall-mcp-72998 \
  --ports 8000 --os-type Linux \
  --location eastus \
  --resource-group lab-master-lab
```

#### **Step 3: Deploy Spotify MCP** (if implementation exists)
```bash
# Check first: ls mcp-a2a-agents/src/spotify/mcp-server/
```

#### **Step 4: Update Configuration**
After each deployment:
1. Test server health
2. Add URL to `.mcp-servers-config`
3. Update `notebook_mcp_helpers.py`
4. Test in notebook

---

## 🎬 One-Click Deployment Script

### Goal
Create `deploy_all_mcp_servers.sh` that:
1. Deploys all available servers (currently 2, eventually 5-7)
2. Tests each server
3. Updates all config files automatically
4. Generates summary report

### Structure
```bash
#!/bin/bash
# deploy_all_mcp_servers.sh

SERVERS=(
    "excel:workshop/.archive/workshop-mcp/06-building-http-server/excel-analytics-mcp"
    "docs:workshop/.archive/workshop-mcp/06-building-http-server/research-docs-mcp"
    "weather:AI-Gateway/labs/mcp-a2a-agents/src/weather/mcp-server"
    "oncall:AI-Gateway/labs/mcp-a2a-agents/src/oncall/mcp-server"
    "spotify:AI-Gateway/labs/mcp-a2a-agents/src/spotify/mcp-server"
)

for server_def in "${SERVERS[@]}"; do
    name=$(echo $server_def | cut -d: -f1)
    path=$(echo $server_def | cut -d: -f2)
    
    echo "🚀 Deploying $name MCP..."
    
    # Build image
    az acr build --registry acrmcp72998 \
      --image "${name}-mcp:latest" \
      --file Dockerfile "$path"
    
    # Deploy to ACI
    az container create \
      --name "${name}-mcp-72998" \
      --image "acrmcp72998.azurecr.io/${name}-mcp:latest" \
      --dns-name-label "${name}-mcp-72998" \
      --ports 8000 --os-type Linux \
      --location eastus \
      --resource-group lab-master-lab
    
    # Test
    sleep 15
    curl "http://${name}-mcp-72998.eastus.azurecontainer.io:8000/health"
done

# Update configs
python3 update_mcp_configs.py
```

---

## 📊 Testing Strategy

### For Each New Server
1. **Health Check**: `curl http://<server-url>/health`
2. **MCP Tools List**: Test `/mcp/` endpoint with `tools/list` method
3. **Sample Tool Call**: Call one tool to verify functionality
4. **Integration Test**: Use in notebook with `MCPClient()`

### Test Script Template
```python
# test_new_server.py
import httpx

def test_server(name, url):
    # Health check
    response = httpx.get(f"{url}/health")
    assert response.status_code == 200
    
    # Tools list
    response = httpx.post(f"{url}/mcp/", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    })
    assert response.status_code == 200
    tools = response.json()["result"]["tools"]
    print(f"✅ {name}: {len(tools)} tools available")
```

---

## 🔄 Configuration Update Process

After deploying each server:

1. **Update `.mcp-servers-config`**:
```bash
echo "WEATHER_MCP_URL=http://weather-mcp-72998.eastus.azurecontainer.io:8000" >> .mcp-servers-config
```

2. **Update `master-lab.env`**:
```bash
echo "MCP_SERVER_WEATHER_URL=http://weather-mcp-72998.eastus.azurecontainer.io:8000" >> master-lab.env
```

3. **Update `notebook_mcp_helpers.py`**:
Add new server class and initialize in MCPClient.__init__()

4. **Test in Notebook**:
```python
mcp = MCPClient()
result = mcp.weather.get_weather(location="Seattle")
```

---

## 💰 Cost Estimate

| Resource | Qty | Cost/Month | Total |
|----------|-----|------------|-------|
| ACR Basic | 1 | $5 | $5 |
| ACI (1 CPU, 1GB) | 2 deployed | $37 each | $74 |
| ACI (1 CPU, 1GB) | 3 planned | $37 each | $111 |
| **Current Total** | - | - | **$79** |
| **After Phase 2** | - | - | **$190** |

**Cost Optimization**:
- Stop containers when not in use
- Use Container Apps with scale-to-zero
- Delete after lab completion

---

## 📝 Next Immediate Steps

1. ✅ **Test current 2 servers** - COMPLETE
2. 🔄 **Deploy weather MCP** - READY TO START
3. ⏭️ **Deploy oncall MCP** - After weather
4. ⏭️ **Check spotify implementation** - Verify files exist
5. ⏭️ **Create one-click script** - After 3-5 servers working
6. ⏭️ **Handle missing servers** - github, product-catalog, etc.

---

## 🎯 Success Criteria

- ✅ All deployed servers return HTTP 200 on /health
- ✅ All servers accessible from notebook
- ✅ Each server's tools callable via MCPClient
- ✅ Configuration files auto-updated
- ✅ One-click deployment script works end-to-end
- ✅ Full documentation with troubleshooting

