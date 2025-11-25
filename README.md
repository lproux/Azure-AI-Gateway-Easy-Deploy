# AI Gateway & Azure OpenAI Integration Repository

Comprehensive collection of Azure AI Gateway implementations, Azure OpenAI with API Management patterns, and AI development resources. This repository consolidates production-ready patterns for enterprise AI deployment on Azure.

## Repository Overview

This repository contains **three major implementation areas**, each providing different approaches to building enterprise-grade AI solutions on Azure:

### 1. **AI-Gateway** - Azure AI Gateway Labs & Samples
   📂 Location: [`AI-Gateway/`](./AI-Gateway/)

   Official Azure samples demonstrating Microsoft Copilot plugin interoperability and comprehensive AI Gateway patterns using Azure API Management.

   **Original Repository:** [Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway)

   **What's Inside:**
   - 🧪 **30+ Hands-on Labs** covering AI agents, MCP integration, function calling, and production patterns
   - 🌟 **Master Lab** - Deploy once, explore 7 comprehensive labs in a single notebook experience
   - 🔐 **Security** - OAuth 2.0, JWT validation, managed identities
   - ⚡ **Performance** - Semantic caching, load balancing, multi-region deployments
   - 💰 **Cost Management** - Token limiting, FinOps framework, chargeback models
   - 🤖 **AI Agents** - OpenAI Agents, Model Context Protocol (MCP), Azure AI Agent Service
   - 📊 **Observability** - Built-in logging, token metrics, compliance monitoring

### 2. **AzureOpenAI-with-APIM** - Enterprise-Grade APIM Integration
   📂 Location: [`AzureOpenAI-with-APIM/`](./AzureOpenAI-with-APIM/)

   Production-ready reference implementation for managing Azure OpenAI through API Management, focusing on enterprise governance, cost control, and operational excellence.

   **Original Repository:** [microsoft/AzureOpenAI-with-APIM](https://github.com/microsoft/AzureOpenAI-with-APIM)

   **What's Inside:**
   - 🚀 **One-Click Deployment** - Deploy APIM, Key Vault, and Log Analytics with auto-configuration
   - 🔄 **Resiliency** - Multi-region retry policies, automatic failover
   - 📈 **Scalability** - Load balancing across multiple Azure OpenAI endpoints
   - 💎 **Performance** - Provisioned Throughput Units (PTU), priority-based routing
   - 💵 **Cost Management** - Token rate limiting, chargeback models, Power BI reporting
   - 🔒 **Security** - Managed identities, private endpoints, zero-trust architecture
   - 📊 **Monitoring** - Log Analytics integration, KQL queries, usage tracking

### 3. **ai-for-developers-main** - AI Development Resources
   📂 Location: [`ai-for-developers-main/`](./ai-for-developers-main/)

   Documentation, best practices, and guidance for building secure AI applications with MCP and GitHub Copilot integration.

---

## 🚀 Getting Started

### Quick Deploy Options

#### Option 1: Master Lab (Recommended for Learning)

Deploy a comprehensive environment with 7 labs in a single Jupyter notebook:

```bash
cd AI-Gateway/labs/master-lab

# Deploy with Azure Developer CLI
az login
azd up
```

**What gets deployed:**
- API Management (StandardV2)
- 3 AI Foundry Hubs (multi-region)
- 7 AI Models (GPT-4o, GPT-4, DALL-E-3, embeddings)
- Redis Enterprise (semantic caching)
- Azure AI Search (vector search)
- Cosmos DB (message storage)
- 7 MCP servers (Container Apps)
- Log Analytics + Application Insights

**Time:** 35-40 minutes
**Cost:** ~$890-1,190/month (varies by usage)

[📖 Master Lab Documentation](./AI-Gateway/labs/master-lab/README.md)

#### Option 2: APIM-Focused Deployment (Production-Ready)

Deploy enterprise-grade APIM for Azure OpenAI management:

```bash
cd AzureOpenAI-with-APIM

# One-button deploy via Azure Portal
# Click: Deploy to Azure button in README

# Or via Azure CLI
az login
az group create --name RG-APIM-OpenAI --location eastus
az deployment group create \
  --resource-group RG-APIM-OpenAI \
  --template-file public-apim.bicep
```

**What gets deployed:**
- API Management
- Key Vault
- Log Analytics
- Auto-configuration for Azure OpenAI
- Token monitoring policies
- Cost management policies

**Time:** 45 minutes
**Cost:** ~$175/month base + usage

[📖 APIM Deployment Guide](./AzureOpenAI-with-APIM/README.md)

#### Option 3: Individual Labs (Modular Learning)

Explore specific capabilities with targeted labs:

```bash
cd AI-Gateway/labs

# Choose your lab:
# - access-controlling/      # OAuth 2.0 & JWT validation
# - backend-pool-load-balancing/  # Multi-region load balancing
# - semantic-caching/        # Redis-backed intelligent caching
# - model-context-protocol/  # MCP integration
# - openai-agents/          # AI agent orchestration
# - finops-framework/        # Cost management
# - built-in-logging/        # Token metrics & monitoring

# Each lab has its own deployment
cd <lab-name>
az login
az deployment group create \
  --resource-group <your-rg> \
  --template-file main.bicep
```

[📖 Individual Labs Index](./AI-Gateway/labs/README_DOCUMENTATION_INDEX.md)

---

## 📚 Key Features by Area

### AI-Gateway Labs

<table>
<tr>
<td width="33%">

**AI Agents & MCP**
- Model Context Protocol integration
- OpenAI Agents SDK
- Azure AI Agent Service
- Function calling patterns
- Multi-tool orchestration

</td>
<td width="33%">

**Production Patterns**
- Load balancing (multi-region)
- Semantic caching (5-20x faster)
- Token rate limiting
- Content safety
- Built-in logging

</td>
<td width="33%">

**Security & Compliance**
- OAuth 2.0 authentication
- JWT token validation
- Managed identities
- Message storage (Cosmos DB)
- Access control policies

</td>
</tr>
</table>

### AzureOpenAI-with-APIM Features

<table>
<tr>
<td width="50%">

**Enterprise Governance**
- Subscription-based access control
- Priority-based routing
- Circuit breaker patterns
- Private endpoint support
- Managed identity authentication

</td>
<td width="50%">

**Cost & Operations**
- Token usage tracking per subscription
- Chargeback models & reporting
- Power BI dashboard integration
- Log Analytics queries (KQL)
- Alert automation with Logic Apps

</td>
</tr>
</table>

---

## 🏗️ Architecture Patterns

### Master Lab Architecture
```
┌─────────────────────────────────────────┐
│    API Management (StandardV2)          │
│  ┌───────────────────────────────────┐  │
│  │ • Access Control (OAuth/JWT)      │  │
│  │ • Semantic Caching (Redis)        │  │
│  │ • Message Storing (Cosmos DB)     │  │
│  │ • Load Balancing (Multi-region)   │  │
│  │ • MCP Integration (7 servers)     │  │
│  │ • Built-in Logging (App Insights) │  │
│  └───────────────────────────────────┘  │
└─────────┬──────────┬──────────┬─────────┘
          │          │          │
    ┌─────▼───┐ ┌────▼────┐ ┌──▼──────┐
    │ Foundry │ │ Foundry │ │ Foundry │
    │ UK South│ │ Sweden C│ │ West EU │
    │ 7 Models│ │ 1 Model │ │ 1 Model │
    └─────────┘ └─────────┘ └─────────┘
```

### APIM Enterprise Architecture
```
┌──────────────────────────────────────┐
│  Client Applications & Services      │
│  (OAuth 2.0 / Managed Identity)      │
└──────────────┬───────────────────────┘
               │
    ┌──────────▼──────────┐
    │  Azure APIM Gateway │
    │  • Token Limiting   │
    │  • Load Balancing   │
    │  • Retry Policies   │
    │  • Logging & Metrics│
    └──────────┬──────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼──────┐   ┌──────▼──────┐
│ Azure AOAI │   │ Azure AOAI  │
│ Region 1   │   │ Region 2    │
│ (Primary)  │   │ (Failover)  │
└────────────┘   └─────────────┘
```

---

## 📖 Documentation Index

### Primary Documentation

| Area | Documentation | Description |
|------|---------------|-------------|
| **Master Lab** | [Master Lab README](./AI-Gateway/labs/master-lab/README.md) | Comprehensive 7-in-1 lab experience |
| **Individual Labs** | [Labs Index](./AI-Gateway/labs/README_DOCUMENTATION_INDEX.md) | 30+ modular labs |
| **APIM Integration** | [APIM Guide](./AzureOpenAI-with-APIM/README.md) | Enterprise APIM patterns |
| **AI Gateway Concepts** | [AI Gateway README](./AI-Gateway/README.md) | Overview and concepts |

### Specialized Guides

| Topic | Guide | Details |
|-------|-------|---------|
| **MCP Integration** | [MCP Lab](./AI-Gateway/labs/model-context-protocol/) | Model Context Protocol implementation |
| **OpenAI Agents** | [Agents Lab](./AI-Gateway/labs/openai-agents/) | AI agent orchestration |
| **Semantic Caching** | [Caching Lab](./AI-Gateway/labs/semantic-caching/) | Redis-backed intelligent caching |
| **Load Balancing** | [Load Balancing Lab](./AI-Gateway/labs/backend-pool-load-balancing/) | Multi-region distribution |
| **Cost Management** | [FinOps Lab](./AI-Gateway/labs/finops-framework/) | Budget control & chargeback |
| **Vector Search** | [Vector Search Lab](./AI-Gateway/labs/vector-searching/) | RAG pattern implementation |
| **Access Control** | [Security Lab](./AI-Gateway/labs/access-controlling/) | OAuth 2.0 & JWT validation |
| **Token Monitoring** | [Logging Lab](./AI-Gateway/labs/built-in-logging/) | Usage tracking & analytics |

---

## 🔧 Prerequisites

### Azure Requirements

- **Azure Subscription** with appropriate permissions:
  - [Contributor](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#contributor) + [RBAC Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#role-based-access-control-administrator)
  - OR [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#owner) role
- **Azure OpenAI** access (request access if needed: [Request Access](https://aka.ms/oai/access))

### Development Tools

```bash
# Required
- Python 3.11 or later
- Azure CLI 2.50 or later
- VS Code with Jupyter extension

# Optional (for specific labs)
- Docker Desktop (for MCP server development)
- Node.js 20.x (for MCP servers)
- Azure Developer CLI (azd)
```

### Quick Setup

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash  # Linux
# Or: https://learn.microsoft.com/cli/azure/install-azure-cli

# Install Azure Developer CLI (azd)
curl -fsSL https://aka.ms/install-azd.sh | bash  # Linux/macOS
# Or: https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd

# Login to Azure
az login
az account set --subscription <your-subscription-id>

# Clone this repository
git clone https://github.com/lproux/MCP-servers-internalMSFT-and-external.git
cd MCP-servers-internalMSFT-and-external
```

---

## 💰 Cost Estimation

### Master Lab (Comprehensive)
| Service | Monthly Cost | Notes |
|---------|--------------|-------|
| API Management StandardV2 | ~$175 | Core gateway |
| AI Foundry (3 regions) | ~$0 base | Usage-based |
| AI Model Usage | ~$500-800 | Varies by usage |
| Redis Enterprise | ~$20 | Caching |
| Azure AI Search | ~$75 | Vector search |
| Cosmos DB | ~$25 | Message storage |
| Container Apps | ~$30 | MCP servers |
| Log Analytics | ~$50 | Monitoring |
| **TOTAL** | **~$890-1,190** | Per month |

### APIM-Focused Deployment
| Service | Monthly Cost | Notes |
|---------|--------------|-------|
| API Management | ~$175 | Production-ready |
| Key Vault | ~$0 | Minimal |
| Log Analytics | ~$20 | Basic monitoring |
| **TOTAL** | **~$195** | Base + usage |

**Cost Optimization Tips:**
- Use semantic caching to reduce API calls by 50-80%
- Start with gpt-4o-mini for development (15-20x cheaper)
- Delete resources when not in use: `az group delete --name <rg-name>`
- Enable auto-scaling for APIM to reduce idle costs

---

## 🎯 Learning Paths

### Beginner Path: Start with Master Lab

1. ✅ **Deploy Master Lab** ([Guide](./AI-Gateway/labs/master-lab/README.md))
   ```bash
   cd AI-Gateway/labs/master-lab
   azd up
   ```

2. ✅ **Explore Labs in Order:**
   - Lab 08: Access Control
   - Lab 09: Semantic Caching
   - Lab 10: Message Storing
   - Lab 11: Vector Search

3. ✅ **Review Monitoring:**
   - Lab 12: Built-in Logging
   - Explore Log Analytics queries
   - Review token usage reports

### Intermediate Path: Production Patterns

1. ✅ **Deploy APIM Integration** ([Guide](./AzureOpenAI-with-APIM/README.md))
   ```bash
   cd AzureOpenAI-with-APIM
   # Use Deploy to Azure button or CLI
   ```

2. ✅ **Implement Resiliency:**
   - Configure multi-region backends
   - Add retry policies
   - Test failover scenarios

3. ✅ **Add Cost Management:**
   - Configure token rate limiting
   - Set up chargeback reporting
   - Create Power BI dashboards

### Advanced Path: Custom Integration

1. ✅ **Explore Individual Labs:**
   - Choose specific labs from [Labs Index](./AI-Gateway/labs/README_DOCUMENTATION_INDEX.md)
   - Customize policies for your use case
   - Integrate with existing infrastructure

2. ✅ **Build Custom MCP Servers:**
   - Review MCP Integration lab
   - Deploy custom data sources
   - Create multi-tool orchestration

3. ✅ **Implement Enterprise Patterns:**
   - Private endpoints
   - Custom authentication
   - Advanced monitoring & alerting

---

## 🔐 Security Best Practices

### Authentication Methods (Ordered by Security)

1. **Managed Identity** (Highest Security)
   - No secrets to manage
   - Automatic credential rotation
   - Native Azure integration
   - **Use for:** Production deployments on Azure

2. **Service Principal with Certificate**
   - Certificate-based authentication
   - Auditable access
   - **Use for:** Automated pipelines, CI/CD

3. **Service Principal with Client Secret**
   - Explicit credential management
   - Time-limited secrets
   - **Use for:** Development, testing

4. **API Keys / Subscription Keys**
   - Simple but less secure
   - Manual key rotation
   - **Use for:** Initial testing only

### Security Checklist

- [ ] Enable managed identities for all service-to-service communication
- [ ] Use private endpoints for production deployments
- [ ] Implement JWT token validation for client authentication
- [ ] Enable Azure AD OAuth 2.0 for user authentication
- [ ] Configure Content Safety policies for input validation
- [ ] Store secrets in Azure Key Vault
- [ ] Enable diagnostic logging for audit trails
- [ ] Implement rate limiting and throttling
- [ ] Use Azure DDoS Protection for public endpoints
- [ ] Enable Azure Defender for Cloud

---

## 🛠️ Common Operations

### Deploy Complete Environment

```bash
# Option 1: Master Lab (azd)
cd AI-Gateway/labs/master-lab
az login
azd up --environment production

# Option 2: APIM-focused (Bicep)
cd AzureOpenAI-with-APIM
az login
az group create --name RG-APIM-OpenAI --location eastus
az deployment group create \
  --resource-group RG-APIM-OpenAI \
  --template-file public-apim.bicep \
  --parameters @parameters.json

# Option 3: Individual Lab
cd AI-Gateway/labs/semantic-caching
az login
az deployment group create \
  --resource-group my-rg \
  --template-file main.bicep
```

### Monitor Deployments

```bash
# Check deployment status
az deployment group show \
  --name <deployment-name> \
  --resource-group <rg-name> \
  --query properties.provisioningState

# View all resources
az resource list \
  --resource-group <rg-name> \
  --output table

# Stream deployment logs
az deployment group list \
  --resource-group <rg-name> \
  --output table
```

### Cleanup Resources

```bash
# Delete entire resource group (CAUTION: Irreversible!)
az group delete \
  --name <rg-name> \
  --yes \
  --no-wait

# Verify deletion
az group show --name <rg-name>
# Should return: (ResourceGroupNotFound)

# Delete specific resource
az resource delete \
  --resource-group <rg-name> \
  --name <resource-name> \
  --resource-type <type>
```

### Query Logs & Metrics

```bash
# Token usage by subscription (KQL)
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "
    customMetrics
    | where name in ('Prompt Tokens', 'Completion Tokens')
    | summarize TotalTokens = sum(value) by tostring(customDimensions['Subscription ID'])
  "

# Recent API calls
az apim api operation list \
  --resource-group <rg-name> \
  --service-name <apim-name> \
  --api-id azure-openai-api

# View Application Insights metrics
az monitor app-insights metrics show \
  --app <app-insights-name> \
  --metric requests/count \
  --aggregation count
```

---

## 🔗 External Resources

### Official Documentation

- [Azure API Management](https://learn.microsoft.com/azure/api-management/) - Core gateway service
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/) - AI model hosting
- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-studio/) - AI project management
- [Azure AI Search](https://learn.microsoft.com/azure/search/) - Vector search capabilities
- [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/) - Semantic caching
- [Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/) - Message storage
- [Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/) - Logging & analytics

### Original Source Repositories

- [Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway) - Official Azure samples
- [microsoft/AzureOpenAI-with-APIM](https://github.com/microsoft/AzureOpenAI-with-APIM) - Enterprise APIM patterns

### AI & MCP Concepts

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - Data source integration standard
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) - Agent orchestration
- [Retrieval Augmented Generation (RAG)](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview) - Grounded AI responses
- [Semantic Caching](https://redis.io/blog/what-is-semantic-caching/) - Intelligent response caching

### Community & Support

- [Azure AI Community](https://techcommunity.microsoft.com/azure/cognitive-services) - Forums & discussions
- [GitHub Issues - AI-Gateway](https://github.com/Azure-Samples/AI-Gateway/issues)
- [GitHub Issues - APIM Integration](https://github.com/microsoft/AzureOpenAI-with-APIM/issues)
- [Azure OpenAI Service Limits](https://learn.microsoft.com/azure/ai-services/openai/quotas-limits) - Quota information

---

## 🤝 Contributing

We welcome contributions to all areas of this repository!

### How to Contribute

1. **Fork the repository**
2. **Choose your area:**
   - AI-Gateway labs: Submit to [Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway)
   - APIM patterns: Submit to [microsoft/AzureOpenAI-with-APIM](https://github.com/microsoft/AzureOpenAI-with-APIM)
   - This consolidation: Create PR here

3. **Make your changes:**
   ```bash
   git checkout -b feature/your-feature
   # Make changes
   git commit -m "Add: Your feature description"
   git push origin feature/your-feature
   ```

4. **Create Pull Request** with:
   - Clear description of changes
   - Testing performed
   - Documentation updates
   - Screenshots (if applicable)

### Contribution Areas

- ✨ New lab implementations
- 📝 Documentation improvements
- 🐛 Bug fixes
- 🎨 Bicep/ARM template enhancements
- 📊 Monitoring & analytics examples
- 🔒 Security pattern improvements
- 💰 Cost optimization guides

---

## 📜 License

This repository consolidates content from multiple sources:

- **AI-Gateway**: [MIT License](./AI-Gateway/LICENSE) - See [Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway)
- **AzureOpenAI-with-APIM**: [MIT License](./AzureOpenAI-with-APIM/LICENSE) - See [microsoft/AzureOpenAI-with-APIM](https://github.com/microsoft/AzureOpenAI-with-APIM)
- **Consolidation & Additional Content**: MIT License

---

## 🙏 Acknowledgments

This repository builds upon the outstanding work of multiple teams and contributors from Microsoft and the Azure community. We extend our sincere gratitude to:

### Original Repository Owners & Contributors

**[Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway)**
- Created and maintained by the **Microsoft Azure Samples Team**
- Special thanks to all contributors who developed the comprehensive lab experiences, MCP integration patterns, and production-ready templates
- This repository forms the foundation of the AI Gateway patterns and the Master Lab experience

**[microsoft/AzureOpenAI-with-APIM](https://github.com/microsoft/AzureOpenAI-with-APIM)**
- Created and maintained by the **Microsoft Azure API Management Team**
- Special thanks to the contributors who built the enterprise-grade APIM integration patterns, cost management frameworks, and resiliency implementations
- This repository provides the production-ready APIM reference architecture

### Azure Product Teams

We thank the following Microsoft Azure teams whose products and documentation made this work possible:
- **Azure API Management Team** - For the robust gateway service and comprehensive documentation
- **Azure OpenAI Service Team** - For democratizing access to cutting-edge AI models
- **Azure AI Foundry Team** - For the unified AI development platform
- **Azure AI Search Team** - For powerful vector search capabilities
- **Azure Cache for Redis Team** - For enabling high-performance semantic caching
- **Azure Cosmos DB Team** - For globally distributed database services
- **Azure Container Apps Team** - For simplifying MCP server deployments
- **Azure Monitor Team** - For comprehensive observability tools

### Community Contributors

This consolidated repository benefits from the collective knowledge and feedback of the Azure AI community. Thank you to everyone who:
- Reported issues and provided feedback
- Contributed code improvements and bug fixes
- Shared deployment experiences and best practices
- Created tutorials and educational content

### Open Source Foundations

We acknowledge the broader ecosystem that makes this work possible:
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** - For standardizing AI data source integration
- **[OpenAI](https://openai.com/)** - For pioneering AI models and APIs
- **Open Source Community** - For the countless tools, libraries, and frameworks that power modern AI development

---

**Note:** This repository is a consolidation and enhancement of existing open-source projects. All original work retains its respective licenses and attributions. We strive to properly credit all sources and welcome corrections or additions to these acknowledgments.

---

## 🎓 Support

### Getting Help

1. **Documentation**: Check the relevant README in each folder
2. **Azure Service Health**: [Azure Status](https://status.azure.com/)
3. **GitHub Issues**:
   - AI-Gateway labs: [Create issue](https://github.com/Azure-Samples/AI-Gateway/issues)
   - APIM integration: [Create issue](https://github.com/microsoft/AzureOpenAI-with-APIM/issues)
4. **Azure Support**: [Azure Support Portal](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)

### Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Authentication failed | Run `az login` and verify subscription |
| Quota exceeded | Request increase in Azure Portal > Quotas |
| Deployment timeout | APIM takes 30-45 min (normal), check `az deployment group show` |
| Module not found | Reinstall: `pip install -r requirements.txt` |
| MCP server errors | Check Container Apps logs: `az containerapp logs show` |

---

## 🌟 What Makes This Repository Special

✅ **Three Comprehensive Approaches** - Master Lab, APIM-focused, Individual Labs
✅ **Production-Ready** - Battle-tested patterns used in enterprise deployments
✅ **Well-Documented** - Extensive README files, inline comments, architecture diagrams
✅ **Cost-Conscious** - Built-in cost tracking, optimization tips, transparent pricing
✅ **Security-First** - Managed identities, private endpoints, OAuth 2.0
✅ **Modular Design** - Use what you need, when you need it
✅ **Active Maintenance** - Regularly updated with latest Azure features

---

## 📊 Repository Statistics

- **Total Labs**: 30+ individual labs + Master Lab
- **Deployment Time**: 35-40 minutes (Master Lab)
- **Lines of Documentation**: ~15,000+
- **Azure Services**: 15+ services integrated
- **Authentication Methods**: 3 (Managed Identity, Service Principal, API Keys)
- **Multi-Region Support**: ✅ Load balancing, failover, high availability

---

## Quick Start Summary

```bash
# 1️⃣ Clone Repository
git clone https://github.com/lproux/MCP-servers-internalMSFT-and-external.git
cd MCP-servers-internalMSFT-and-external

# 2️⃣ Choose Your Path

# Master Lab (Recommended for Learning)
cd AI-Gateway/labs/master-lab
az login && azd up

# APIM-Focused (Production-Ready)
cd AzureOpenAI-with-APIM
# Use "Deploy to Azure" button OR:
az deployment group create --resource-group <rg> --template-file public-apim.bicep

# Individual Lab (Modular)
cd AI-Gateway/labs/semantic-caching
az deployment group create --resource-group <rg> --template-file main.bicep

# 3️⃣ Explore & Learn
# Open notebooks, review policies, test deployments

# 4️⃣ Cleanup (When Done)
az group delete --name <rg-name> --yes --no-wait
```

---

**🚀 Ready to build enterprise-grade AI solutions on Azure!**

Last Updated: 2025-11-25
Version: 2.0.0
Maintained by: [LP Roux](https://github.com/lproux)
