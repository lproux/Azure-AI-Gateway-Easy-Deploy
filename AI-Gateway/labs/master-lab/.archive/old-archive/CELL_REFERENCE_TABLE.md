# Cell Reference Table

Quick lookup for cell modifications during refactoring.

---

## Import Consolidation Reference

### Cells to Modify (Remove Listed Imports)

| Cell | Remove These Imports | Keep These Imports | Notes |
|------|---------------------|-------------------|-------|
| 41 | requests, DefaultAzureCredential | - | Simple removal |
| 42 | - | AzureOpenAI (local scope) | Keep as-is |
| 47 | requests, DefaultAzureCredential | - | Simple removal |
| 49 | Counter | - | Simple removal |
| 51 | matplotlib.pyplot, pandas, Counter, Patch | - | Remove all 4 |
| 59 | requests, os | - | Near Access Control but NOT in it |
| 76 | AuthenticationError | - | Simple removal |
| 78 | os, AuthenticationError | - | Simple removal |
| 82 | All Azure imports (4 total) | - | Remove all |
| 86 | os, sys, asyncio, json, pathlib | dotenv, MCP helpers | Keep MCP-specific |
| 88 | os, json, ast, traceback | WeatherMCP | Keep MCP helper |
| 89 | os, json, ast, traceback | GitHubMCP | Keep MCP helper |
| 90 | os, json, ast, traceback | OnCallMCP | Keep MCP helper |
| 92 | os, json, ast, traceback | SpotifyMCP | Keep MCP helper |
| 94 | os, json, ast, traceback | OnCallMCP | Keep MCP helper |
| 96 | os, json, ast, traceback | OnCallMCP | Keep MCP helper |
| 98 | json, ast, traceback | GitHubMCP | Keep MCP helper |
| 100 | os, socket, requests, json, time, base64, ast | GitHubMCP, textwrap | Keep specialized |
| 103 | json, ast | SpotifyMCP | Keep MCP helper |
| 105 | os, json, ast | SpotifyMCP | Keep MCP helper |
| 106 | os, json, ast | ProductCatalogMCP | Keep MCP helper |
| 109 | ast | - | Simple removal |
| 111 | redis.asyncio | - | Simple removal |
| 116 | os, subprocess, shutil, time, tempfile | - | Remove all 5 |
| 117 | os, requests, json | typing imports | Keep typing |
| 119 | os, base64, json, requests, matplotlib.pyplot | Optional, display, PIL | Keep specialized |
| 121 | os, re, json, subprocess, shutil, pathlib | - | Remove all 6 |
| 123 | os, requests, textwrap, json | typing imports | Keep typing |
| 136 | concurrent.futures | - | Simple removal |
| 144 | redis.asyncio | - | Simple removal |
| 156 | sys, subprocess, os | importlib, openai libs, MCP | Keep specialized |
| 174 | uuid | - | Simple removal |
| 176 | time | - | Simple removal |
| 182 | - | Cosmos imports | KEEP - specialized |
| 184 | - | Search imports | KEEP - specialized |
| 193 | json, requests, time, os | - | Remove all 4 |
| 195 | os, DefaultAzureCredential, get_bearer_token_provider | AzureOpenAI, NotFoundError | Keep OpenAI |
| 197 | pandas | - | Simple removal |
| 202 | os, pathlib | - | Simple removal |
| 204 | os, json, time, requests, Optional | - | Remove all 5 |
| 205 | base64 | math | Keep math if needed |
| 214 | json, asyncio, time | MCP imports | Keep MCP-specific |
| 215 | asyncio, json | httpx, MCP imports | Keep specialized |
| 217 | asyncio, nest_asyncio | agent_framework, MCP | Keep frameworks |
| 220 | asyncio | semantic_kernel, MCP | Keep frameworks |
| 228 | os, subprocess, shutil, time, tempfile | - | Remove all 5 |
| 229 | requests | - | Simple removal |
| 230 | requests | - | Simple removal |
| 235 | pandas, pathlib, json, traceback | - | Remove all 4 |
| 237 | - | json as _json | KEEP - specific alias |
| 238 | - | json as _json | KEEP - specific alias |
| 242 | os, pathlib | - | Simple removal |
| 243 | requests, json | AzureOpenAI | Keep OpenAI |
| 244 | - | AzureOpenAI | KEEP as-is |

---

## Access Control Protected Cells (DO NOT MODIFY)

| Cell | Type | Description | Policy Switch |
|------|------|-------------|---------------|
| 56 | markdown | Lab 06 header with warning | - |
| 57 | markdown | Lab 06 description | - |
| 58 | markdown | Workshop intro | - |
| 59 | code | Test: API Key only | NO |
| 60 | code | Test: JWT only | YES 🔒 |
| 61 | code | Test: API Key only (2) | NO |
| 62 | code | Test: Dual auth (Key+JWT) | YES 🔒 |
| 63 | code | Test: RBAC managed identity | NO |
| 64 | code | Test: Dual auth (2) | YES 🔒 |
| 65 | code | Test: JWT manual token | NO |
| 66 | code | Test: JWT auto refresh | YES 🔒 |
| 155 | markdown | Lab 06 extended tests | - |
| 170 | code | MCP OAuth test | Depends on 06 |

**Warning:** These cells contain critical policy-switching sequences. ANY modification could break authentication flows.

---

## Comment Removal Reference

### Obsolete Cell Reference Comments

| Cell | Line/Comment | Action |
|------|-------------|--------|
| 11 | "Load BICEP_DIR (set by Cell 3)" | DELETE |
| 46 | "DefaultAzureCredential already imported earlier (cell 22)" | DELETE |
| 46 | "Audience accepted by the APIM JWT-only policy (see policy cell 59)" | REPLACE with "Audience for APIM JWT policy" |
| 78 | "Current APIM policy may require BOTH api-key and a valid JWT (see dual auth ce..." | SIMPLIFY to "Current APIM policy may require dual auth" |
| 81 | "Require Cell 5 (Azure CLI Setup) to have been run" | REPLACE with "Requires: az_cli global variable" |
| 86 | "NOTE: MCP servers are already initialized in Cell 9 via MCPClient()" | DELETE or REPLACE with "NOTE: MCP servers initialized in MCP Setup section" |
| 100 | "Use globally initialized MCP client from Cell 9" | DELETE |
| 116 | "Require Cell 5 (Azure CLI Setup) to have been run" | REPLACE with "Requires: az_cli from Azure CLI Setup" |
| 116 | "az_cli already set by Cell 5" | DELETE |
| 116 | "API_ID will be auto-discovered by cell 9's apply_policies() function" | REPLACE with "API_ID auto-discovered by apply_policies()" |
| 116 | "Apply policy using helper function from cell 9" | DELETE |
| 121 | "Require Cell 5 (Azure CLI Setup) to have been run" | REPLACE with "Requires: az_cli from Azure CLI Setup" |
| 121 | "az_cli already set by Cell 5" | DELETE |
| 170 | "MCP OAuth authorization test with APIM (Cell 99)" | DELETE cell reference |
| 228 | "Require Cell 5 (Azure CLI Setup) to have been run" | REPLACE with "Requires: az_cli from Azure CLI Setup" |
| 228 | "az_cli already set by Cell 5" | DELETE |
| 228 | "API_ID will be auto-discovered by cell 9's apply_policies() function" | REPLACE with "API_ID auto-discovered by apply_policies()" |
| 228 | "Apply policy using helper function from cell 9" | DELETE |
| 241 | "Require Cell 5 (Azure CLI Setup) to have been run" | REPLACE with "Requires: az_cli from Azure CLI Setup" |

---

## Commented Code Review

| Cell | Lines | Review Action | Priority |
|------|-------|--------------|----------|
| 11 | 12 lines in 4 blocks | Check if deployment alternatives, remove if obsolete | P2 |
| 24 | 6 lines in 2 blocks | Check if config alternatives, remove if obsolete | P3 |
| 41 | 3 lines in 1 block | Likely debug code, remove | P1 |
| 55 | 4 lines in 1 block | Check if test variations, remove if obsolete | P3 |
| 109 | 4 lines in 1 block | Check if workflow alternatives, remove if obsolete | P2 |
| 214 | 3 lines in 1 block | Likely debug code, remove | P1 |
| 217 | 3 lines in 1 block | Likely debug code, remove | P1 |

---

## Function Deduplication Reference

### Functions to Consolidate into New "Deployment Utilities" Cell

| Function Name | Currently In | Action |
|---------------|-------------|--------|
| check_resource_group_exists() | Cells 20, 22 | Move to utilities, remove from both |
| compile_bicep() | Cells 3, 22 | Move to utilities, remove from both |
| check_deployment_exists() | Cells 3, 22 | Move to utilities, remove from both |
| deploy_template() | Cells 3, 22 | Move to utilities, remove from both |
| get_deployment_outputs() | Cells 3, 22 | Move to utilities, remove from both |
| az() | Cells 2, 29 | Keep in cell 2, remove from 29 |

### New Utilities Cell Content

Insert after cell 2:

```python
# Deployment Utilities Cell
from pathlib import Path
from azure.mgmt.resource import ResourceManagementClient
import subprocess
import json

# Functions: check_resource_group_exists, compile_bicep,
# check_deployment_exists, deploy_template, get_deployment_outputs

print("✓ Deployment utilities loaded")
```

---

## Section Header Fixes

### Duplicate Headers to Remove

| Cell | Current Header | Action |
|------|---------------|--------|
| 4 | Second "Section 1" marker | REMOVE (keep first at cell 0) |
| 69 | Second "Section 4" marker | REMOVE (keep first at cell 39) |
| 85 | Third "Section 1" marker | REMOVE |
| 112 | Second "Section 2" marker | REMOVE (keep first at cell 12) |
| 113 | Second "Section 3" marker | REMOVE (keep first at cell 25) |
| 118 | Third "Section 2" marker | REMOVE |

### Headers to Standardize

Format: `## Section X: Descriptive Name`

| Cell | Current | Standardize To |
|------|---------|---------------|
| 0 | Various formats | ## Section 1: Initialization & Setup |
| 12 | Various formats | ## Section 2: Azure Deployment |
| 25 | Various formats | ## Section 3: Configuration & Policies |
| 39 | Various formats | ## Section 4: Verification & Core Labs |
| ~85 | Various formats | ## Section 5: Advanced Labs & MCP |
| 212 | Current is good | ## Section 6: Agent Frameworks with MCP |
| 222 | Current is good | ## Section 7: OAuth & Authorization Patterns |

---

## Lab Organization Reference

### Foundation Labs (01-05)

| Lab | Cell Range | Can Modify | Notes |
|-----|-----------|------------|-------|
| Lab 01 | 71, 125-134 | YES | Zero to Production |
| Lab 02 | 72, 135-140 | YES | Load Balancing |
| Lab 04 | 73, 151 | YES | Token Metrics |
| Lab 05 | 74 | YES | Policy Foundations |

### Security Labs (06-07)

| Lab | Cell Range | Can Modify | Notes |
|-----|-----------|------------|-------|
| Lab 06 | 56-66, 155, 170 | NO 🔒 | Access Control - PROTECTED |
| Lab 07 | 75-76, 157 | YES | Content Safety |

### AI Feature Labs (08-10)

| Lab | Cell Range | Can Modify | Notes |
|-----|-----------|------------|-------|
| Lab 08 | 77-78, 159 | YES | Model Routing |
| Lab 09 | 79-81, 161 | YES | AI Foundry SDK |
| Lab 10 | 83-84 | YES | AI Foundry DeepSeek |

### MCP Labs (11-17)

| Lab | Cell Range | Can Modify | Notes |
|-----|-----------|------------|-------|
| Lab 11 | 87-91, 165 | YES | MCP Connection Methods |
| Lab 12 | 93, 167 | YES | Weather + AI |
| Lab 13 | 95, 169 | YES | OnCall Schedule |
| Lab 14 | 97 | YES | GitHub Repo Access |
| Lab 15 | 99, 124, 173 | YES | GitHub + AI Analysis |
| Lab 16 | 101 | YES | Spotify Search |
| Lab 17 | 104 | YES | Spotify + AI |

### Extended Labs (18-25)

| Lab | Cell Range | Can Modify | Notes |
|-----|-----------|------------|-------|
| Lab 18 | 177 | YES | Function Calling |
| Lab 19 | 141-143, 179 | YES | Semantic Caching |
| Lab 20 | 181 | YES | Message Storing |
| Lab 21 | 183 | YES | Vector Searching |
| Lab 22 | 145-147, 185 | YES | Image Generation |
| Lab 23 | 108 | YES | Multi-Server Orchestration |
| Lab 24 | 187 | YES | FinOps Framework |

---

## Priority Quick Reference

### Must Do First (Phase 1)
1. ✓ Remove obsolete comments (19 locations)
2. ✓ Fix section headers (6 duplicates)
3. ✓ Review commented code (7 cells)

### High Value (Phase 2)
4. ✓ Expand consolidated imports (cell 38)
5. ✓ Remove duplicate imports (40+ cells)

### Important (Phase 3)
6. ✓ Create deployment utilities cell
7. ✓ Remove duplicate functions (6 functions)

### Never Do
- ❌ Modify cells 56-66 (Lab 06)
- ❌ Modify cell 155 (Lab 06 tests)
- ❌ Modify cell 170 (MCP OAuth)
- ❌ Change execution order of policy switches
- ❌ Remove imports that are specialized/unique

---

## Testing Checklist by Section

After modifications, test these sections:

| Section | Key Tests | Critical Cells |
|---------|-----------|---------------|
| Section 1 | Imports load, env vars set | 38 (imports) |
| Section 2 | Deployment works | Utilities cell, 3, 22 |
| Section 3 | Policies apply | 30, 31, 37 |
| Section 4 | Lab 01-05 pass | 71-74 |
| Section 4 | Lab 06 works perfectly 🔒 | 56-66 |
| Section 4 | Lab 07-10 pass | 75-84 |
| Section 5 | MCP labs work | 87-109 |
| Section 5 | Extended labs work | 110-211 |
| Section 6 | Agent frameworks work | 212-221 |
| Section 7 | OAuth flows work | 222-247 |

---

## Cell Count Changes

| Phase | Added Cells | Removed Cells | Net Change |
|-------|-------------|---------------|------------|
| Phase 1 | 0 | 6 (duplicate headers) | -6 |
| Phase 2 | 0 | 0 (imports consolidated, not removed) | 0 |
| Phase 3 | 1 (utilities) | 6 (duplicate funcs) | -5 |
| **Total** | **1** | **12** | **-11** |

Final count: 248 → ~237 cells

---

**Quick Tip:** Print this file and check off cells as you modify them!

**Last Updated:** 2025-11-13
