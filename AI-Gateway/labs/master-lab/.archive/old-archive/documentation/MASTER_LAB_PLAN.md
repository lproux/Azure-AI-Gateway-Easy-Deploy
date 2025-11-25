# Master AI Gateway Lab - Implementation Plan

## Overview
This document outlines the plan for consolidating 31 AI Gateway labs into a single master lab with comprehensive testing capabilities.

## Scope

### Labs Included (31 total)
Organized by learning sequence:

#### 1. Foundation & Basics
1. **zero-to-production** - Core APIM + AI Foundry setup, load balancing, token metrics, rate limiting

#### 2. Core Features
2. **backend-pool-load-balancing** - Load balancing across multiple regions (priority/weight)
3. **backend-pool-load-balancing-tf** - Load balancing with Terraform
4. **built-in-logging** - Logging and observability
5. **token-metrics-emitting** - Token usage tracking
6. **token-rate-limiting** - Rate limiting by tokens

#### 3. Security & Access Control
7. **access-controlling** - OAuth 2.0 authorization with Microsoft Entra ID
8. **content-safety** - Azure AI Content Safety integration
9. **private-connectivity** - Private endpoints and VNETs

#### 4. Model Management
10. **model-routing** - Intelligent model routing based on criteria
11. **ai-foundry-sdk** - Azure AI Foundry SDK integration
12. **ai-foundry-deepseek** - DeepSeek model integration

#### 5. Model Context Protocol (MCP) & Agents
13. **model-context-protocol** - MCP basics with GitHub OAuth (skip ServiceNow)
14. **mcp-from-api** - Convert existing APIs to MCP servers
15. **mcp-client-authorization** - MCP OAuth authorization
16. **mcp-a2a-agents** - Agent-to-Agent communication via MCP
17. **mcp-registry-apic** - MCP registry with API Center
18. **mcp-registry-apic-github-workflow** - CI/CD for MCP servers

#### 6. AI Agent Services
19. **openai-agents** - OpenAI Assistants API integration
20. **ai-agent-service** - Azure AI Agent Service
21. **realtime-mcp-agents** - Realtime MCP agents

#### 7. Advanced Features
22. **function-calling** - Function calling with LLMs
23. **semantic-caching** - Semantic caching with Redis
24. **message-storing** - Message persistence
25. **vector-searching** - Vector search integration
26. **image-generation** - Image generation (DALL-E, FLUX)
27. **realtime-audio** - Realtime audio with OpenAI
28. **slm-self-hosting** - Self-hosted small language models
29. **session-awareness** - Session management

#### 8. FinOps & Monitoring
30. **finops-framework** - Cost management and chargeback
31. **secure-responses-api** - Secure API responses
32. **token-metrics-emitting** - (already covered above)

### Labs Explicitly Excluded
- **_deprecated/** - All deprecated labs
- **aws-bedrock** - Requires AWS credentials
- **gemini-mcp-agents** - Requires Google Cloud credentials

## Master Resource Structure

### Single Resource Group: `lab-master-lab`

### Core Infrastructure (Deployed Once)
1. **API Management**
   - SKU: `Basicv2` (can be upgraded to `StandardV2` or `Premium` if needed)
   - Single gateway for all APIs
   - All 31 lab features configured as APIs/operations

2. **AI Foundry Hub + Project**
   - Single hub in one region
   - All models deployed to this project:
     - **Chat Models**: gpt-4o-mini, gpt-4.1, gpt-4.1-mini, gpt-4o (if needed)
     - **Image Models**: gpt-image-1, DALL-E-3, FLUX-1.1-pro
     - **Embedding Models**: text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002
     - **Specialized Models**: DeepSeek-R1, Phi-4
     - **Realtime Models**: gpt-4o-realtime-preview

3. **Supporting Services**
   - **Redis Cache** (Managed Redis - for semantic caching)
   - **Azure AI Content Safety** - Content moderation
   - **Log Analytics Workspace** - Centralized logging
   - **Application Insights** - Monitoring and metrics
   - **Container Registry** - For MCP server images
   - **Container Apps** - For MCP servers:
     - Weather MCP server
     - Oncall MCP server
     - GitHub MCP server
     - Product catalog MCP server
     - More as needed
   - **Azure Search** - For vector searching
   - **Cosmos DB** - For message storage (optional, for session awareness)

4. **Networking** (if private connectivity lab is included)
   - Virtual Network
   - Private Endpoints for APIM and AI Foundry

5. **Identity & Access**
   - Managed Identity for APIM
   - App Registration for OAuth flows
   - Credential Manager providers (GitHub OAuth)

## File Structure

```
master-lab/
├── master-ai-gateway.ipynb       # Main notebook with all features
├── master-cleanup.ipynb           # Cleanup all resources
├── master-deployment.bicep        # Consolidated Bicep with ALL resources
├── params.json                    # Generated parameters file
├── README.md                      # Comprehensive documentation
├── MASTER_LAB_PLAN.md             # This planning document
├── analyze_labs.py                # Lab analysis script
├── policies/                      # All APIM policies
│   ├── access-controlling-policy.xml
│   ├── backend-pool-load-balancing-policy.xml
│   ├── content-safety-policy.xml
│   ├── semantic-caching-policy.xml
│   ├── token-rate-limiting-policy.xml
│   ├── ... (71 total policies)
├── src/                          # Source code for MCP servers and utilities
│   ├── weather/
│   ├── oncall/
│   ├── github/
│   ├── product-catalog/
│   └── ...
└── diagrams/                     # Architecture diagrams
    └── master-architecture.png
```

## Master Notebook Structure

### Estimated Size
- **~500-600 cells** (based on ~20 cells per lab × 31 labs)
- **Organized sequentially** by the learning path above
- **Fully expanded** test sections for each feature

### Notebook Sections

1. **Master Initialization** (Single section for all labs)
   - Import all required libraries
   - Set up master configuration
   - One credential setup (Azure CLI authentication)
   - Master resource naming

2. **One-Time Deployment** (Single deployment of all resources)
   - Deploy master-deployment.bicep
   - Wait for completion (~30-60 minutes)
   - Retrieve all outputs

3. **Lab Sections** (31 sections, one per lab)
   Each section includes:
   - Feature introduction/explanation
   - Configuration specific to that feature
   - API policy update (if applicable)
   - Fully expanded test examples:
     - HTTP requests with `requests` library
     - Azure OpenAI SDK examples
     - Agent framework examples (Semantic Kernel, AutoGen, etc.)
     - Visualization/analysis (plots, charts)
   - Verification and validation

4. **Master Cleanup Reference**
   - Link to master-cleanup.ipynb

## Master Bicep File Strategy

**Approach**: One giant master.bicep file with ALL resources

### Structure
```bicep
// Parameters (consolidated from all labs)
param apimSku string = 'Basicv2'
param location string = resourceGroup().location
param aiFoundryLocation string
param modelsConfig array = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
  { name: 'gpt-4.1', publisher: 'OpenAI', version: '2025-04-14', sku: 'GlobalStandard', capacity: 100 }
  // ... all other models
]
// ... more parameters

// Modules/Resources
module logging 'logging.bicep'                    // Log Analytics + App Insights
module aiFoundry 'ai-foundry.bicep'               // Hub + Project + all Models
module apim 'apim.bicep'                          // APIM + all APIs + backends
module redis 'redis.bicep'                        // Redis cache for semantic caching
module contentSafety 'content-safety.bicep'       // Content Safety service
module containerRegistry 'acr.bicep'              // Container Registry
module containerApps 'container-apps.bicep'       // All MCP servers
module search 'search.bicep'                      // Azure Search for vector search
module cosmosdb 'cosmos.bicep'                    // Cosmos DB for message storage
module networking 'networking.bicep'              // VNet + Private Endpoints (optional)
module identity 'identity.bicep'                  // Managed Identities + RBAC

// Outputs (all deployment outputs)
output apimGatewayUrl string
output aiFoundryProjectEndpoint string
// ... all other outputs
```

### Estimated Size
- **~2000-3000 lines** of Bicep code
- Modular where possible, but all in one deployment

## Consolidated Models List

Based on analysis, here are ALL unique models to deploy:

### Chat Completion Models
1. `gpt-4o-mini` - Most common, cost-effective
2. `gpt-4.1-mini` - Newer mini variant
3. `gpt-4.1` - Latest GPT-4 Turbo
4. `gpt-4o` - Standard GPT-4
5. `gpt-4o-realtime-preview` - For realtime audio

### Image Generation Models
6. `gpt-image-1` - OpenAI's latest image model (gated, may require request)
7. `DALL-E-3` - DALL-E 3
8. `FLUX-1.1-pro` - Black Forest Labs model

### Embedding Models
9. `text-embedding-3-small` - For semantic caching/search
10. `text-embedding-3-large` - Larger embedding model
11. `text-embedding-ada-002` - Legacy embedding model

### Specialized Models
12. `DeepSeek-R1` - DeepSeek reasoning model
13. `Phi-4` - Microsoft's small language model
14. `o1-preview` - OpenAI's o1 model (if available)

## Policy Files Organization

All 71 policy XML files will be copied to `master-lab/policies/` with clear naming:

- `lab-name-feature-policy.xml` format
- Examples:
  - `access-controlling-jwt-validation-policy.xml`
  - `backend-pool-load-balancing-retry-policy.xml`
  - `semantic-caching-lookup-policy.xml`
  - `content-safety-validation-policy.xml`

## Master README Structure

```markdown
# Master AI Gateway Lab

## Overview
Complete reference implementation combining all 31 AI Gateway labs

## Quick Start
1. Prerequisites
2. Clone repository
3. Run master deployment
4. Execute master notebook

## Architecture
- Diagram showing all integrated components
- Resource list with descriptions

## Features (31 labs)
- Organized by category
- Links to specific sections in master notebook

## Cost Estimation
- Breakdown by resource
- Estimated monthly cost

## Troubleshooting
- Common issues
- How to use tracing

## Contributing
## License
```

## Implementation Timeline

### Phase 1: Infrastructure Files
1. ✅ Create folder structure
2. ✅ Create analysis script
3. ⏳ Create master-deployment.bicep
4. ⏳ Copy all policy files to policies/

### Phase 2: Documentation
5. ⏳ Create comprehensive README.md
6. ⏳ Create architecture diagrams

### Phase 3: Notebooks
7. ⏳ Create master-ai-gateway.ipynb (large file!)
8. ⏳ Create master-cleanup.ipynb

### Phase 4: Testing & Validation
9. Test deployment
10. Validate all 31 features work

## Questions for Confirmation

1. **Bicep Approach**: Confirm single large master.bicep (~2000-3000 lines) is acceptable?
2. **Notebook Size**: Confirm single notebook with ~500-600 cells is acceptable?
3. **Model Selection**: Any specific models to prioritize or exclude?
4. **Region Selection**: Which Azure region should be primary for resources?
5. **APIM SKU**: Start with Basicv2 or go straight to StandardV2/Premium?
6. **Private Connectivity**: Include VNet/Private Endpoint setup or skip for simplicity?
7. **Cost Budget**: Any constraints on deployed resources (e.g., skip expensive resources)?

## Next Steps

Please review this plan and confirm:
- ✅ The structure looks good
- ✅ The scope is correct (31 labs)
- ✅ Approach is acceptable (one big deployment, one big notebook)
- ✅ Any modifications needed

Once confirmed, I will proceed with generating:
1. master-deployment.bicep (~2500 lines)
2. master-ai-gateway.ipynb (~500-600 cells)
3. master-cleanup.ipynb (~50 cells)
4. README.md (comprehensive documentation)
5. All 71 policy files copied and organized
