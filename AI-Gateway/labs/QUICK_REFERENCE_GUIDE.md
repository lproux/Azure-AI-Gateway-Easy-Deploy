# Master AI Gateway Workshop - Quick Reference Guide

Fast lookup for sections, labs, and key concepts.

---

## Navigation Index

### By Section

| Section | Cells | Focus | Time |
|---------|-------|-------|------|
| [Section 0](#section-0) | 1-20 | Deployment & Setup | 40 min |
| [Section 1](#section-1) | 21-70 | Core Features | Variable |
| [Section 2](#section-2) | 71-100 | Advanced Features | Variable |
| [MCP Fundamentals](#mcp) | 101-115 | Data Integration | Variable |
| [Section 3](#section-3) | 116-135 | AI Foundry & SK | Variable |

---

## Section 0: Initialize and Deploy

### Quick Checklist

```
[  ] 0.1 Environment Detection     - Detect Azure subscription
[  ] 0.2 Bootstrap Configuration   - Initialize basic config
[  ] 0.3 Dependencies Installation - Install Python packages
[  ] 0.4 Azure Authentication      - Login to Azure
[  ] 0.5 Core Helper Functions     - Load utility functions
[  ] 0.6 Deployment Configuration  - Prepare parameters
[  ] 0.7 Deploy Infrastructure     - Run 4-step deployment
[  ] 0.8 Reload Configuration      - Load deployed resources
```

### Key Variables Generated

```python
# After Section 0, available:
apim_gateway_url        # APIM endpoint URL
apim_api_key           # APIM subscription key
resource_group         # Azure resource group
subscription_id        # Azure subscription
ai_foundry_project     # AI Foundry project name
```

### Deployment Steps (0.7)

1. **Core Infrastructure** (10 min)
   - APIM Service
   - Log Analytics
   - Application Insights

2. **AI Foundry** (15 min)
   - 3 Hubs
   - 14 Models
   - Deployments

3. **Supporting Services** (10 min)
   - Redis Cache
   - AI Search
   - Cosmos DB
   - Content Safety

4. **MCP Servers** (5 min)
   - Container Apps
   - 7 Servers
   - Networking

### Troubleshooting Section 0

| Issue | Solution |
|-------|----------|
| Authentication fails | Run `az login` first |
| Quota exceeded | Check Azure subscription limits |
| Deployment timeout | Increase timeout or retry |
| Network errors | Check firewall and VPN |

---

## Section 1: Core AI Gateway Features (6 Labs)

### Lab 1.1: Zero to Production

**What**: Basic chat completion through APIM
**Time**: 5-10 minutes
**Tests**: 3 (Basic, Streaming, Multiple)
**Success**: Response < 2 seconds

```python
# Key code pattern:
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)
```

---

### Lab 1.2: Backend Pool Load Balancing

**What**: Multi-region routing with failover
**Time**: 10-15 minutes
**Tests**: 2 (Distribution, Response Times)
**Backend Config**:
- Priority 1: Primary PTU
- Priority 2: Fallback (multiple)

```xml
<!-- APIM Backend Pool Configuration -->
<backend-pool>
  <backend name="priority1" priority="1">
    <address>https://openai-east.openai.azure.com</address>
  </backend>
  <backend name="priority2a" priority="2">
    <address>https://openai-central.openai.azure.com</address>
  </backend>
  <backend name="priority2b" priority="2">
    <address>https://openai-west.openai.azure.com</address>
  </backend>
</backend-pool>
```

---

### Lab 1.3: Token Metrics Emitting

**What**: Track token consumption for cost monitoring
**Time**: 5-10 minutes
**Metrics**: Prompt, Completion, Total tokens
**Storage**: Application Insights

```python
# Metrics appear in App Insights within 2-5 minutes
# Query pattern:
customMetrics
| where name == "LLM-Tokens"
| summarize sum(value) by tostring(customDimensions.model)
```

---

### Lab 1.4: Access Controlling

**What**: OAuth 2.0 authentication via Azure AD
**Time**: 10-15 minutes
**Pattern**: Token acquisition → Bearer header → APIM validation

```bash
# Get token
TOKEN=$(az account get-access-token --query accessToken -o tsv)

# Use in request
curl -H "Authorization: Bearer $TOKEN" \
  https://{apim}.azure-api.net/openai/chat/completions
```

---

### Lab 1.5: Content Safety

**What**: Screen prompts before sending to Azure OpenAI
**Time**: 5-10 minutes
**Threshold**: Configurable severity (0-7)
**Categories**: Hate, SelfHarm, Sexual, Violence

```python
# Response includes verdict in headers
content_safety_verdict = response.headers.get('x-content-safety-verdict')
# Result: "Safe", "LowSeverity", "ModerateSeverity", "HighSeverity"
```

---

### Lab 1.6: Model Routing

**What**: Route requests to different models/backends
**Time**: 10-15 minutes
**Routing Logic**: Based on model parameter

```python
# Request with model parameter
response = client.chat.completions.create(
    model="gpt-4o",  # Routes to East deployment
    messages=[...]
)
# OR
response = client.chat.completions.create(
    model="gpt-4-turbo",  # Routes to Central deployment
    messages=[...]
)
```

---

## Section 2: Advanced Features (4 Labs)

### Lab 2.1: Semantic Caching

**What**: Cache similar queries using vector embeddings
**Time**: 10-20 minutes
**Cache**: Redis
**Benefit**: Up to 90% cost reduction

```python
# Configuration:
similarity_threshold = 0.8      # 80% match required
cache_ttl = 1200               # 20 minutes
embedding_model = "text-embedding-3-small"

# Effect: Similar queries return cached responses in <100ms
```

---

### Lab 2.2: Message Storing with Cosmos DB

**What**: Persistent audit trail of all LLM interactions
**Time**: 15-30 minutes
**Pipeline**: APIM → Azure Monitor → Event Hub → Stream Analytics → Cosmos DB

```kusto
// Query stored interactions:
SELECT c.user_id, c.prompt, c.completion, c.token_count, c.timestamp
FROM messages c
WHERE c.timestamp > GetCurrentTimestamp() - 3600
ORDER BY c.timestamp DESC
```

**Timeline**:
- Logs appear in Event Hub: <1 second
- Stream Analytics processes: <5 seconds
- Data in Cosmos DB: 1-2 minutes

---

### Lab 2.3: Vector Searching with RAG

**What**: Augment responses with retrieved documents
**Time**: 20-30 minutes
**Flow**: Documents → Chunks → Embeddings → AI Search → LLM augmentation

```python
# Embedding latency: <1 second
# Search latency: <500ms
# Response generation: 2-5 seconds

# Process:
1. Index documents with embeddings
2. User query → embedding
3. Vector search finds top-k results
4. Results added to LLM prompt
5. Enhanced response returned
```

---

### Lab 2.4: Built-in LLM Logging

**What**: Comprehensive observability for all LLM interactions
**Time**: 5-10 minutes
**Data**: Prompts, completions, tokens, metadata

```kusto
// Sample KQL query:
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.APIMANAGEMENT"
| where Category == "GatewayLogs"
| where backendRequestUri contains "openai"
| summarize
    Count = count(),
    AvgLatency = avg(latency),
    MaxLatency = max(latency)
    by tostring(responseCode)
```

---

## MCP Fundamentals

### MCP Data Sources

```python
# Access via global 'mcp' object:
mcp.excel     # Excel Analytics (direct)
mcp.docs      # Research Documents (direct)
mcp.github    # GitHub API (via APIM)
mcp.weather   # Weather API (via APIM)
```

### MCP Exercises Quick Links

| Exercise | Purpose | Data Source |
|----------|---------|-------------|
| 2.2 | Sales Analysis | Excel MCP |
| 2.3 | Cost Analysis | Excel MCP |
| 2.4 | Function Calling | MCP Tools |
| 2.5 | Column Analysis | Excel MCP |

### Lab 3.2: GitHub Repository Access

**What**: Access GitHub repo contents via MCP
**Time**: 10-15 minutes
**Capabilities**: Browse, read files, check history

```python
# Example:
repository_structure = mcp.github.list_files(repo_name)
file_content = mcp.github.read_file(repo_name, file_path)
commits = mcp.github.get_commits(repo_name)
```

### Lab 3.3: GitHub + AI Code Analysis

**What**: Analyze code with Azure OpenAI + GitHub MCP
**Time**: 20-30 minutes
**Output**: Quality report, issues, recommendations

```
Flow: GitHub → Extract → Chunk → Azure OpenAI → Analysis Report
```

---

## Section 3: AI Foundry & Integrations

### Lab 3.1: AI Foundry SDK

**What**: Use AI Foundry SDK with APIM routing
**Time**: 10-15 minutes
**Configuration**:

```python
from azure.ai.projects import AIProjectClient

client = AIProjectClient.from_config()
# Automatically routes through APIM if connection configured
response = client.agents.create(...)
```

**Connection Setup**:
```
Provider: Azure OpenAI
Endpoint: https://{apim_gateway}.azure-api.net
Key: {apim_subscription_key}
API Version: 2024-08-01-preview
```

---

### Semantic Kernel & AutoGen (Phase 3)

**What**: Advanced orchestration patterns
**Time**: Varies by phase (10-60 minutes)

| Phase | Focus | Complexity |
|-------|-------|-----------|
| Cell 1 | SK Plugins + Function Calling | Medium |
| Cell 2 | SK Streaming Chat | Medium |
| Cell 3 | AutoGen Multi-Agent | High |
| Cell 4 | SK Agent Custom Client | Medium |
| Cell 5 | Hybrid Orchestration | High |
| Cell 6 | Advanced Patterns | Expert |

---

## Common Commands

### Azure CLI

```bash
# Authentication
az login
az account set --subscription "SUBSCRIPTION_ID"

# Check APIM
az apim api list --service-name $APIM_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP --output table

# Check health
az apim backend list --service-name $APIM_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP

# View logs
az monitor log-analytics query --workspace $LOG_ANALYTICS_ID \
  -q "AzureDiagnostics | limit 10"
```

### Python

```python
# Load configuration
import os
from dotenv import load_dotenv
load_dotenv("master-lab.env")

# Access variables
apim_gateway_url = os.getenv("APIM_GATEWAY_URL")
apim_api_key = os.getenv("APIM_API_KEY")

# Initialize clients
from azure.openai import AzureOpenAI
client = AzureOpenAI(
    api_key=apim_api_key,
    api_version="2024-08-01-preview",
    azure_endpoint=apim_gateway_url
)
```

---

## Troubleshooting Quick Guide

### Authentication Issues

```
Problem: 401 Unauthorized
Solution: Wait 30-60 seconds for policy to propagate
Check: az account show
```

### Deployment Issues

```
Problem: Quota exceeded
Solution: Check subscription limits in Azure Portal
Command: az vm list --output table
```

### Performance Issues

```
Problem: Slow responses
Solution: Check backend load with Test 1 of Lab 1.2
Command: Check Application Insights for latency metrics
```

### APIM Issues

```
Problem: API returns 500 error
Solution: Check backend health and APIM tracing
Command: az apim backend list
```

### Logging Issues

```
Problem: Logs not appearing
Solution: Check diagnostic settings are enabled
Wait: 2-5 minutes for logs to appear in Analytics
```

---

## Performance Targets

### Response Times

| Operation | Target | Threshold |
|-----------|--------|-----------|
| Chat completion | <2s | <5s |
| Token metrics | <100ms | <500ms |
| Vector search | <500ms | <1s |
| Cache hit | <100ms | <200ms |
| Embedding | <1s | <2s |

### Scalability Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Requests/sec | 1000+ | With load balancing |
| Concurrent users | 10,000+ | With proper scaling |
| Message size | 4MB | APIM limit |
| Token limit | 128K | Model dependent |

### Cost Metrics

| Metric | Baseline | With Optimization |
|--------|----------|-------------------|
| API calls | 100% | 10-50% (caching) |
| Storage | Full | Reduced with TTL |
| Compute | Standard | Optimized |

---

## Document References

### In Notebook

- Each lab has: Objective, What You'll Learn, How It Works, Prerequisites, Expected Results
- Troubleshooting section in relevant labs
- Sample KQL/SQL queries provided
- Configuration examples included

### External Resources

- Azure OpenAI Docs: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- APIM Docs: https://learn.microsoft.com/en-us/azure/api-management/
- Semantic Kernel: https://github.com/microsoft/semantic-kernel
- MCP Protocol: https://modelcontextprotocol.io/

---

## Key Environment Variables

```bash
# Generated after Section 0:
APIM_GATEWAY_URL=https://{name}.azure-api.net
APIM_API_KEY={subscription-key}
APIM_SERVICE_NAME={service-name}
RESOURCE_GROUP={resource-group-name}
SUBSCRIPTION_ID={subscription-id}
AI_FOUNDRY_PROJECT={project-name}
AI_FOUNDRY_HUB={hub-id}
LOG_ANALYTICS_ID={workspace-id}
APP_INSIGHTS_KEY={instrumentation-key}
COSMOS_DB_ENDPOINT={cosmos-endpoint}
REDIS_ENDPOINT={redis-endpoint}
AI_SEARCH_ENDPOINT={search-endpoint}
```

---

## Success Checklist

### After Section 0
- [ ] Azure resources deployed
- [ ] Configuration file created (master-lab.env)
- [ ] All environment variables set
- [ ] APIM reachable
- [ ] Models deployed

### After Section 1 (Core Labs)
- [ ] Lab 1.1: Chat completion working
- [ ] Lab 1.2: Load balancing verified
- [ ] Lab 1.3: Token metrics visible in App Insights
- [ ] Lab 1.4: OAuth tokens acquired
- [ ] Lab 1.5: Content safety filtering active
- [ ] Lab 1.6: Model routing functional

### After Section 2 (Advanced Labs)
- [ ] Lab 2.1: Cache hit ratio >50%
- [ ] Lab 2.2: Messages in Cosmos DB
- [ ] Lab 2.3: RAG responses improved
- [ ] Lab 2.4: Logs queryable in Analytics

### After MCP & Section 3
- [ ] MCP data sources accessible
- [ ] GitHub integration working
- [ ] Code analysis producing results
- [ ] AI Foundry SDK routing through APIM
- [ ] SK and AutoGen agents functional

---

## Links & Anchors

Quick jump to sections:

- [Section 0](#section-0-initialize-and-deploy) - Deployment
- [Lab 1.1](#lab-11-zero-to-production) - Basic setup
- [Lab 1.6](#lab-16-model-routing) - Advanced routing
- [Lab 2.3](#lab-23-vector-searching-with-rag) - RAG patterns
- [Lab 3.1](#lab-31-ai-foundry-sdk) - AI Foundry
- [MCP Fundamentals](#mcp-fundamentals) - Data integration
- [SK & AutoGen](#semantic-kernel--autogen-phase-3) - Orchestration

---

## Document Information

- **Version**: 1.0
- **Last Updated**: November 23, 2025
- **Coverage**: All 135 notebook cells
- **Format**: Quick reference with links to full docs
- **Audience**: Developers, DevOps, Data Scientists

---

**For detailed information, see:**
- `COMPREHENSIVE_TABLE_OF_CONTENTS.md` - Full hierarchy
- `NOTEBOOK_STRUCTURE_SUMMARY.md` - Architecture overview
- Notebook cells for complete explanations and code examples

