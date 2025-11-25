# Creative Solutions for AI Foundry Deployment Issues

## Problem Summary
Deployment fails with circular reference or model availability errors.

---

## Solution 1: Simplified Stable Models (Currently Applied)

**What Changed**:
- Removed unsupported models: `gpt-4o-realtime-preview`, `DeepSeek-R1`, `Phi-4`, `FLUX-1.1-pro`
- Removed experimental `gpt-4.1` models (not GA yet)
- Focused on **production-ready models** available in UK South

**Model List (7 stable models)**:
```
foundry1 (UK South):
  ✓ gpt-4o-mini       - Main lightweight model
  ✓ gpt-4o            - Main flagship model
  ✓ gpt-4             - Legacy stable model
  ✓ dall-e-3          - Image generation
  ✓ text-embedding-3-small
  ✓ text-embedding-3-large
  ✓ text-embedding-ada-002

foundry2 (Sweden Central):
  ✓ gpt-4o-mini       - Failover model

foundry3 (West Europe):
  ✓ gpt-4o-mini       - Failover model
```

**Try This**: Re-run Cell 17 now - should deploy successfully in ~15 minutes

---

## Solution 2: Deploy Foundries Separately (If Solution 1 Fails)

Split Step 2 into 3 sub-steps:

### Create: `deploy-02a-foundry-hubs.bicep`
Deploy just the 3 AI Foundry hubs + projects (no models)

### Create: `deploy-02b-foundry-models.bicep`
Deploy models one hub at a time using Python loop with try-catch per model

### Create: `deploy-02c-apim-api.bicep`
Configure APIM Inference API

**Benefit**: If one model fails, others still deploy

---

## Solution 3: Python Direct Deployment (No Bicep)

Use Azure Python SDK directly to deploy models with error handling:

```python
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

models = [
    {'name': 'gpt-4o-mini', 'publisher': 'OpenAI', ...},
    {'name': 'gpt-4o', 'publisher': 'OpenAI', ...},
    # ...
]

for model in models:
    try:
        print(f'[*] Deploying {model["name"]}...')
        deployment = client.deployments.begin_create_or_update(
            resource_group,
            account_name,
            model['name'],
            {
                'sku': {'name': model['sku'], 'capacity': model['capacity']},
                'properties': {'model': model}
            }
        ).result()
        print(f'[OK] {model["name"]} deployed')
    except Exception as e:
        print(f'[SKIP] {model["name"]} failed: {e}')
        continue  # Skip failed models, continue with rest
```

**Benefit**: Resilient to individual model failures

---

## Solution 4: Use Azure CLI Deployment Mode (Incremental)

Set deployment mode to `Incremental` and use `--what-if` first:

```bash
az deployment group what-if \
  --resource-group lab-master-lab \
  --template-file deploy-02-ai-foundry.json \
  --parameters params-02-ai-foundry.json
```

Check what will be deployed before committing.

---

## Solution 5: Deploy Only Core Models First

Start with **absolute minimum**:

```bicep
var foundry1Models = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
]
```

Then add models incrementally via Azure Portal or separate deployments.

---

## Recommended Approach

1. **Try Solution 1** (current) - Re-run Cell 17
2. **If still fails** → Use Solution 3 (Python direct with error handling)
3. **For production** → Keep Solution 1's stable model list

---

## Model Availability by Region

| Model | UK South | Sweden Central | West Europe |
|-------|----------|----------------|-------------|
| gpt-4o-mini | ✓ | ✓ | ✓ |
| gpt-4o | ✓ | ✓ | ✓ |
| gpt-4 | ✓ | ✓ | ✓ |
| dall-e-3 | ✓ | ? | ? |
| text-embedding-3-* | ✓ | ✓ | ✓ |
| gpt-4o-realtime-preview | ✗ | ? | ? |
| DeepSeek-R1 | ✗ | ✗ | ✗ |
| Phi-4 | ✗ | ? | ? |
| FLUX-1.1-pro | ✗ | ✗ | ✗ |

✓ = Available
✗ = Not Available
? = Unknown (not tested)

---

## Next Steps

Re-run **Cell 17** with the simplified stable model configuration. If it fails, let me know the error and I'll implement Solution 3 (Python resilient deployment).
