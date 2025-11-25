# Azure AI Gateway - Easy Deploy Quick Start

## 5-Minute Active Setup (60 minutes total automated time)

### Prerequisites (2 minutes)

1. **Azure CLI**
   ```bash
   az login
   az account set --subscription <your-subscription-id>
   ```

2. **Python 3.11+**
   ```bash
   pip install -r requirements.txt
   ```

### Deploy (3 minutes active work)

Open `master-ai-gateway-easy-deploy.ipynb`:

1. Run Cell 1-2: Install dependencies
2. Run Cell 3: Enter subscription ID, deployment starts
3. Run Cell 4: Save configuration
4. Wait ~60 minutes (automated)

### Run Labs (30-45 minutes)

5. Run Cell 5+: Execute all lab exercises

**Total time**: 65-75 minutes end-to-end

---

## What You Get

- API Management with OAuth 2.0
- 3 AI Foundry Hubs with 6 model deployments
- Redis Cache (semantic caching)
- Cosmos DB (message storage)
- Azure AI Search (vector search)
- 5 MCP servers in Container Apps

---

## Quick Commands

### Python Deployment
```python
from util.deploy_all import deploy_complete_infrastructure, DeploymentConfig

config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab'
)

outputs = deploy_complete_infrastructure(config)
outputs.to_env_file('master-lab.env')
```

### CLI Deployment
```bash
python -m util.deploy_all \
  --subscription-id xxx \
  --resource-group lab-master-lab \
  --output master-lab.env
```

### Lab Initialization
```python
from quick_start.shared_init import quick_init

config = quick_init()
```

---

## Comparison

| Metric | Original | Easy Deploy | Improvement |
|--------|----------|-------------|-------------|
| Cells | 152 | 34 | 78% reduction |
| File Size | 791 KB | 33 KB | 96% reduction |
| Code Lines | ~3,500 | ~400 | 89% reduction |

---

## Files

- `master-ai-gateway-easy-deploy.ipynb` - Start here (34 cells)
- `EASY_DEPLOY_README.md` - Full documentation
- `util/deploy_all.py` - Deployment utility
- `quick_start/shared_init.py` - Shared initialization

---

## Cost: ~$0.40/hour (~$10/day)

Delete when not needed:
```bash
az group delete --name lab-master-lab
```

---

**Get Started**: Open `master-ai-gateway-easy-deploy.ipynb` now!
