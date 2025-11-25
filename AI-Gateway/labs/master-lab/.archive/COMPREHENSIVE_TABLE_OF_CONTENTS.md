# Master AI Gateway Workshop - Comprehensive Table of Contents

**One-Click Deployment for Azure AI Gateway with MCP Integration**

---

## Quick Navigation

- [Section 0: Initialize and Deploy](#section-0-initialize-and-deploy)
- [Section 1: Core AI Gateway Features](#section-1-core-ai-gateway-features)
- [Section 2: Advanced Features](#section-2-advanced-features)
- [Section: MCP Fundamentals](#section-mcp-fundamentals)
- [Section 3: AI Foundry & Integrations](#section-3-ai-foundry--integrations)

---

# Section 0: Initialize and Deploy

**Important**: These cells run WITHOUT master-lab.env (it doesn't exist yet!)

## 0.1 Environment Detection

Detects Azure environment and subscription configuration.

## 0.2 Bootstrap Configuration

Minimal configuration setup for initial deployment.

## 0.3 Dependencies Installation

Installs all required Python packages and Azure CLI tools.

## 0.4 Azure Authentication & Service Principal

Authenticates with Azure and creates service principal credentials.

## 0.5 Core Helper Functions

Provides utility functions for deployment and configuration management.

## 0.6 Deployment Configuration

Prepares configuration parameters for infrastructure deployment.

## 0.7 Deploy Infrastructure

### Main Deployment - All 4 Steps

Deploys all infrastructure in sequence:

1. **Core Infrastructure** (~10 min)
   - Azure API Management (APIM)
   - Log Analytics Workspace
   - Application Insights

2. **AI Foundry** (~15 min)
   - 3 AI Foundry Hubs
   - 14 Models (GPT-4o, GPT-4 Turbo, GPT-3.5, etc.)
   - Model Deployments

3. **Supporting Services** (~10 min)
   - Redis Cache
   - Azure AI Search
   - Azure Cosmos DB
   - Azure AI Content Safety

4. **MCP Servers** (~5 min)
   - Container Apps Environment
   - 7 MCP Servers
   - Network configuration

**Total estimated time: ~40 minutes**

## 0.8 Reload Complete Configuration

Reloads and validates all deployed resources and configuration.

---

# Section 1: Core AI Gateway Features

Foundation labs covering essential Azure API Management capabilities for AI workloads.

## Lab 1.1: Zero to Production

Learn the fundamentals of deploying and testing Azure OpenAI through API Management.

### Objective

Establish the foundation for all advanced labs by deploying basic chat completion.

### What You'll Learn

- Basic Chat Completion: Send prompts to GPT-4o-mini and receive responses
- Streaming Responses: Handle real-time streaming output
- Request Patterns: Understand HTTP request/response cycles through APIM
- API Key Management: Secure API access using APIM subscription keys

### Tests

#### Test 1: Basic Chat Completion

Tests simple chat completion requests through the APIM gateway.

#### Test 2: Streaming Response

Validates streaming response handling with incremental token delivery.

#### Test 3: Multiple Requests

Confirms multiple sequential requests complete successfully.

### Expected Outcome

- Basic chat completion returns valid responses
- Streaming works correctly with incremental tokens
- Multiple requests complete successfully
- Response times remain under 2 seconds for simple prompts

---

## Lab 1.2: Backend Pool Load Balancing

Implement multi-region Azure OpenAI deployment patterns with intelligent routing.

### Objective

Understand prioritized backend pool configuration for PTU (Provisioned Throughput Units) with fallback consumption scenarios.

### What You'll Learn

- Backend Pool Configuration: Define priority-based routing rules in APIM
- Load Distribution: Understand request routing across multiple endpoints
- Failover Behavior: See graceful degradation when backends reach capacity
- Priority-Based Routing: Configure primary (Priority 1) and fallback (Priority 2) endpoints
- Monitoring: Track request distribution and backend health

### How It Works

1. Client requests arrive at APIM gateway
2. APIM evaluates backend pool configuration
3. Priority 1 backend receives requests first
4. When Priority 1 is exhausted, automatic failover to Priority 2 backends
5. Multiple Priority 2 backends load-balanced equally
6. Metrics show distribution of requests

### Tests

#### Test 1: Load Distribution

Observes how requests distribute across backend pools.

#### Test 2: Visualize Response Times

Tracks response time consistency during failover scenarios.

### Expected Results

- Load distribution patterns visible in metrics
- Priority 1 backend exhaustion triggers failover
- Automatic failover to Priority 2 backends confirmed
- Equal load distribution among Priority 2 endpoints
- Response times remain consistent despite failover

---

## Lab 1.3: Token Metrics Emitting

Implement comprehensive observability for your AI gateway by emitting token consumption metrics.

### Objective

Track LLM token usage (prompt, completion, and total tokens) to monitor costs and capacity planning.

### What You'll Learn

- Token Metrics Policy: Configure APIM to emit token metrics
- Cost Monitoring: Track prompt tokens, completion tokens, and total tokens
- Application Insights Integration: Send metrics for centralized monitoring
- Response Streaming: Support streaming while tracking tokens
- Troubleshooting: Use tracing tools to verify metric emission

### How It Works

1. Request arrives at APIM with Azure OpenAI headers
2. Policy extracts token counts from responses
3. Categorizes tokens: Prompt, Completion, Total
4. Emits custom metrics to Application Insights
5. Metrics queryable and visualizable in dashboards
6. Streaming responses aggregate token counts

### Key Configuration

- Policy name: `azure-openai-emit-token-metric`
- Supported endpoints: Azure OpenAI Chat Completion, Completion APIs
- Metrics update in real-time as requests complete

### Expected Results

- Metrics appear in Application Insights within 2-5 minutes
- Custom metric "LLM-Tokens" shows token breakdown
- Create alerts based on token thresholds
- Streaming responses properly track all tokens
- KQL queries analyze token patterns

---

## Lab 1.4: Access Controlling

Implement OAuth 2.0 based access control to restrict API access by user or client.

### Objective

Configure identity provider-based authentication for fine-grained authorization on Azure OpenAI models through APIM.

### What You'll Learn

- OAuth 2.0 Authorization: Configure identity provider-based authentication
- Token Acquisition: Request tokens from Azure AD for authenticated API calls
- Bearer Tokens: Include tokens in API requests for authorization
- Access Scopes: Define granular permissions for different API endpoints
- Token Expiration: Handle token refresh and expiration scenarios
- Troubleshooting: Debug 401/403 errors and policy propagation delays

### How It Works

1. Client application requests OAuth token from Azure AD
2. Azure AD validates credentials and returns access token
3. Client includes token in Authorization header (Bearer token)
4. APIM policy validates token with Azure AD
5. Policy checks token scope against API requirements
6. Authorized requests proceed to backend Azure OpenAI
7. Unauthorized requests return 403 Forbidden

### Prerequisites

- Python 3.12 or later
- VS Code with Jupyter notebook extension
- Azure Subscription with Contributor + RBAC Administrator roles
- Azure CLI installed and authenticated
- Azure AD application registration (created during deployment)

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Wait 30-60 seconds for policy to propagate |
| 500 Internal Server Error | Check backend health with Azure CLI |
| Token not found | Run `az login` to authenticate |
| Missing API Key | Verify APIM_API_KEY in environment variables |

### Expected Results

- Successful authentication with valid OAuth token
- Requests with invalid/missing tokens receive 401 Unauthorized
- Token-based access control enforced at APIM level
- Can observe policy evaluation in APIM tracing
- Different users can have different access levels
- Token expiration properly handled with refresh

---

## Lab 1.5: Content Safety

Protect your AI gateway from harmful content by implementing Azure AI Content Safety policy.

### Objective

Screen user prompts before sending them to Azure OpenAI using content filtering.

### What You'll Learn

- Content Safety Policy: Configure LLM content filtering in APIM
- Pre-Request Scanning: Analyze prompts before they reach the backend
- Severity Levels: Understand how Content Safety categorizes harmful content
- Policy Actions: Block malicious prompts or log suspicious content
- Configuration: Fine-tune sensitivity thresholds for your use case
- Compliance: Meet organizational policies around harmful content

### How It Works

1. User prompt arrives at APIM gateway
2. Policy intercepts request before sending to Azure OpenAI
3. Prompt is sent to Azure AI Content Safety service
4. Content Safety service analyzes for harmful content
5. Severity score returned (0-7 scale)
6. Policy decision:
   - If severity < threshold: request proceeds to Azure OpenAI
   - If severity >= threshold: request blocked with 403 error
7. Response returned to client with content safety result

### Configuration Options

- Severity threshold: Configurable (typically 0-7 scale)
- Categories: Hate, SelfHarm, Sexual, Violence
- Action: Block with 403 or Log and Proceed
- Cache policy results for repeated content

### Expected Results

- Normal prompts pass through Content Safety checks
- Prompts with harmful content blocked with 403 error
- Content Safety verdict visible in response headers
- Detailed analysis of why content was blocked
- Different severity thresholds can be configured
- Logs show all content safety evaluations

---

## Lab 1.6: Model Routing

Implement intelligent model routing in APIM to direct requests to appropriate Azure OpenAI backends.

### Objective

Enable multi-model deployments with automatic request routing based on the requested model name.

### What You'll Learn

- Model-Based Routing: Configure conditional routing based on model parameter
- Multiple Backends: Manage requests to different Azure OpenAI deployments
- Request Rewriting: Modify requests to match backend deployment names
- Model Aliases: Map user-friendly model names to actual deployment names
- Fallback Logic: Handle requests for unavailable models gracefully
- Policy Composition: Combine routing with other policies

### How It Works

1. Client requests Azure OpenAI API with specific model parameter
2. APIM policy extracts the model name from request
3. Policy evaluates routing rules based on model
4. Conditional logic routes to appropriate backend:
   - GPT-4o → Azure OpenAI East deployment
   - GPT-4 Turbo → Azure OpenAI Central deployment
   - GPT-3.5 Turbo → Azure OpenAI West deployment
5. Request forwarded to selected backend with deployment name rewrite
6. Response returned to client transparently

### Common Use Cases

1. **Multi-Region Deployment**: Route by model to distribute load geographically
2. **Model Separation**: Keep different models in different deployments
3. **Cost Optimization**: Route to cost-effective models for suitable workloads
4. **Gradual Migration**: Route some requests to new model versions
5. **A/B Testing**: Route percentage of traffic to different model versions

### Expected Results

- Requests for GPT-4o routed to correct backend
- Requests for GPT-4 Turbo reach appropriate deployment
- Requests for GPT-3.5 Turbo complete successfully
- Model names properly translated for each backend
- Invalid model requests fail gracefully
- Can trace routing decisions in APIM logs

---

# Section 2: Advanced Features

Advanced labs covering sophisticated AI gateway patterns and integrations.

## Lab 2.1: Semantic Caching

Reduce API calls for similar queries using semantic similarity matching.

### Objective

Implement semantic caching to reduce Azure OpenAI API calls by matching semantically similar queries.

### What You'll Learn

- How semantic caching reduces API calls for similar queries
- How to measure caching performance
- How vector embeddings enable semantic similarity matching

### Key Benefits

- **Cost savings**: Reduced Azure OpenAI API calls (up to 90% reduction!)
- **Performance**: Faster response times (15-100x faster for cached requests)
- **Scalability**: Better handling of repetitive queries

### Configuration

- **Similarity Threshold**: 0.8 (80% match required)
- **Cache TTL**: 20 minutes (1200 seconds)
- **Embeddings Model**: text-embedding-3-small
- **Cache Storage**: Redis

---

## Lab 2.2: Message Storing with Cosmos DB

Build a persistent audit trail of all LLM interactions by storing prompts and completions.

### Objective

Create a data pipeline from APIM logging through Event Hub to long-term storage in Cosmos DB.

### What You'll Learn

- Built-in LLM Logging: Capture prompts and completions automatically
- Event Hub Integration: Stream logging data to Event Hub
- Stream Analytics: Process and transform log data in flight
- Cosmos DB Storage: Persist structured interaction data
- Document Querying: Query stored interactions for audit and analysis
- Data Pipeline: Understand full flow from API to persistent storage
- Scalable Architecture: Handle high-volume LLM interactions

### How It Works

1. User request processed by APIM
2. Built-in logging captures prompt, completion, and metadata
3. Logs sent to Azure Monitor
4. Diagnostic settings export logs to Event Hub
5. Stream Analytics consumes Event Hub messages
6. Analytics transforms and enriches message data
7. Data written to Cosmos DB for long-term storage
8. Applications query Cosmos DB for interaction history

### Data Flow Diagram

```
[APIM] → [Azure Monitor] → [Event Hub] → [Stream Analytics] → [Cosmos DB]
```

### Sample Cosmos DB Query

```kusto
SELECT c.user_id, c.prompt, c.completion, c.token_count, c.timestamp
FROM messages c
WHERE c.timestamp > GetCurrentTimestamp() - 3600
ORDER BY c.timestamp DESC
```

### Expected Results

- Prompts and completions logged to Azure Monitor
- Logs appear in Event Hub within seconds
- Stream Analytics job processes and transforms data
- Documents appear in Cosmos DB within 1-2 minutes
- Can query stored interactions by user, timestamp, model
- Audit trail shows complete interaction history
- Token metrics aggregated and stored

---

## Lab 2.3: Vector Searching with RAG

Implement Retrieval Augmented Generation (RAG) to enhance Azure OpenAI responses with current information.

### Objective

Implement RAG to search vector embeddings in Azure AI Search and augment LLM responses with retrieved documents.

### What You'll Learn

- Vector Embeddings: Convert documents and queries to embeddings
- Azure AI Search: Index and search documents using vector similarity
- RAG Pattern: Combine retrieval with generative AI for accurate responses
- Prompt Augmentation: Add retrieved context to LLM prompts
- End-to-End Flow: From document ingestion through response generation
- APIM Gateway: Route embedding and search requests through APIM

### How It Works

1. Knowledge base documents uploaded and indexed in Azure AI Search
2. Each document chunked and embedded using text-embedding-3-small
3. Vector embeddings stored in AI Search index
4. User asks question to APIM gateway
5. Question embedded using same embedding model
6. AI Search performs vector similarity search
7. Top matching documents retrieved and ranked
8. Retrieved documents added to LLM prompt as context
9. Azure OpenAI generates response augmented with retrieved information
10. Response returned to user with source attribution

### Data Flow

```
[Documents] → [Chunking] → [Embedding] → [AI Search Index]
                                            ↓
[User Query] → [Embedding] → [Vector Search] → [Top Results]
                                                  ↓
[Context + Query] → [Azure OpenAI] → [Augmented Response]
```

### Key Metrics

- Embedding generation latency: <1 second per query
- Vector search latency: <500ms
- Response generation: 2-5 seconds depending on context
- Accuracy: Measured by user satisfaction with RAG responses

### Expected Results

- Documents successfully indexed with embeddings
- Vector search returns relevant documents
- Retrieved context properly formatted for LLM
- Azure OpenAI generates contextually accurate responses
- Source documents attributed in responses
- Search relevance improves with better document chunking
- Response quality enhanced by augmentation

---

## Lab 2.4: Built-in LLM Logging

Implement comprehensive observability for LLM interactions using Azure's built-in logging capabilities.

### Objective

Capture and analyze all LLM interactions including prompts, completions, and token metrics using Azure Monitor.

### What You'll Learn

- Built-in LLM Logging: Capture prompts and completions automatically
- Log Analytics Integration: Query interaction data in Log Analytics
- Application Insights: Track performance metrics and failures
- Diagnostic Settings: Configure what data to log and where
- Query Language (KQL): Write queries to analyze patterns
- Dashboard Creation: Build monitoring dashboards for operations

### How It Works

1. Request arrives at APIM gateway
2. Built-in logging policy captures request and response
3. Extracts prompt, completion, and metadata
4. Sends logs to Azure Monitor
5. Logs indexed in Log Analytics workspace
6. Can query logs using KQL
7. Create dashboards and alerts based on patterns

### Key Monitored Data

- User ID and request timestamp
- Prompt text and completion text
- Token counts (prompt, completion, total)
- Model name and deployment
- Response time and status
- Content safety verdicts

### Sample KQL Query

```kusto
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.APIMANAGEMENT"
| where Category == "GatewayLogs"
| where backendRequestUri contains "openai"
| project TimeGenerated, backendRequestUri, responseCode, latency
| summarize AvgLatency = avg(latency) by tostring(responseCode)
```

### Expected Results

- All API requests logged to Log Analytics workspace
- Application Insights captures latency metrics
- KQL queries return request data successfully
- Can trace individual requests end-to-end
- Dashboards show real-time gateway health
- Alerts trigger on anomalies or threshold violations

---

# Section: MCP Fundamentals

Learn the basics of Model Context Protocol (MCP) and how to integrate MCP servers with your AI gateway.

## MCP Server Integration

MCP servers are initialized with MCPClient providing access to multiple data sources:

- **Excel MCP**: Direct Excel Analytics data access
- **Docs MCP**: Research Documents access
- **GitHub MCP**: GitHub API via APIM
- **Weather MCP**: Weather API via APIM

All configuration is loaded from `.mcp-servers-config` file. No additional initialization needed beyond Cell 11.

### Data Flow

1. AI application sends MCP request to APIM
2. APIM validates OAuth token and enforces policies
3. Request forwarded to MCP server
4. MCP server executes tool and returns result
5. APIM proxies response back to client
6. AI model processes tool result and generates response

### Two MCP Connection Patterns

#### Pattern 1: HTTP-Based MCP (Used in this notebook)

**How It Works:**
- Protocol: HTTP POST requests
- Endpoint: `{server_url}/mcp/`
- Format: JSON-RPC 2.0
- Communication: Request/response pattern

**Advantages:**
- Simple, reliable, works with standard HTTP clients
- Easy to test with curl or Postman
- Works through standard load balancers and API gateways
- No special client libraries required
- Firewall-friendly (standard HTTP/HTTPS)

#### Pattern 2: Stdio Transport (Direct Integration)

**How It Works:**
- Protocol: stdin/stdout communication
- Direct process spawning
- Suitable for local/internal integrations

---

## MCP Exercises

### Exercise 2.2: Sales Analysis via MCP + AI

Use MCP for data access and Azure OpenAI for all analysis.

Retrieves sales data from Excel MCP and performs analysis using Azure OpenAI.

### Exercise 2.3: Azure Cost Analysis via MCP

Analyzes Azure cost data through MCP integration.

### Exercise 2.4: Function Calling with MCP Tools

Demonstrates how to call MCP tools directly from Azure OpenAI function calling.

### Exercise 2.5: Dynamic Column Analysis

Performs dynamic analysis of data columns using MCP and AI.

---

## Lab 3.2: GitHub Repository Access

Access and analyze GitHub repositories through MCP integration.

### Objective

Enable your AI applications to read GitHub repository contents and perform code analysis.

### What You'll Learn

- GitHub MCP Integration: Access GitHub API through MCP
- Repository Navigation: Browse repository structure
- File Reading: Retrieve file contents for analysis
- Commit History: Access version history and commits
- Issue Management: Read issues and pull requests
- Integration with AI: Use retrieved data with Azure OpenAI

### How It Works

1. MCP server initialized with GitHub credentials
2. Application requests specific repository contents
3. MCP translates request to GitHub API calls
4. GitHub data retrieved and formatted
5. Data returned to application for processing
6. AI model analyzes retrieved contents

### Data Flow

```
[GitHub] ← [MCP Server] ← [APIM] ← [AI Application]
```

### MCP Server Configuration

```python
github_config = {
    "type": "github",
    "endpoint": "https://api.github.com",
    "credentials": "GitHub Token"
}
```

### Example Use Cases

1. **Code Review Automation**: Review PRs with AI analysis
2. **Documentation Generation**: Generate docs from code
3. **Issue Analysis**: Analyze issues for patterns
4. **Dependency Auditing**: Check for security vulnerabilities
5. **Code Search**: Find patterns across repositories

### Expected Results

- Successfully authenticated with GitHub
- Can read repository structure
- File contents retrieved for analysis
- Commit history accessible
- AI analysis integrates with retrieved data
- Results include source attribution

---

## Lab 3.3: GitHub + AI Code Analysis

Perform comprehensive code analysis combining GitHub access with Azure OpenAI intelligence.

### Objective

Build an end-to-end code analysis pipeline that uses GitHub as data source and Azure OpenAI for intelligent analysis.

### What You'll Learn

- Repository Cloning: Clone repositories for analysis
- Code Parsing: Extract code structure and dependencies
- Intelligent Analysis: Use AI for code quality assessment
- Documentation: Auto-generate documentation
- Vulnerability Detection: Identify security issues
- Pattern Recognition: Find code patterns and best practices
- Multi-File Analysis: Analyze dependencies across files

### What You'll Do

1. Clone or access GitHub repositories
2. Extract code files and structure
3. Send code to Azure OpenAI for analysis
4. Generate analysis reports
5. Identify issues and recommendations
6. Create documentation

### How It Works

1. Repository contents retrieved via GitHub MCP
2. Code files parsed and organized
3. Code chunks formatted for AI analysis
4. Sent to Azure OpenAI with analysis prompts
5. AI generates detailed analysis
6. Results compiled into report
7. Recommendations and improvements suggested

### Analysis Pipeline

```
[GitHub Repo] → [Code Extraction] → [Chunking] → [Azure OpenAI Analysis]
                                                        ↓
                                               [Analysis Report]
```

### Advanced Techniques (Phase 3)

- **Multi-Agent Analysis**: Different agents for different analysis types
- **Streaming Analysis**: Real-time analysis updates
- **Function Calling**: Use AI function calling for structured analysis
- **Semantic Kernel Integration**: Use SK for orchestration
- **AutoGen Collaboration**: Multi-agent code review

### Analysis Outputs

- **Code Quality Report**: Overall quality metrics
- **Issues Found**: Bugs, vulnerabilities, antipatterns
- **Recommendations**: Suggestions for improvements
- **Documentation**: Generated API docs and comments
- **Architecture Overview**: System design analysis
- **Dependency Map**: Visualization of dependencies

### Expected Results

- Successfully access GitHub repositories
- Retrieve and analyze code contents
- Azure OpenAI generates meaningful analysis
- Detailed reports identify issues
- Recommendations are actionable
- Can handle multi-language codebases
- Results include confidence scores

---

# Section 3: AI Foundry & Integrations

Advanced integrations with AI Foundry, Semantic Kernel, and AutoGen.

## Lab 3.1: AI Foundry SDK

Integrate Azure AI Foundry SDK with your APIM gateway for native development patterns.

### Objective

Route all LLM requests through the API gateway while using native AI Foundry development patterns.

### What You'll Learn

- AI Foundry SDK: Use Python SDK for AI Foundry projects
- Connection Configuration: Configure Azure OpenAI connections with APIM endpoint
- Gateway Routing: Route SDK requests through APIM automatically
- Model Catalog: Access AI Foundry model catalog through APIM
- Policy Application: All APIM policies apply to SDK requests
- Authentication: Handle credentials seamlessly with APIM integration
- Development Patterns: Use native SDK patterns with gateway benefits

### How It Works

1. Developer creates Azure AI Foundry project with AI Foundry SDK
2. AI Foundry project has OpenAI connection configured
3. OpenAI connection specifies APIM endpoint as the provider
4. Developer uses standard AI Foundry SDK code
5. SDK requests go to APIM instead of direct Azure OpenAI
6. APIM applies all configured policies:
   - Load balancing
   - Rate limiting
   - Content safety
   - Token metrics
   - Semantic caching
   - Logging
7. Requests forwarded to backend Azure OpenAI
8. Responses returned through APIM to application

### Connection Configuration Format

```
Provider: Azure OpenAI
Endpoint: https://{APIM_GATEWAY}.azure-api.net
Key: {APIM_SUBSCRIPTION_KEY}
API Version: 2024-08-01-preview
```

### Key Benefits

1. **Centralized Governance**: All AI Foundry SDK requests through APIM policies
2. **Unified Monitoring**: Track all interactions in one place
3. **Multi-Region Support**: APIM load balancing benefits
4. **Cost Control**: Token metrics and rate limiting
5. **Security**: All APIM security policies applied

### Expected Results

- AI Foundry SDK initializes successfully
- Requests are routed through APIM (visible in APIM logs)
- Chat completions work through SDK
- All APIM policies apply to SDK requests
- Can track SDK usage in APIM analytics
- No code changes needed to use APIM gateway
- Token metrics appear in Application Insights

---

## Semantic Kernel & AutoGen Integration

Advanced orchestration using Semantic Kernel and AutoGen with Azure OpenAI through APIM.

### Testing Phases

Three phases of integration testing with increasing complexity.

---

## Phase 3, Cell 1: SK Plugin for Gateway-Routed Function Calling

Implement Semantic Kernel plugins with requests routed through the APIM gateway.

### Capabilities

- Create custom SK plugins
- Call plugins through gateway
- Handle function responses
- Track metrics for plugin calls

---

## Phase 3, Cell 2: SK Streaming Chat with Function Calling

Implement streaming chat interactions with function calling in Semantic Kernel.

### Capabilities

- Streaming chat responses
- Function calling within streams
- Real-time token tracking
- Progressive result rendering

---

## Phase 3, Cell 3: AutoGen Multi-Agent Conversation via APIM

Implement multi-agent conversations using AutoGen with APIM routing.

### Capabilities

- Define multiple agents
- Agent collaboration patterns
- Message routing through APIM
- Conversation logging and metrics

---

## Phase 3, Cell 4: SK Agent with Custom Azure OpenAI Client

Create Semantic Kernel agents with custom Azure OpenAI client configuration.

### Capabilities

- Custom client initialization
- Agent-specific configuration
- Advanced request handling
- Enhanced error management

---

## Phase 3, Cell 5: Hybrid SK + AutoGen Orchestration

Combine Semantic Kernel and AutoGen for complex orchestration patterns.

### Capabilities

- Mix SK and AutoGen agents
- Hybrid workflow patterns
- Cross-platform tool calling
- Advanced state management

---

## Appendix: Lab Structure Summary

### Core AI Gateway Labs (Lab 1.x)

| Lab | Title | Focus Area |
|-----|-------|-----------|
| 1.1 | Zero to Production | Foundation setup |
| 1.2 | Backend Pool Load Balancing | Multi-region routing |
| 1.3 | Token Metrics Emitting | Cost monitoring |
| 1.4 | Access Controlling | OAuth authentication |
| 1.5 | Content Safety | Harmful content filtering |
| 1.6 | Model Routing | Intelligent model selection |

### Advanced Features Labs (Lab 2.x)

| Lab | Title | Focus Area |
|-----|-------|-----------|
| 2.1 | Semantic Caching | Performance optimization |
| 2.2 | Message Storing | Persistent audit trails |
| 2.3 | Vector Searching with RAG | Knowledge augmentation |
| 2.4 | Built-in LLM Logging | Comprehensive observability |

### Integration Labs (Lab 3.x)

| Lab | Title | Focus Area |
|-----|-------|-----------|
| 3.1 | AI Foundry SDK | SDK integration |
| 3.2 | GitHub Repository Access | Code access patterns |
| 3.3 | GitHub + AI Code Analysis | Code intelligence |

### MCP & Advanced Integration

| Component | Purpose |
|-----------|---------|
| MCP Fundamentals | Learn MCP basics and integration |
| SK & AutoGen | Advanced orchestration patterns |
| Phase 3 Cells | Testing and validation phases |

---

**Last Updated**: November 23, 2025
**Total Sections**: 4 Main + Appendix
**Total Labs**: 10 Core + 3 Integration
**Total Exercises**: 10+ Hands-on Exercises
