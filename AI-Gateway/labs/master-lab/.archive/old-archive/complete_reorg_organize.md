# Complete Reorganization Plan

## Source: master-ai-gateway-fix-MCP.ipynb (145 cells, 836KB)
## Target: master-ai-gateway-fix-MCP-clean.ipynb

## Critical Deployment Flow
```
1. Bootstrap (minimal env) → Cells 001-005
2. Deploy Azure Resources → Cells 006-010
3. GENERATE master-lab.env → Cell 011 (CRITICAL)
4. Load Complete Config → Cell 012
5. Configure MCP/Policies → Cells 013-030
6. Run Exercises → Cells 031+
```

## Cell Mapping Plan

### Part 0: Bootstrap & Initial Setup (NO master-lab.env required)
| New | Source | Purpose |
|-----|--------|---------|
| 001 | Create New | Environment Detection (Codespace vs Local) |
| 002 | Cells 1-2 | Minimal Config Loader (bootstrap.env only) |
| 003 | Cell 3 | Dependencies Installation |
| 004 | Cell 4 | Azure Authentication & Service Principal |
| 005 | Create New | Core Helper Classes (AzureOps wrapper) |

### Part 1: Deployment & Environment Generation  
| New | Source | Purpose |
|-----|--------|---------|
| 006 | Cell 14-20 | Resource Group & APIM Deployment |
| 007 | Cell 21-25 | OpenAI/AI Foundry Resources |
| 008 | Cell 26-28 | Storage, Redis, Cosmos |
| 009 | Cell 29-31 | Search Service, Additional Resources |
| 010 | Consolidate | Verify All Deployments Complete |
| 011 | **CREATE NEW** | **GENERATE master-lab.env from outputs** |
| 012 | **CREATE NEW** | **Reload Complete Configuration** |

### Part 2: MCP Server Configuration
| New | Source | Purpose |
|-----|--------|---------|
| 013 | Cell 78+ | Excel MCP Setup |
| 014 | Cell 79+ | Docs MCP Setup |
| 015 | Cell 80+ | GitHub MCP Setup |
| 016 | Cell 81+ | Weather API Setup |
| 017 | Cell 82+ | MCP Connection Tests |
| 018 | Cell 83+ | MCP Operations Tests |

### Part 3: Security & Policies
| New | Source | Purpose |
|-----|--------|---------|
| 019 | Cell 56-60 | JWT Token Configuration (Access Control Workshop) |
| 020 | Cell 61-65 | Token Validation Setup |
| 021 | Cell 66-70 | APIM Policy Fragments |
| 022 | Cell 71-75 | Semantic Cache Policies |
| 023 | Cell 76-77 | Content Safety Policies |

### Part 4: Framework Integration
| New | Source | Purpose |
|-----|--------|---------|
| 024 | Cell 133 | SK Plugin Function Calling |
| 025 | Cell 135 | SK Streaming Chat |
| 026 | Cell 137 | AutoGen Multi-Agent |
| 027 | Cell 139 | SK Custom Client |
| 028 | Cell 141 | SK Vector Search |
| 029 | Cell 143 | SK + AutoGen Hybrid |

### Part 5: Exercises & Validation
| New | Source | Purpose |
|-----|--------|---------|
| 030 | Cell 38-40 | Lab 01: Basic Chat |
| 031-050 | Consolidate remaining labs | All lab exercises |

## Key Variables to Track

### Bootstrap Phase (Cells 001-005):
- `subscription_id` (from bootstrap.env)
- `resource_group` (from bootstrap.env)
- `location` (from bootstrap.env)
- `az_ops` (AzureOps instance)
- `sp_credentials` (Service Principal)

### Deployment Phase (Cells 006-010):
- `deployment_outputs` (from Bicep)
- `apim_name`
- `openai_endpoint`
- `redis_connection`
- `cosmos_endpoint`

### Critical Cell 011:
- **Generates** `master-lab.env` file
- **Creates** all environment variables from deployment outputs

### Post-Config Phase (Cell 012+):
- `config` (WorkshopConfig object with ALL variables)
- `apim_gateway_url`
- `apim_api_key`
- `mcp` (MCP client instance)
- `excel_cache_key`, `cost_cache_key`

## Files to Create

1. `bootstrap.env.template` - Minimal config
2. `requirements.txt` - All dependencies  
3. `run_workshop.sh` - Linux launcher
4. `run_workshop.ps1` - Windows launcher
5. `workshop_modules.py` - Reusable code
6. `test_notebook.py` - Test suite with A-L methodology

## Success Criteria

✅ One-click deployment works
✅ Bootstrap → Deploy → Generate Env → Configure sequence works
✅ All cells pass A-L testing
✅ File size reduced by 30%+
✅ Works in Codespace and local
✅ No hard-coded values, all from env

## Next Steps

1. Create all supporting files
2. Build clean notebook with proper sequencing  
3. Run comprehensive tests
4. Document migration
