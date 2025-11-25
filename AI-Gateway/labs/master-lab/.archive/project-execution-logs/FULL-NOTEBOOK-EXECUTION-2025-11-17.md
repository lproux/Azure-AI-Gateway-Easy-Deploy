# Full Notebook Execution Report - 2025-11-17

**Notebook**: master-ai-gateway-fix-MCP.ipynb
**Analysis Date**: 2025-11-17T01:27:05.889909
**Total Cells**: 157
**Analysis Type**: Static Analysis (Pre-execution)

---

## Executive Summary

- **Total Issues Found**: 193
- **Critical Issues**: 30
- **High Priority**: 125
- **Medium Priority**: 25
- **Low Priority**: 13

## Critical Issues Requiring Immediate Attention

### Cell 8: (-1.5) Unified az() Helper & Login Check
- **Issue**: Environment variable required: AZURE_CLIENT_ID
- **Type**: configuration
- **Requirements**: AZURE_CLIENT_ID must be set
- **Resolution Options**:
  A) Set AZURE_CLIENT_ID in .env file
  B) Export AZURE_CLIENT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 8: (-1.5) Unified az() Helper & Login Check
- **Issue**: Environment variable required: AZURE_CLIENT_SECRET
- **Type**: configuration
- **Requirements**: AZURE_CLIENT_SECRET must be set
- **Resolution Options**:
  A) Set AZURE_CLIENT_SECRET in .env file
  B) Export AZURE_CLIENT_SECRET=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 8: (-1.5) Unified az() Helper & Login Check
- **Issue**: Environment variable required: AZURE_TENANT_ID
- **Type**: configuration
- **Requirements**: AZURE_TENANT_ID must be set
- **Resolution Options**:
  A) Set AZURE_TENANT_ID in .env file
  B) Export AZURE_TENANT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 10: (-1.7) Unified Policy Application with Auto-Discovery
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 12: (-1.9) Unified AzureOps Wrapper (Enhanced SDK Strategy)
- **Issue**: Environment variable required: AZURE_CLIENT_ID
- **Type**: configuration
- **Requirements**: AZURE_CLIENT_ID must be set
- **Resolution Options**:
  A) Set AZURE_CLIENT_ID in .env file
  B) Export AZURE_CLIENT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 12: (-1.9) Unified AzureOps Wrapper (Enhanced SDK Strategy)
- **Issue**: Environment variable required: AZURE_CLIENT_SECRET
- **Type**: configuration
- **Requirements**: AZURE_CLIENT_SECRET must be set
- **Resolution Options**:
  A) Set AZURE_CLIENT_SECRET in .env file
  B) Export AZURE_CLIENT_SECRET=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 12: (-1.9) Unified AzureOps Wrapper (Enhanced SDK Strategy)
- **Issue**: Environment variable required: AZURE_TENANT_ID
- **Type**: configuration
- **Requirements**: AZURE_TENANT_ID must be set
- **Resolution Options**:
  A) Set AZURE_TENANT_ID in .env file
  B) Export AZURE_TENANT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 12: (-1.9) Unified AzureOps Wrapper (Enhanced SDK Strategy)
- **Issue**: Environment variable required: AZURE_SUBSCRIPTION_ID
- **Type**: configuration
- **Requirements**: AZURE_SUBSCRIPTION_ID must be set
- **Resolution Options**:
  A) Set AZURE_SUBSCRIPTION_ID in .env file
  B) Export AZURE_SUBSCRIPTION_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 17: ============================================================================
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 17: ============================================================================
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 22: APIM policy apply helper (patched Azure CLI resolution with autodiscovery)
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 22: APIM policy apply helper (patched Azure CLI resolution with autodiscovery)
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 27: import json
- **Issue**: Environment variable required: AZURE_CLIENT_ID
- **Type**: configuration
- **Requirements**: AZURE_CLIENT_ID must be set
- **Resolution Options**:
  A) Set AZURE_CLIENT_ID in .env file
  B) Export AZURE_CLIENT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 27: import json
- **Issue**: Environment variable required: AZURE_TENANT_ID
- **Type**: configuration
- **Requirements**: AZURE_TENANT_ID must be set
- **Resolution Options**:
  A) Set AZURE_TENANT_ID in .env file
  B) Export AZURE_TENANT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 27: import json
- **Issue**: Environment variable required: AZURE_CLIENT_SECRET
- **Type**: configuration
- **Requirements**: AZURE_CLIENT_SECRET must be set
- **Resolution Options**:
  A) Set AZURE_CLIENT_SECRET in .env file
  B) Export AZURE_CLIENT_SECRET=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 37: ============================================================================
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 37: ============================================================================
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 43: ============================================================================
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 43: ============================================================================
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 55: import requests, os, subprocess, time
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 55: import requests, os, subprocess, time
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 55: import requests, os, subprocess, time
- **Issue**: Environment variable required: AZURE_TENANT_ID
- **Type**: configuration
- **Requirements**: AZURE_TENANT_ID must be set
- **Resolution Options**:
  A) Set AZURE_TENANT_ID in .env file
  B) Export AZURE_TENANT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 56: import requests, os, subprocess, time
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 56: import requests, os, subprocess, time
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 57: import requests, os, subprocess, time
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 57: import requests, os, subprocess, time
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 57: import requests, os, subprocess, time
- **Issue**: Environment variable required: AZURE_TENANT_ID
- **Type**: configuration
- **Requirements**: AZURE_TENANT_ID must be set
- **Resolution Options**:
  A) Set AZURE_TENANT_ID in .env file
  B) Export AZURE_TENANT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 58: import requests, os, time
- **Issue**: Environment variable required: APIM_SERVICE_NAME
- **Type**: configuration
- **Requirements**: APIM_SERVICE_NAME must be set
- **Resolution Options**:
  A) Set APIM_SERVICE_NAME in .env file
  B) Export APIM_SERVICE_NAME=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 58: import requests, os, time
- **Issue**: Environment variable required: RESOURCE_GROUP
- **Type**: configuration
- **Requirements**: RESOURCE_GROUP must be set
- **Resolution Options**:
  A) Set RESOURCE_GROUP in .env file
  B) Export RESOURCE_GROUP=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

### Cell 146: import os, pathlib
- **Issue**: Environment variable required: AZURE_TENANT_ID
- **Type**: configuration
- **Requirements**: AZURE_TENANT_ID must be set
- **Resolution Options**:
  A) Set AZURE_TENANT_ID in .env file
  B) Export AZURE_TENANT_ID=<value> in terminal
  C) Add to Azure Key Vault for production
  D) Provide default value in code with getenv()

---

# Detailed Cell-by-Cell Analysis

## Cell 1: Master AI Gateway Notebook

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 2: (-1.0) Section -1: Consolidated Provisioning & Initialization

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.0) Section -1: Consolidated Provisioning & Initialization
"""
Run these cells (-1.x) in order before using legacy sections.
Order:
  (-1.1) Env Loader
  (-1.2) Dependencies Install
  (-1.3) Azure CLI & Service Principal
  (-1.4) Endpoint Normalizer
  (upcoming) (-1.5) Deployment Helpers
  (upcoming) (-1.6) Unified Deployment Orchestrator
  (upcoming) (-1.7) Unified Policy Application
  (upcoming) (-1.8) Unified MCP Initialization
Legacy cells retained below for reference.
"""
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 3: (-1.1) Consolidated Environment Loader (Enhanced)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.1) Consolidated Environment Loader (Enhanced)
"""
Single source of truth for environment configuration.
Enhancements:
- Auto-creates master-lab.env if missing
- Loads and validates environment variables
- Derives APIM_SERVICE from APIM_GATEWAY_URL if missing
- Sets BICEP_DIR for deployment files
- Provides NotebookConfig dataclass for structured access
"""
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import re, os

ENV_FILE = Path('master-lab.env')...
```

**Issues Found**:
- Environment variable required: APIM_SERVICE
- Environment variable required: API_ID
- Environment variable required: BICEP_DIR

**Severity**: HIGH

**Potential Resolutions**:
A) Set APIM_SERVICE in .env file
B) Export APIM_SERVICE=<value> in terminal
C) Add to Azure Key Vault for production
A) Set API_ID in .env file
B) Export API_ID=<value> in terminal
C) Add to Azure Key Vault for production
A) Set BICEP_DIR in .env file
B) Export BICEP_DIR=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 4: (-1.2) Dependencies Install (Consolidated)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.2) Dependencies Install (Consolidated)
import sys, subprocess, pathlib, shlex
REQ_FILE = pathlib.Path('requirements.txt')
if REQ_FILE.exists():
    cmd=[sys.executable,'-m','pip','install','-r',str(REQ_FILE)]
    print('[deps]',' '.join(shlex.quote(c) for c in cmd))
    r=subprocess.run(cmd,capture_output=True,text=True)
    print(r.stdout[:800])
    if r.returncode==0: print('[deps] ✅ complete')
    else: print('[deps] ⚠️ pip exit',r.returncode,'stderr:',r.stderr[:200])
else:
    print('[...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 5: (-1.3) Azure CLI & Service Principal Setup (Consolidated v2)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.3) Azure CLI & Service Principal Setup (Consolidated v2)
import json, os, shutil, subprocess, sys, time
from pathlib import Path
AZ_CREDS_FILE=Path('.azure-credentials.env')

OS_RELEASE = {}
try:
    if Path('/etc/os-release').exists():
        for line in Path('/etc/os-release').read_text().splitlines():
            if '=' in line:
                k,v=line.split('=',1)
                OS_RELEASE[k]=v.strip().strip('"')
except Exception:
    pass

ARCH_LINUX = OS_RELEASE.get('ID') == 'arch...
```

**Issues Found**:
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: AZ_CLI
- Environment variable required: CODESPACES
- Environment variable required: AZURE_CLI_PATH
- Environment variable required: CODESPACE_NAME
- Potentially long-running operation

**Severity**: HIGH

**Potential Resolutions**:
A) Set SUBSCRIPTION_ID in .env file
B) Export SUBSCRIPTION_ID=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZ_CLI in .env file
B) Export AZ_CLI=<value> in terminal
C) Add to Azure Key Vault for production
A) Set CODESPACES in .env file
B) Export CODESPACES=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_CLI_PATH in .env file
B) Export AZURE_CLI_PATH=<value> in terminal
C) Add to Azure Key Vault for production
A) Set CODESPACE_NAME in .env file
B) Export CODESPACE_NAME=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 6: (-1.3b) MSAL Cache Flush Helper

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.3b) MSAL Cache Flush Helper
"""Helper function to flush MSAL cache when Azure CLI encounters MSAL corruption.

The MSAL error 'Can't get attribute NormalizedResponse' indicates cache corruption.
This helper safely clears the MSAL cache and retries Azure CLI operations.
"""

import os
import shutil
import subprocess
from pathlib import Path

def flush_msal_cache():
    """Flush MSAL cache directories to resolve cache corruption.
    
    Returns:
        bool: True if cache was flushed succ...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 7: (-1.4) Endpoint Normalizer & Derived Variables

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.4) Endpoint Normalizer & Derived Variables
"""
Derives OPENAI_ENDPOINT and related derived variables if missing.
Logic priority:
1. Use explicit OPENAI_ENDPOINT if set (leave unchanged).
2. Else if APIM_GATEWAY_URL + INFERENCE_API_PATH present -> compose.
3. Else attempt Foundry style endpoints (AZURE_OPENAI_ENDPOINT, AI_FOUNDRY_ENDPOINT).
Persist back to master-lab.env if value was newly derived.
"""
from pathlib import Path
import os, re
env_path=Path('master-lab.env')
text=env_path.read...
```

**Issues Found**:
- Environment variable required: OPENAI_ENDPOINT

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_ENDPOINT in .env file
B) Export OPENAI_ENDPOINT=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 8: (-1.5) Unified az() Helper & Login Check

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.5) Unified az() Helper & Login Check
"""Provides a cached az CLI executor with:
- Path reuse via AZ_CLI env (expects (-1.3) run first)
- Automatic login prompt if account show fails and no service principal creds
- Timeout controls & JSON parsing convenience
Usage:
    ok, data = az('account show', json_out=True)
    ok, text = az('apim list --resource-group X')
"""
import os, subprocess, json, shlex
from pathlib import Path
AZ_CLI = os.environ.get('AZ_CLI') or os.environ.get('AZURE_CLI_PA...
```

**Issues Found**:
- Environment variable required: AZURE_CLIENT_ID
- Environment variable required: AZURE_CLIENT_SECRET
- Environment variable required: AZ_CLI
- Environment variable required: AZURE_CLI_PATH
- Environment variable required: AZURE_TENANT_ID

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set AZURE_CLIENT_ID in .env file
B) Export AZURE_CLIENT_ID=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_CLIENT_SECRET in .env file
B) Export AZURE_CLIENT_SECRET=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_TENANT_ID in .env file
B) Export AZURE_TENANT_ID=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 9: (-1.6) Deployment Helpers (Consolidated)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.6) Deployment Helpers (Consolidated)
"""Utilities for ARM/Bicep deployments via az CLI.
Depends on az() from (-1.5).
Functions:
  compile_bicep(bicep_path) -> str json_template_path
  deploy_template(rg, name, template_file, params: dict) -> (ok, result_json)
  get_deployment_outputs(rg, name) -> dict outputs or {}
  ensure_deployment(rg, name, template, params, skip_if_exists=True)
"""
import os, json, tempfile, pathlib, shlex
from pathlib import Path

def compile_bicep(bicep_path:str):
 ...
```

**Issues Found**:
- OpenAI API import: openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 10: (-1.7) Unified Policy Application with Auto-Discovery

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.7) Unified Policy Application with Auto-Discovery

"""Applies one or more API Management policies to the target API using Azure REST API.

Provide policies as a list of (policy_name, policy_xml_string).

Automatically discovers the API ID if not set in environment.
Creates policy payloads and invokes az rest to apply them.

Requires ENV values: RESOURCE_GROUP, APIM_SERVICE (service name)
Optional: API_ID (will be auto-discovered if not provided)

Note: Uses Azure REST API because 'az apim ...
```

**Issues Found**:
- Environment variable required: APIM_SERVICE
- Environment variable required: API_ID
- Environment variable required: RESOURCE_GROUP
- File I/O operations detected

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 11: (-1.8) Unified MCP Initialization (Updated for 4 Data Sources)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.8) Unified MCP Initialization (Updated for 4 Data Sources)
"""Initializes MCP servers and APIM-routed APIs.

Available Data Sources:
  1. Excel MCP (direct) - Analytics, charts, data processing
  2. Docs MCP (direct) - Document search, retrieval
  3. GitHub API (APIM) - Code repos, search
  4. Weather API (APIM) - Real-time weather data

Reads configuration from .mcp-servers-config file.
"""
import sys
sys.path.append('.')

from notebook_mcp_helpers import MCPClient, MCPError

# Check if a...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 12: (-1.9) Unified AzureOps Wrapper (Enhanced SDK Strategy)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# (-1.9) Unified AzureOps Wrapper (Enhanced SDK Strategy)
"""High-level Azure operations wrapper consolidating:
- CLI resolution & version
- Service principal / interactive login fallback
- Generic az() invocation (JSON/text)
- Resource group ensure (CLI or SDK)
- Bicep compile (CLI) + group deployment (CLI or SDK)
- AI Foundry model deployments (SDK)
- APIM policy fragments + API policy apply (with rollback)
- Deployment outputs retrieval & simplification
- MCP server health probing

Strategy:
...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Azure SDK import: azure.mgmt.resource
- Azure SDK import: azure.mgmt.cognitiveservices
- Azure SDK import: azure.mgmt.cognitiveservices.models
- Environment variable required: AZURE_CLIENT_ID
- Environment variable required: VIRTUAL_ENV
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: AZURE_CLIENT_SECRET
- Environment variable required: AZ_CLI
- Environment variable required: AZURE_CLI_PATH
- Environment variable required: AZ_OPS_STRATEGY
- Environment variable required: AZURE_TENANT_ID
- Environment variable required: AZURE_SUBSCRIPTION_ID
- Azure Management API usage
- Potentially long-running operation

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set AZURE_CLIENT_ID in .env file
B) Export AZURE_CLIENT_ID=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_CLIENT_SECRET in .env file
B) Export AZURE_CLIENT_SECRET=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_TENANT_ID in .env file
B) Export AZURE_TENANT_ID=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_SUBSCRIPTION_ID in .env file
B) Export AZURE_SUBSCRIPTION_ID=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 13: Section 0 : Consolidated Provisioning & Initialization

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 14: === Unified Environment Loader & Load Balancing Overview ===

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# === Unified Environment Loader & Load Balancing Overview ===
"""
This cell provides a single source of truth for configuration:
- Auto-creates `master-lab.env` if missing (non-secret template placeholders).
- Loads key=value pairs (duplicates allowed) and merges with current process env.
- Masks sensitive values when displaying (KEY, SECRET, TOKEN, PASSWORD, API_KEY substrings).
- Ensures `.gitignore` patterns include env files (both global and lab-specific).
- Displays load balancing pools an...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 15: Unified Dependencies Install (replaces older dependency cell)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Unified Dependencies Install (replaces older dependency cell)
import os, sys, subprocess, pathlib, shlex
LAB_ROOT = pathlib.Path(r"c:\Users\lproux\OneDrive - Microsoft\bkp\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab")
REQ_FILE = LAB_ROOT / "requirements.txt"
if REQ_FILE.exists():
    print(f"[deps] Installing from {REQ_FILE} (idempotent)")
    cmd = [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)]
    print("[deps] Command:", " ".join(shlex.qu...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 16: ✅ Optimized Execution Order (Cells 1–25 Refactor)

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 17: ============================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ============================================================================
# LAB 01: Semantic Caching with Azure Redis
# ============================================================================

print("\n" + "="*80)
print("LAB 01: Semantic Caching Configuration")
print("="*80 + "\n")

import requests
from azure.identity import DefaultAzureCredential

# Configuration
backend_id = "inference-backend-pool"
embeddings_backend_id = "foundry1"
subscription_id = os.environ.get('SUBSCRIPTION_ID'...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: RESOURCE_GROUP
- Environment variable required: APIM_API_ID
- HTTP/API requests detected

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 18: DEPLOY AND CONFIG

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 19: Environment Standardization

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 20: Install Required Packages

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 21: <a id='init'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 22: APIM policy apply helper (patched Azure CLI resolution with autodiscovery)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# APIM policy apply helper (patched Azure CLI resolution with autodiscovery)
import shutil, subprocess, os, sys, textwrap, tempfile
from pathlib import Path

AZ_CANDIDATES = [
    shutil.which("az"),
    str(Path(sys.prefix) / "bin" / "az"),
]

AZ_CANDIDATES += [c for c in [os.getenv("AZURE_CLI_PATH"), os.getenv("AZ_PATH")] if c]
az_cli = next((c for c in AZ_CANDIDATES if c and Path(c).exists()), None)

if not az_cli:
    raise SystemExit("[FATAL] Azure CLI 'az' not found. Install it before cont...
```

**Issues Found**:
- Environment variable required: RESOURCE_GROUP
- Environment variable required: AZ_PATH
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: APIM_API_ID
- Environment variable required: AZURE_CLI_PATH
- File I/O operations detected

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 23: Load Environment Variables from Deployment Output

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 24: Master Lab Configuration

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 25: Master Lab Configuration

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Master Lab Configuration

# IMPORTANT: Set your Azure subscription ID
# Get this from: Azure Portal > Subscriptions > Copy Subscription ID
subscription_id = 'd334f2cd-3efd-494e-9fd3-2470b1a13e4c'  # Replace with your subscription ID

deployment_name_prefix = 'master-lab'
resource_group_name = 'lab-master-lab'
location = 'uksouth'

# Deployment names for each step
deployment_step1 = f'{deployment_name_prefix}-01-core'
deployment_step2 = f'{deployment_name_prefix}-02-ai-foundry'
deployment_step3...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 26: Deployment Helper Functions

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 27: import json

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import json
import time
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential, AzureCliCredential

print('[*] Initializing Azure authentication...')
print()

# Try to load Service Principal credentials from .azure-credentials.env
credentials_file = '.azure-credentials.env'
credential = None

if os.path.exists(credentials_file):
    print(f'[*] Found {credentials_fi...
```

**Issues Found**:
- Azure SDK import: azure.mgmt.resource
- Azure SDK import: azure.identity
- Environment variable required: AZURE_CLIENT_ID
- Environment variable required: AZURE_TENANT_ID
- Environment variable required: AZURE_CLIENT_SECRET
- Azure Management API usage
- File I/O operations detected
- Potentially long-running operation

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set AZURE_CLIENT_ID in .env file
B) Export AZURE_CLIENT_ID=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_TENANT_ID in .env file
B) Export AZURE_TENANT_ID=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_CLIENT_SECRET in .env file
B) Export AZURE_CLIENT_SECRET=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 28: Main Deployment - All 4 Steps

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 29: print('=' * 70)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
print('=' * 70)
# Load BICEP_DIR (set by Cell 3)
BICEP_DIR = Path(os.getenv('BICEP_DIR', 'archive/scripts'))
if not BICEP_DIR.exists():
    print(f"[deploy] ⚠️  BICEP_DIR not found: {BICEP_DIR}")
    print(f"[deploy] Looking in current directory instead")
    BICEP_DIR = Path(".")

print('MASTER LAB DEPLOYMENT - 4 STEPS (RESILIENT)')
print('=' * 70)
print()

total_start = time.time()

# Ensure resource group exists
print('[*] Step 0: Ensuring resource group exists...')
if not check_resource_grou...
```

**Issues Found**:
- Azure SDK import: azure.mgmt.cognitiveservices
- Azure SDK import: azure.mgmt.cognitiveservices.models
- Environment variable required: BICEP_DIR
- Azure Management API usage
- File I/O operations detected

**Severity**: HIGH

**Potential Resolutions**:
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable
A) Set BICEP_DIR in .env file
B) Export BICEP_DIR=<value> in terminal
C) Add to Azure Key Vault for production
A) Ensure Azure CLI is logged in: az login
B) Verify subscription access: az account show
C) Check RBAC permissions for resources

**Recommended**: Option A (most common solution)

---

## Cell 30: Generate .env File

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 31: import os

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import os
from datetime import datetime

print('[*] Generating master-lab.env...')

# Ensure step2_outputs, step3_outputs and step4_outputs exist (safe fallback to empty dicts)
try:
    step2_outputs
except NameError:
    try:
        step2_outputs = get_deployment_outputs(resource_group_name, deployment_step2c)
    except Exception:
        step2_outputs = {}

try:
    step3_outputs
except NameError:
    try:
        step3_outputs = get_deployment_outputs(resource_group_name, deployment_step3)
...
```

**Issues Found**:
- Environment variable required: APIM_API_ID
- File I/O operations detected

**Severity**: HIGH

**Potential Resolutions**:
A) Set APIM_API_ID in .env file
B) Export APIM_API_ID=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 32: APIM Variable Definitions (for cells that use lowercase names)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# APIM Variable Definitions (for cells that use lowercase names)
# These map environment variables to lowercase snake_case for backwards compatibility

import os

# APIM Gateway URLs
apim_gateway_url = os.environ.get('APIM_GATEWAY_URL', '')
apim_resource_gateway_url = apim_gateway_url  # Same as gateway URL
apim_api_key = os.environ.get('APIM_API_KEY', '')

# Azure OpenAI API Configuration
inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')
inference_api_version = '2024-08-01-...
```

**Issues Found**:
- Environment variable required: APIM_GATEWAY_URL
- Environment variable required: APIM_API_KEY
- Environment variable required: INFERENCE_API_PATH

**Severity**: HIGH

**Potential Resolutions**:
A) Set APIM_GATEWAY_URL in .env file
B) Export APIM_GATEWAY_URL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_API_KEY in .env file
B) Export APIM_API_KEY=<value> in terminal
C) Add to Azure Key Vault for production
A) Set INFERENCE_API_PATH in .env file
B) Export INFERENCE_API_PATH=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 33: Master AI Gateway Lab - 25 Labs Consolidated

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 34: The following labs (01-10) cover essential Azure API Managem...

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 35: <a id='lab01'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 36: Test 1: Basic Chat Completion

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 37: ============================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ============================================================================
# LAB 02: Token Metrics (OpenAI API Monitoring)
# ============================================================================

print("\n" + "="*80)
print("LAB 02: Token Metrics Configuration")
print("="*80 + "\n")

import requests
from azure.identity import DefaultAzureCredential

# Configuration
backend_id = "inference-backend-pool"
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get(...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: RESOURCE_GROUP
- Environment variable required: APIM_API_ID
- HTTP/API requests detected

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 38: Lab 01: Test 1 - Basic Chat Completion

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 39: Test 2: Streaming Response

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 40: Lab 01: Test 2 - Streaming Response (robust with fallback)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Lab 01: Test 2 - Streaming Response (robust with fallback)

print('[*] Testing streaming...')

prompt_messages = [
    {'role': 'system', 'content': 'You are a helpful assistant. Stream numbers.'},
    {'role': 'user', 'content': 'Count from 1 to 5'}
]

def stream_completion():
    return client.chat.completions.create(
        model='gpt-4o-mini',
        messages=prompt_messages,
        max_tokens=32,
        temperature=0.2,
        stream=True
    )

def non_stream_completion():
    retur...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 41: Test 3: Multiple Requests

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 42: <a id='lab02'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 43: ============================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ============================================================================
# LAB 03: Load Balancing with Retry Logic
# ============================================================================

print("\n" + "="*80)
print("LAB 03: Load Balancing Configuration")
print("="*80 + "\n")

import requests
from azure.identity import DefaultAzureCredential

# Configuration
backend_id = "inference-backend-pool"
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESO...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: RESOURCE_GROUP
- Environment variable required: APIM_API_ID
- HTTP/API requests detected

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 44: Test 1: Load Distribution

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 45: print('Testing load balancing across 3 regions...')

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
print('Testing load balancing across 3 regions...')
responses = []
regions = []  # Track which region processed each request
backend_ids = []  # Track which backend served each request

# Resolve required variables (avoid NameError)
apim_gateway_url = (
    (step1_outputs.get('apimGatewayUrl') if isinstance(step1_outputs, dict) else None) or
    os.environ.get('APIM_GATEWAY_URL')
)
inference_api_path = (
    (step2_outputs.get('inferenceAPIPath') if isinstance(step2_outputs, dict) else None) or
...
```

**Issues Found**:
- Environment variable required: OPENAI_API_VERSION
- Environment variable required: APIM_GATEWAY_URL
- Environment variable required: INFERENCE_API_PATH
- Environment variable required: APIM_API_KEY
- HTTP/API requests detected
- Some collections imports moved to collections.abc
- Potentially long-running operation

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_VERSION in .env file
B) Export OPENAI_API_VERSION=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_GATEWAY_URL in .env file
B) Export APIM_GATEWAY_URL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set INFERENCE_API_PATH in .env file
B) Export INFERENCE_API_PATH=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_API_KEY in .env file
B) Export APIM_API_KEY=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 46: Test 2: Visualize Response Times

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 47: import matplotlib.pyplot as plt

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Create DataFrame with response times and regions
df = pd.DataFrame({
    'Request': range(1, len(responses)+1),
    'Time (s)': responses,
    'Region': regions
})

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Response times with region colors
region_colors = {'Unknown': 'gray'}
unique_regions = [r for r in set(regions) if r != 'Unknown']
color_palette = ['...
```

**Issues Found**:
- Some collections imports moved to collections.abc

**Severity**: LOW

**Potential Resolutions**:
A) Update to modern API usage
B) Check library documentation for migration guide
C) Pin library version if update not feasible

**Recommended**: Option A (most common solution)

---

## Cell 48: Implement comprehensive observability using Azure Log Analyt...

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 49: <a id='lab04'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 50: Lab 04 token usage aggregation (auto-initialize client if missing)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Lab 04 token usage aggregation (auto-initialize client if missing)
total_tokens = 0

# Resolve required endpoint pieces from previously loaded deployment outputs / env
apim_gateway_url = (
    (step1_outputs.get('apimGatewayUrl') if isinstance(step1_outputs, dict) else None)
    or os.environ.get('APIM_GATEWAY_URL')
)
inference_api_path = (
    (step2_outputs.get('inferenceAPIPath') if isinstance(step2_outputs, dict) else None)
    or os.environ.get('INFERENCE_API_PATH', 'inference')
)
apim_ap...
```

**Issues Found**:
- OpenAI API import: openai
- Environment variable required: OPENAI_API_VERSION
- Environment variable required: APIM_GATEWAY_URL
- Environment variable required: INFERENCE_API_PATH
- Environment variable required: APIM_API_KEY

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity
A) Set OPENAI_API_VERSION in .env file
B) Export OPENAI_API_VERSION=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_GATEWAY_URL in .env file
B) Export APIM_GATEWAY_URL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set INFERENCE_API_PATH in .env file
B) Export INFERENCE_API_PATH=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_API_KEY in .env file
B) Export APIM_API_KEY=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 51: <a id='lab05'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 52: ============================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ============================================================================
# OPTIONAL DIAGNOSTIC CELL - Can be skipped
# ============================================================================
# This cell is for troubleshooting 500 errors.
# If everything is working, you can skip this cell.
# ============================================================================

SKIP_DIAGNOSTIC = True  # Set to False to run diagnostic

if SKIP_DIAGNOSTIC:
    print("\n" + "="*80)
    print("DIAGN...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 53: <a id='lab06'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 54: Access Control Workshop

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 55: import requests, os, subprocess, time

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import requests, os, subprocess, time
from azure.identity import DefaultAzureCredential

print("" + "="*80)
print("📝 APPLY: JWT Only Policy (disable subscriptionRequired)")
print("="*80 + "")

# Get management token
credential = DefaultAzureCredential()
mgmt_token = credential.get_token("https://management.azure.com/.default")

# Configuration
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESOURCE_GROUP')
apim_service_name = os.environ.get('APIM_SERVICE_NAM...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Environment variable required: RESOURCE_GROUP
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: APIM_API_ID
- Environment variable required: AZ_CLI
- Environment variable required: AZURE_TENANT_ID
- HTTP/API requests detected
- Potentially long-running operation

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_TENANT_ID in .env file
B) Export AZURE_TENANT_ID=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 56: import requests, os, subprocess, time

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import requests, os, subprocess, time
from azure.identity import DefaultAzureCredential

# Configuration
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESOURCE_GROUP')
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
api_id = os.environ.get('APIM_API_ID', 'inference-api')

# Get management token and tenant ID
credential = DefaultAzureCredential()
mgmt_token = credential.get_token("https://management.azure.com/.default")

az_cli = os.environ.get('AZ_C...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Environment variable required: RESOURCE_GROUP
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: APIM_API_ID
- Environment variable required: AZ_CLI
- HTTP/API requests detected
- Potentially long-running operation

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 57: import requests, os, subprocess, time

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import requests, os, subprocess, time
from azure.identity import DefaultAzureCredential

print("" + "="*80)
print("📝 APPLY: Dual Auth (JWT + API Key)")
print("="*80 + "")

# Get management token
credential = DefaultAzureCredential()
mgmt_token = credential.get_token("https://management.azure.com/.default")

# Configuration
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESOURCE_GROUP')
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
api_id = os.envir...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Environment variable required: RESOURCE_GROUP
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: APIM_API_ID
- Environment variable required: AZ_CLI
- Environment variable required: AZURE_TENANT_ID
- HTTP/API requests detected
- Potentially long-running operation

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_TENANT_ID in .env file
B) Export AZURE_TENANT_ID=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 58: import requests, os, time

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import requests, os, time
from azure.identity import DefaultAzureCredential

print("" + "="*80)
print("🔄 RESET: API-KEY Authentication (for remaining labs)")
print("="*80 + "")

# Configuration
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESOURCE_GROUP')
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
api_id = os.environ.get('APIM_API_ID', 'inference-api')

# Get management token
credential = DefaultAzureCredential()
mgmt_token = credential.get_to...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Environment variable required: SUBSCRIPTION_ID
- Environment variable required: APIM_SERVICE_NAME
- Environment variable required: RESOURCE_GROUP
- Environment variable required: APIM_API_ID
- HTTP/API requests detected
- Potentially long-running operation

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set APIM_SERVICE_NAME in .env file
B) Export APIM_SERVICE_NAME=<value> in terminal
C) Add to Azure Key Vault for production
A) Set RESOURCE_GROUP in .env file
B) Export RESOURCE_GROUP=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 59: Troubleshooting

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 60: <a id='lab07'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 61: Lab 07 Content Safety Test (adds JWT auth if required by current APIM policy)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Lab 07 Content Safety Test (adds JWT auth if required by current APIM policy)

def _get_jwt_token():
    # Reuse existing jwt_token if earlier cell created it
    if 'jwt_token' in globals() and jwt_token:
        return jwt_token
    try:
        cred = DefaultAzureCredential()
        tok = cred.get_token("https://cognitiveservices.azure.com/.default")
        return tok.token
    except Exception as _e:
        print(f'[auth] WARN: Unable to acquire JWT token ({_e}); proceeding without it.'...
```

**Issues Found**:
- OpenAI API import: openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 62: <a id='lab08'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 63: Lab 08: Model Routing test (fixed for Dual Auth + invalid model + 401 handling)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Lab 08: Model Routing test (fixed for Dual Auth + invalid model + 401 handling)

import os
from openai import AuthenticationError

# Ensure DefaultAzureCredential is available even if this cell runs before its import elsewhere.
try:
    DefaultAzureCredential  # type: ignore
except NameError:
    from azure.identity import DefaultAzureCredential

# Acquire JWT (audience: https://cognitiveservices.azure.com) – may be required with APIM dual auth.
try:
    credential = DefaultAzureCredential()
 ...
```

**Issues Found**:
- OpenAI API import: openai
- Azure SDK import: azure.identity

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable

**Recommended**: Option A (most common solution)

---

## Cell 64: <a id='lab09'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 65: AI Foundry SDK lab

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 66: deployment_name = "gpt-4o-mini"

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
deployment_name = "gpt-4o-mini"

missing_vars = [k for k, v in {
    'apim_gateway_url': globals().get('apim_gateway_url'),
    'inference_api_path': globals().get('inference_api_path'),
    'apim_api_key': globals().get('apim_api_key')
}.items() if not v]

if missing_vars:
    raise RuntimeError(f"Missing required variables: {', '.join(missing_vars)}. Run the earlier env/config cells first.")

# Normalize endpoint (avoid double slashes)
base = apim_gateway_url.rstrip('/')
inference_path = infer...
```

**Issues Found**:
- Azure SDK import: azure.identity
- Azure SDK import: azure.ai.inference
- Azure SDK import: azure.core.credentials
- Azure SDK import: azure.ai.inference.models

**Severity**: HIGH

**Potential Resolutions**:
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable

**Recommended**: Option A (most common solution)

---

## Cell 67: ---

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 68: """

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 69: Lab Example: Weather API (via APIM)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Lab Example: Weather API (via APIM)
"""
Demonstrates Weather API access through Azure API Management.

Features:
- Current weather for a city
- Multi-city comparison
- 5-day forecast
- Temperature, conditions, humidity
"""

print("=" * 80)
print("WEATHER API EXAMPLE (via APIM)")
print("=" * 80)

if not mcp.weather:
    print("❌ Weather API not configured")
    print("   Set APIM_WEATHER_URL and OPENWEATHER_API_KEY in .mcp-servers-config")
else:
    print("\n1️⃣  CURRENT WEATHER - London")
    ...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 70: Lab 10 Example: GitHub API (via APIM)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Lab 10 Example: GitHub API (via APIM)
"""
Demonstrates GitHub REST API access through Azure API Management.

Features:
- Repository details
- Statistics (stars, forks, watchers)
- Recent activity
"""

print("=" * 80)
print("GITHUB API EXAMPLE (via APIM)")
print("=" * 80)

if not mcp.github:
    print("❌ GitHub API not configured")
    print("   Set APIM_GITHUB_URL and APIM_SUBSCRIPTION_KEY in .mcp-servers-config")
else:
    print("\n1️⃣  REPOSITORY DETAILS")
    print("-" * 80)
    
    try:
 ...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 71: Lab 14: GitHub Repository Access

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 72: GitHub: Search and explore repositories (via APIM)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# GitHub: Search and explore repositories (via APIM)
"""
Search GitHub repositories using various criteria:
- Language filters
- Star count filters
- Sort by relevance, stars, or updated date
"""

print("=" * 80)
print("GITHUB REPOSITORY SEARCH (via APIM)")
print("=" * 80)

if not mcp.github:
    print("❌ GitHub API not configured")
else:
    try:
        # Search for AI/ML repositories
        search_query = "machine learning language:python stars:>1000"
        
        print(f"\n🔍 Search Quer...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 73: Lab 15: GitHub + AI Code Analysis

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 74: GitHub: Repository analysis (via APIM)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# GitHub: Repository analysis (via APIM)
"""
Perform deep analysis of a GitHub repository:
- Contributor statistics
- Issue tracking
- Pull request metrics
- Language breakdown
- Community health
"""

print("=" * 80)
print("GITHUB REPOSITORY ANALYSIS (via APIM)")
print("=" * 80)

if not mcp.github:
    print("❌ GitHub API not configured")
else:
    try:
        # Analyze a popular repository
        owner = "microsoft"
        repo = "semantic-kernel"
        
        print(f"\n🔍 Analyzing: {own...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 75: Multi-MCP AI Aggregation: Cross-Domain Analysis

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Multi-MCP AI Aggregation: Cross-Domain Analysis
"""
Demonstrates aggregating data from multiple MCP servers and using AI to synthesize insights.

This example:
1. Fetches GitHub repository data (stars, commits, issues)
2. Fetches Weather data for the repository's location
3. Combines both datasets
4. Sends to Azure OpenAI for cross-domain analysis
5. Generates actionable insights

This showcases the power of combining multiple data sources through MCP.
"""

print("=" * 80)
print("MULTI-MCP AI ...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 76: Section 2 Advanced MCP

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 77: Exercise 2.1: MCP Data + AI

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 78: Exercise 2.1: Sales Analysis via Local Pandas (NO MCP upload)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Exercise 2.1: Sales Analysis via Local Pandas (NO MCP upload)
print(" Sales Analysis via Local Pandas + Azure OpenAI")
print("=" * 80)

from pathlib import Path
import pandas as pd
import json

try:
    # Identify local Excel source relative to the notebook's location
    search_path = Path("./sample-data/excel/")
    excel_candidates = list(search_path.glob("*sales*.xlsx"))
    if not excel_candidates:
        raise FileNotFoundError(f"Could not locate a local Excel sales file in '{search_pat...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 79: Exercise 2.2: Sales Analysis via MCP + AI ONLY

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 80: This cell acts as a fallback if the primary MCP analysis in the previous cell fails.if 'sales_data_info' not in locals() or not sales_data_info:    print("⚠️ MCP analysis failed or returned no data. Initiating local fallback...")    try:        import pandas as pd        from pathlib import Path        import json         FIXED: Use CSV file instead of encrypted Excel file        csv_path = Path("./sample-data/csv/sales_performance.csv")        if not csv_path.exists():            print(f"❌ Fallback failed: CSV file not found at {csv_path.resolve()}")        else:            print(f"✅ Found local CSV file: {csv_path.resolve()}")             Read the CSV file using pandas            df = pd.read_csv(csv_path)             Generate a structure summary similar to the MCP output            structure = {                "file_name": csv_path.name,                "columns": df.columns.tolist(),                "row_count": len(df),                "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()},                "sample_data": df.head(3).to_dict('records')            }             Create a formatted string summary            summary_lines = [                f"File Name: {structure['file_name']}",                f"Total Rows: {structure['row_count']}",                f"Columns ({len(structure['columns'])}):"            ]            for col, dtype in structure['column_types'].items():                summary_lines.append(f"  - {col} (Type: {dtype})")            summary_lines.append("\nSample Data (First 3 Rows):")            for i, row in enumerate(structure['sample_data'], 1):                summary_lines.append(f"  Row {i}:")                for key, val in row.items():                    summary_lines.append(f"    {key}: {val}")             Store the summary in the required variable            sales_data_info = "\n".join(summary_lines)            print("\n" + "="*80)            print("✅ LOCAL FALLBACK ANALYSIS COMPLETE")            print("="*80)            print(sales_data_info)    except Exception as e:        print(f"❌ An error occurred during local fallback analysis: {e}")        import traceback        traceback.print_exc()else:    print("✅ MCP analysis was successful. Skipping local fallback.")

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# This cell acts as a fallback if the primary MCP analysis in the previous cell fails.if 'sales_data_info' not in locals() or not sales_data_info:    print("⚠️ MCP analysis failed or returned no data. Initiating local fallback...")    try:        import pandas as pd        from pathlib import Path        import json        # FIXED: Use CSV file instead of encrypted Excel file        csv_path = Path("./sample-data/csv/sales_performance.csv")        if not csv_path.exists():            print(f"❌ F...
```

**Issues Found**:
- File I/O operations detected

**Severity**: LOW

**Potential Resolutions**:
A) Verify file paths are correct
B) Check file permissions
C) Create required directories if missing

**Recommended**: Option A (most common solution)

---

## Cell 81: (Empty cell)

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 82: Excersice 2.3 Azure Cost Analysis via MCP

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 83: Exercise 2.3: Azure Cost Analysis via Local Pandasprint("💰 Azure Cost Analysis via Local Pandas + Azure OpenAI")print("=" * 80)from pathlib import Pathimport pandas as pdtry:     FIXED: Use CSV file instead of encrypted Excel file    cost_file_path = Path("./sample-data/csv/azure_resource_costs.csv")    if not cost_file_path.exists():        raise FileNotFoundError(f"Cost file not found at '{cost_file_path.resolve()}'")    print(f"✅ Reading cost file locally: {cost_file_path.name}")         Read CSV file using pandas    df = pd.read_csv(cost_file_path)        print(f"✅ File loaded successfully: {len(df)} rows, {len(df.columns)} columns")         Display columns    print(f"\n📊 Columns: {df.columns.tolist()}")         Preview data    print("\n👀 Preview (first 3 rows):")    print(df.head(3).to_string())     Determine column names (case-insensitive search)    group_by_col = None    metric_col = None         Look for ResourceType or ResourceName for grouping    for col in df.columns:        if 'resourcetype' in col.lower() or ('resource' in col.lower() and 'type' in col.lower()):            group_by_col = col        if 'cost' in col.lower():            metric_col = col        if not group_by_col:         Try ResourceName as fallback        for col in df.columns:            if 'resourcename' in col.lower() or 'resource' in col.lower():                group_by_col = col                break        if not group_by_col or not metric_col:        print(f"⚠️ Warning: Could not auto-detect columns. Available: {df.columns.tolist()}")         Use defaults if detection fails        group_by_col = group_by_col or df.columns[0]        metric_col = metric_col or df.columns[1] if len(df.columns) > 1 else df.columns[0]    print(f"\n📈 Analyzing costs with group_by='{group_by_col}' and metric='{metric_col}'")     Group by service and sum costs    cost_breakdown = df.groupby(group_by_col)[metric_col].agg(['sum', 'mean', 'count']).reset_index()    cost_breakdown.columns = ['ServiceName', 'Total', 'Average', 'Count']    cost_breakdown = cost_breakdown.sort_values('Total', ascending=False)         Calculate totals    total_cost = cost_breakdown['Total'].sum()     Assuming the data represents daily costs, calculate a monthly projection    monthly_projection = total_cost * 30    print("\n💵 Cost Analysis Summary:")    print("=" * 80)    print("📊 Cost Breakdown by Service Name:")    for idx, row in cost_breakdown.iterrows():        print(f"  - {row['ServiceName']}: ${row['Total']:,.2f} (Avg: ${row['Average']:,.2f}, Count: {row['Count']})")    print(f"\n💰 Total Daily Cost: ${total_cost:,.2f}")    print(f"📅 Projected Monthly Cost: ${monthly_projection:,.2f}")     Create a compact summary for AI analysis    cost_data_info = f"""Total Daily Cost: ${total_cost:,.2f}Projected Monthly Cost: ${monthly_projection:,.2f}Top Service: {cost_breakdown.iloc[0]['ServiceName']} (${cost_breakdown.iloc[0]['Total']:,.2f})Number of Services: {len(cost_breakdown)}"""    print("\n📋 Compact cost_data_info for AI prompts:")    print(cost_data_info)except Exception as e:    print(f"❌ ERROR (Cost Analysis): {e}")    print("🔍 Troubleshooting:")    print("  • Ensure the cost file exists at './sample-data/csv/azure_resource_costs.csv'")    print("  • Verify the file is a valid CSV format")    print("  • Check that pandas is installed: pip install pandas")    import traceback    traceback.print_exc()

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Exercise 2.3: Azure Cost Analysis via Local Pandasprint("💰 Azure Cost Analysis via Local Pandas + Azure OpenAI")print("=" * 80)from pathlib import Pathimport pandas as pdtry:    # FIXED: Use CSV file instead of encrypted Excel file    cost_file_path = Path("./sample-data/csv/azure_resource_costs.csv")    if not cost_file_path.exists():        raise FileNotFoundError(f"Cost file not found at '{cost_file_path.resolve()}'")    print(f"✅ Reading cost file locally: {cost_file_path.name}")        # ...
```

**Issues Found**:
- File I/O operations detected

**Severity**: LOW

**Potential Resolutions**:
A) Verify file paths are correct
B) Check file permissions
C) Create required directories if missing

**Recommended**: Option A (most common solution)

---

## Cell 84: Exercise 2.4 : Function Calling with MCP Tools

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 85: Exercise 2.4 & 2.5: Function Calling with MCP Tools (enhanced diagnostics)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Exercise 2.4 & 2.5: Function Calling with MCP Tools (enhanced diagnostics)
# Architecture: MCP connects directly to server, OpenAI goes through APIM

import json
import asyncio
import time
from mcp import ClientSession, McpError
from mcp.client.streamable_http import streamablehttp_client
from mcp.client import session as mcp_client_session
from openai import AzureOpenAI
import nest_asyncio
nest_asyncio.apply()

# CRITICAL FIX: Server uses MCP protocol v1.0; patch client to accept it
# The ser...
```

**Issues Found**:
- OpenAI API import: openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 86: Section 3: Advanced Framework + MCP Integration

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 87: Exercise 3.1: Microsoft Agent Framework with MCP

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 88: ⚠️ Exercise 3.1: Microsoft Agent Framework with MCP (COMMENTED OUT)

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 89: Exercise 3.2: Semantic Kernel OpenAI Agent with MCP + Timeout Handling

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 90: import asyncio

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# import asyncio
# import nest_asyncio
# from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
# from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
# from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
#
# nest_asyncio.apply()
#
# # Use the working Docs MCP server
# DOCS_MCP_URL = mcp.docs.server_url if (mcp and hasattr(mcp, "docs")) else "http://docs-mcp-24774.eastus.azurecontainer.io:8000"
#
# user_input = "Can you retrieve the azure-o...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 91: 🧪 SEMANTIC KERNEL TESTING SUITE - 15 TECHNIQUES

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 92: ========================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ========================================================================
# TECHNIQUE 1: Direct Azure OpenAI (Baseline - No SK, No MCP)
# ========================================================================
import time

print("TECHNIQUE 1: Direct Azure OpenAI")
print("="*70)
print("Purpose: Verify Azure OpenAI works through APIM")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from openai import AzureOpenAI
    
    client = AzureOpenAI(
        azure_endpoint=f"{apim_gatewa...
```

**Issues Found**:
- OpenAI API import: openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 93: ========================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ========================================================================
# TECHNIQUE 2: Semantic Kernel Without MCP (Baseline)
# ========================================================================
import time

print("TECHNIQUE 2: Semantic Kernel Without MCP")
print("="*70)
print("Purpose: Verify SK works with Azure OpenAI")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatComple...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 94: ========================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ========================================================================
# TECHNIQUE 3: ChatCompletionAgent Without MCP (Baseline)
# ========================================================================
import time
import asyncio

print("TECHNIQUE 3: ChatCompletionAgent Without MCP")
print("="*70)
print("Purpose: Verify SK Agent works without MCP plugin")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from semantic_kernel.agents import ChatCompletionAgent
    from semantic_k...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 95: ========================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ========================================================================
# TECHNIQUE 4: Manual MCP Connection with Timeout (Diagnostic)
# ========================================================================
import time
import asyncio
import httpx

print("TECHNIQUE 4: Manual MCP Connection Test")
print("="*70)
print("Purpose: Test MCP server connectivity with timeout")
print(f"Target: {mcp.docs.server_url if mcp and hasattr(mcp, 'docs') else 'http://docs-mcp-master.eastus.azurecontainer.io:...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 96: ========================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ========================================================================
# TECHNIQUE 8: Direct Function Calling (No Framework)
# ========================================================================
import time
import json

print("TECHNIQUE 8: Direct Function Calling")
print("="*70)
print("Purpose: Manual function calling without agent framework")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from openai import AzureOpenAI
    import httpx
    
    # Define tool manually
  ...
```

**Issues Found**:
- OpenAI API import: openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 97: ========================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ========================================================================
# TECHNIQUE 15: Hybrid Approach - SK Orchestration + Direct HTTP
# ========================================================================
import time
import asyncio
import httpx

print("TECHNIQUE 15: Hybrid Approach (RECOMMENDED)")
print("="*70)
print("Purpose: Use SK for chat, bypass MCP plugin with direct HTTP")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from semantic_kernel import Kernel
    from ...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 98: 🎯 PRODUCTION SOLUTION: AutoGen + APIM

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 99: ========================================================================

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# ========================================================================
# PRODUCTION: AutoGen + APIM + MCP (SSE Transport)
# ========================================================================
import asyncio
import time

print("🎯 PRODUCTION AUTOGEN + APIM SOLUTION")
print("="*70)
print()

async def run_autogen_agent(task: str, mcp_endpoint: str, timeout: int = 30):
    """
    Run AutoGen agent with MCP tools through APIM
    
    Args:
        task: User query/task
        mcp_endpoint:...
```

**Issues Found**:
- OpenAI API import: autogen_ext.models.openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 100: 📊 TESTING RESULTS SUMMARY

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 101: <a id='autogen'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 102: 1. [Configure the GitHub MCP Server in VS Code](https://code...

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 103: <a id='githubtest'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 104: import asyncio

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import asyncio
from asyncio import TimeoutError
import nest_asyncio
nest_asyncio.apply()

async def run_with_timeout(task, timeout_seconds=300, task_name="Semantic Kernel task"):
    """
    Run Semantic Kernel task with timeout to prevent indefinite hanging
    
    Args:
        task: Async task/coroutine to run
        timeout_seconds: Maximum time to wait (default: 300s = 5 min)
        task_name: Description for error messages
        
    Returns:
        Task result if successful
        ...
```

**Issues Found**:
- OpenAI API import: openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 105: 🔍 Diagnostic Troubleshooting Cell

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 106: import asyncio

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import asyncio
import httpx
import sys
from datetime import datetime

print("=" * 80)
print("SEMANTIC KERNEL DIAGNOSTIC REPORT")
print(f"Generated: {datetime.now().isoformat()}")
print("=" * 80)

# Test 1: Python Environment
print("\n[1/7] Python Environment")
print("-" * 80)
print(f"Python version: {sys.version}")
print(f"asyncio: {asyncio.__version__ if hasattr(asyncio, '__version__') else 'built-in'}")

# Test 2: Package Versions
print("\n[2/7] Package Versions")
print("-" * 80)
packages_to_c...
```

**Issues Found**:
- OpenAI API import: openai

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 107: Semantic Cache Performance

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 108: import redis.asyncio as redis  # unused currently; keep if p...

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import redis.asyncio as redis  # unused currently; keep if planning Redis integration
import random  # required for random.choice

questions = [
    'How to make coffee?',
    'What is the best way to brew coffee?',
    'Tell me about coffee preparation',
    'Coffee making tips?'
]

times = []

# Ensure 'time' module is available without re-importing if already loaded
try:
    time
except NameError:
    import time

# Initialize AzureOpenAI client if missing (reuse earlier env vars)
if 'client'...
```

**Issues Found**:
- OpenAI API import: openai
- HTTP/API requests detected
- Potentially long-running operation

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 109: ---

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 110: ---

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 111: <a id='lab22'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 112: Test: Generate Images

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 113: Deployment discovery for image & vision models

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Deployment discovery for image & vision models
import os, requests, json
from typing import Dict, List

inference_api_path = os.getenv("INFERENCE_API_PATH", "inference")
# Safely derive gateway URL; fall back to existing global if previously defined
apim_gateway_url = os.getenv("APIM_GATEWAY_URL") or os.getenv("APIM_GATEWAY") or globals().get("apim_gateway_url")
api_version = (os.getenv("OPENAI_IMAGE_API_VERSION")
               or os.getenv("OPENAI_CHAT_API_VERSION")
               or "2025-0...
```

**Issues Found**:
- Environment variable required: INFERENCE_API_PATH
- Environment variable required: APIM_SCOPE
- Environment variable required: APIM_GATEWAY_URL
- Environment variable required: APIM_GATEWAY
- Environment variable required: DALL_E_DEPLOYMENT
- Environment variable required: FLUX_DEPLOYMENT
- Environment variable required: OPENAI_CHAT_API_VERSION
- Environment variable required: USE_JWT_FOR_IMAGE
- Environment variable required: OPENAI_IMAGE_API_VERSION
- HTTP/API requests detected

**Severity**: HIGH

**Potential Resolutions**:
A) Set INFERENCE_API_PATH in .env file
B) Export INFERENCE_API_PATH=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_SCOPE in .env file
B) Export APIM_SCOPE=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_GATEWAY_URL in .env file
B) Export APIM_GATEWAY_URL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_GATEWAY in .env file
B) Export APIM_GATEWAY=<value> in terminal
C) Add to Azure Key Vault for production
A) Set DALL_E_DEPLOYMENT in .env file
B) Export DALL_E_DEPLOYMENT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set FLUX_DEPLOYMENT in .env file
B) Export FLUX_DEPLOYMENT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set OPENAI_CHAT_API_VERSION in .env file
B) Export OPENAI_CHAT_API_VERSION=<value> in terminal
C) Add to Azure Key Vault for production
A) Set USE_JWT_FOR_IMAGE in .env file
B) Export USE_JWT_FOR_IMAGE=<value> in terminal
C) Add to Azure Key Vault for production
A) Set OPENAI_IMAGE_API_VERSION in .env file
B) Export OPENAI_IMAGE_API_VERSION=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 114: Image & Vision Model Flow (Updated)

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 115: Validate required environment variables

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Validate required environment variables
required_vars = ['RESOURCE_GROUP', 'APIM_GATEWAY_URL']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing environment variables: {missing}")
    print("   Run Cell 3 (Environment Loader) first")
    raise RuntimeError(f"Missing variables: {missing}")

# Updated Lab 22 Image Generation & Vision Analysis (FLUX models with deployment-style routing)
import os, base64, json, requests
from typing import Optional

# Cor...
```

**Issues Found**:
- Environment variable required: INFERENCE_API_PATH
- Environment variable required: DALL_E_DEFAULT_SIZE
- Environment variable required: APIM_GATEWAY_URL
- Environment variable required: IMAGE_OUTPUT_FORMAT
- Environment variable required: VISION_MODEL
- Environment variable required: DALL_E_DEPLOYMENT
- Environment variable required: FLUX_DEPLOYMENT
- Environment variable required: USE_JWT_FOR_IMAGE
- Environment variable required: OPENAI_IMAGE_API_VERSION
- Environment variable required: FLUX_DEFAULT_SIZE
- HTTP/API requests detected
- File I/O operations detected

**Severity**: HIGH

**Potential Resolutions**:
A) Set INFERENCE_API_PATH in .env file
B) Export INFERENCE_API_PATH=<value> in terminal
C) Add to Azure Key Vault for production
A) Set DALL_E_DEFAULT_SIZE in .env file
B) Export DALL_E_DEFAULT_SIZE=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_GATEWAY_URL in .env file
B) Export APIM_GATEWAY_URL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set IMAGE_OUTPUT_FORMAT in .env file
B) Export IMAGE_OUTPUT_FORMAT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set VISION_MODEL in .env file
B) Export VISION_MODEL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set DALL_E_DEPLOYMENT in .env file
B) Export DALL_E_DEPLOYMENT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set FLUX_DEPLOYMENT in .env file
B) Export FLUX_DEPLOYMENT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set USE_JWT_FOR_IMAGE in .env file
B) Export USE_JWT_FOR_IMAGE=<value> in terminal
C) Add to Azure Key Vault for production
A) Set OPENAI_IMAGE_API_VERSION in .env file
B) Export OPENAI_IMAGE_API_VERSION=<value> in terminal
C) Add to Azure Key Vault for production
A) Set FLUX_DEFAULT_SIZE in .env file
B) Export FLUX_DEFAULT_SIZE=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 116: Lab 01: Test - Temperature Variations

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 117: for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'Write a creative sentence'}],
        temperature=temp,
        max_tokens=30
    )
    print(f'Temp {temp}: {response.choices[0].message.content}')
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 118: Lab 01: Test - System Prompts

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 119: system_prompts = [

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
system_prompts = [
    'You are a helpful assistant.',
    'You are a sarcastic comedian.',
    'You are a professional technical writer.',
    'You are a poet.'
]

for prompt in system_prompts:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': 'Describe the weather'}
        ],
        max_tokens=50
    )
    print(f'\n{prompt}:\n{response.choices[0].message.co...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 120: Lab 19: Test - Redis Connection

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 121: import redis.asyncio as redis

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import redis.asyncio as redis

# Resolve Redis connection settings without redefining earlier variables if already present
# Prefer existing globals, then environment (.env / master-lab.env), then step3_outputs
redis_host = globals().get('redis_host') or os.getenv('REDIS_HOST') or step3_outputs.get('redisCacheHost')
redis_port_raw = globals().get('redis_port') or os.getenv('REDIS_PORT') or step3_outputs.get('redisCachePort', 6380)
redis_key = globals().get('redis_key') or os.getenv('REDIS_KEY') ...
```

**Issues Found**:
- Environment variable required: REDIS_PORT
- Environment variable required: REDIS_HOST
- Environment variable required: REDIS_KEY

**Severity**: HIGH

**Potential Resolutions**:
A) Set REDIS_PORT in .env file
B) Export REDIS_PORT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set REDIS_HOST in .env file
B) Export REDIS_HOST=<value> in terminal
C) Add to Azure Key Vault for production
A) Set REDIS_KEY in .env file
B) Export REDIS_KEY=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 122: Lab 22: Test - Multiple Image Styles

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 123: FIXED: Updated to use FLUX-1.1-pro instead of dall-e-3

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# FIXED: Updated to use FLUX-1.1-pro instead of dall-e-3
prompts = [
    'A serene mountain landscape at dawn',
    'Abstract geometric patterns in blue and gold',
    'A cyberpunk city street at night'
]

for i, prompt in enumerate(prompts):
    print(f'Generating image {i+1}: {prompt}')
    response = requests.post(
        f'{apim_gateway_url}/{inference_api_path}/openai/deployments/FLUX-1.1-pro/images/generations?api-version={api_version}',
        headers={'api-key': apim_api_key},
        ...
```

**Issues Found**:
- HTTP/API requests detected
- File I/O operations detected

**Severity**: MEDIUM

**Potential Resolutions**:
A) Verify network connectivity
B) Check firewall/proxy settings
C) Add retry logic with exponential backoff

**Recommended**: Option A (most common solution)

---

## Cell 124: Lab 13: MCP Client Authorization

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 125: MCP OAuth authorization test with APIM (Cell 99)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# MCP OAuth authorization test with APIM (Cell 99)

print("=== MCP Authorization Test ===")

# Reuse existing credential (ClientSecretCredential) and MCP_SERVERS
if 'credential' not in globals():
    print("[ERROR] 'credential' not initialized earlier.")
else:
    audiences = [
        f"api://{client_id}/.default",              # Common custom API audience pattern
        "https://management.azure.com/.default"     # Fallback ARM scope
    ]

    access_token = None
    used_audience = None
   ...
```

**Issues Found**:
- HTTP/API requests detected

**Severity**: MEDIUM

**Potential Resolutions**:
A) Verify network connectivity
B) Check firewall/proxy settings
C) Add retry logic with exponential backoff

**Recommended**: Option A (most common solution)

---

## Cell 126: Lab 14: A2A Agents - Multi-Agent Communication

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 127: Agent-to-Agent (A2A) communication test via existing agent outputs and LLM refinement

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Agent-to-Agent (A2A) communication test via existing agent outputs and LLM refinement
print('Testing A2A agent communication...')

required = ['planner', 'critic', 'summarizer']
missing = [r for r in required if 'agents' not in globals() or r not in agents]
if missing:
    print(f'[ERROR] Missing agents: {missing}')
else:
    print(f'[OK] Agents available: {required}')

# Use existing collected outputs if present
source_outputs = agent_outputs if 'agent_outputs' in globals() and agent_outputs ...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 128: Lab 15: OpenAI Agents - Create Assistant

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 129: Using Azure AI Agents (fallback stub if project_client is not defined)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Using Azure AI Agents (fallback stub if project_client is not defined)

if 'project_client' not in globals():
    # Minimal in-memory stub to avoid NameError and simulate Agents API behavior
    import uuid

    class _TextWrapper:
        def __init__(self, value): self.value = value

    class _ContentPart:
        def __init__(self, value): self.text = _TextWrapper(value)

    class _Message:
        def __init__(self, role, content):
            self.id = str(uuid.uuid4())
            self...
```

**Issues Found**:
- Potentially long-running operation

**Severity**: MEDIUM

**Potential Resolutions**:
A) Add progress indicators
B) Optimize algorithm if possible
C) Consider async/parallel execution

**Recommended**: Option A (most common solution)

---

## Cell 130: Lab 16: AI Agent Service - Multiple Agents

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 131: import time

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import time

# Multi-agent scenario (planning, critic, summarizer) using existing agents_client + client
print('AI Agent Service: multi-agent test...')

# Create agents
agents = {
    'planner': agents_client.create_agent(model='gpt-4o-mini', name='planner', instructions='Plan a concise Azure AI workshop agenda.'),
    'critic': agents_client.create_agent(model='gpt-4o-mini', name='critic', instructions='Review a proposed agenda and point out gaps.'),
    'summarizer': agents_client.create_agent...
```

**Issues Found**:
- Potentially long-running operation

**Severity**: MEDIUM

**Potential Resolutions**:
A) Add progress indicators
B) Optimize algorithm if possible
C) Consider async/parallel execution

**Recommended**: Option A (most common solution)

---

## Cell 132: Lab 18: Function Calling - Multiple Functions

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 133: functions = [

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
functions = [
    {
        'name': 'get_weather',
        'description': 'Get weather for a location',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {'type': 'string', 'description': 'City name'}
            },
            'required': ['location']
        }
    },
    {
        'name': 'calculate',
        'description': 'Perform calculation',
        'parameters': {
            'type': 'object',
            'properties': {
       ...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 134: Lab 20: Message Storing - Store and Retrieve

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 135: Cosmos DB message storage (uses existing env + step outputs; avoids printing secrets)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Cosmos DB message storage (uses existing env + step outputs; avoids printing secrets)

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError

# Resolve endpoint/key (prefer existing vars, then env, then deployment outputs; guard missing step3_outputs)
_step3 = globals().get('step3_outputs', {}) or {}
cosmos_endpoint = globals().get('cosmos_endpoint') or os.getenv('COSMOS_ENDPOINT') or _step3.get('cosmosDbEndpoint')
cosmos_key = globals(...
```

**Issues Found**:
- Azure SDK import: azure.cosmos
- Azure SDK import: azure.cosmos.exceptions
- Environment variable required: COSMOS_KEY
- Environment variable required: COSMOS_ENDPOINT

**Severity**: HIGH

**Potential Resolutions**:
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable
A) Install Azure SDK: pip install azure-mgmt-* azure-identity
B) Configure Azure credentials (az login or service principal)
C) Set AZURE_SUBSCRIPTION_ID environment variable
A) Set COSMOS_KEY in .env file
B) Export COSMOS_KEY=<value> in terminal
C) Add to Azure Key Vault for production
A) Set COSMOS_ENDPOINT in .env file
B) Export COSMOS_ENDPOINT=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 136: Lab 24: FinOps Framework - Cost Analysis

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 137: Simulate cost tracking

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Simulate cost tracking
costs = []
for i in range(10):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'test'}],
        max_tokens=50
    )
    # Estimate cost (example rates)
    prompt_cost = response.usage.prompt_tokens * 0.00015 / 1000
    completion_cost = response.usage.completion_tokens * 0.00060 / 1000
    total_cost = prompt_cost + completion_cost
    costs.append(total_cost)

print(f'Total estimated cost: ${sum...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 138: <a id='testSecureWithDirectHttp'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 139: <a id='testSecureWithDirectHttp'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 140: <a id='kql'></a>

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 141: import pandas as pd

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import pandas as pd

query = "let llmHeaderLogs = ApiManagementGatewayLlmLog \
| where DeploymentName != ''; \
let llmLogsWithSubscriptionId = llmHeaderLogs \
| join kind=leftouter ApiManagementGatewayLogs on CorrelationId \
| project \
    SubscriptionId = ApimSubscriptionId, DeploymentName, TotalTokens; \
llmLogsWithSubscriptionId \
| summarize \
    SumTotalTokens      = sum(TotalTokens) \
  by SubscriptionId, DeploymentName"

# Resolve Log Analytics workspace/customer ID from existing global...
```

**Issues Found**:
- Environment variable required: LOG_ANALYTICS_WORKSPACE_ID

**Severity**: HIGH

**Potential Resolutions**:
A) Set LOG_ANALYTICS_WORKSPACE_ID in .env file
B) Export LOG_ANALYTICS_WORKSPACE_ID=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 142: All 31 Labs Tested Successfully!

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 143: print('='*60)

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
print('='*60)
print('MASTER LAB TESTING COMPLETE')
print('='*60)
print('\nSummary:')
print('  - 31 labs tested')
print('  - All features validated')
print('  - Ready for production use')
print('\nNext steps:')
print('  1. Review logs in Azure Portal')
print('  2. Analyze performance metrics')
print('  3. Customize policies as needed')
print('  4. Scale resources based on load')
print('\nCleanup: Run master-cleanup.ipynb')
print('\n[OK] Master lab complete!')
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 144: Lab 01: Extended Test 1 - Scenario Variations

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 145: Extra Cells

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 146: import os, pathlib

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import os, pathlib
TENANT_ID = "2b9d9f47-1fb6-400a-a438-39fe7d768649"
os.environ["AZURE_TENANT_ID"] = TENANT_ID
print(f"AZURE_TENANT_ID exported: {TENANT_ID}")
# Ensure .env has the tenant id (already patched, but idempotent safeguard)
env_path = pathlib.Path('.env')
lines = []
if env_path.exists():
    with env_path.open('r', encoding='utf-8') as f:
        lines = f.readlines()
found = any(l.startswith('AZURE_TENANT_ID=') for l in lines)
if not found:
    lines.append(f'AZURE_TENANT_ID={TENANT...
```

**Issues Found**:
- Environment variable required: AZURE_TENANT_ID
- File I/O operations detected

**Severity**: CRITICAL

**Potential Resolutions**:
A) Set AZURE_TENANT_ID in .env file
B) Export AZURE_TENANT_ID=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 147: import base64, math

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
import base64, math

# Image & Vision Model Initialization
# Chooses direct Azure OpenAI endpoint (if discovered) else APIM gateway route.

IMAGE_MODEL = globals().get('DALL_E_DEPLOYMENT') or os.environ.get('DALL_E_DEPLOYMENT') or 'gpt-image-1'
VISION_MODEL = globals().get('VISION_MODEL') or os.environ.get('VISION_MODEL') or 'gpt-4o'
IMAGE_API_VERSION = globals().get('OPENAI_IMAGE_API_VERSION') or os.environ.get('OPENAI_IMAGE_API_VERSION') or '2025-06-01-preview'
CHAT_API_VERSION = globals().get...
```

**Issues Found**:
- Environment variable required: INFERENCE_API_PATH
- Environment variable required: AZURE_OPENAI_API_KEY
- Environment variable required: DALL_E_DEFAULT_SIZE
- Environment variable required: IMAGE_OUTPUT_FORMAT
- Environment variable required: APIM_GATEWAY_URL
- Environment variable required: VISION_MODEL
- Environment variable required: DALL_E_DEPLOYMENT
- Environment variable required: OPENAI_CHAT_API_VERSION
- Environment variable required: USE_JWT_FOR_IMAGE
- Environment variable required: OPENAI_IMAGE_API_VERSION
- HTTP/API requests detected

**Severity**: HIGH

**Potential Resolutions**:
A) Set INFERENCE_API_PATH in .env file
B) Export INFERENCE_API_PATH=<value> in terminal
C) Add to Azure Key Vault for production
A) Set AZURE_OPENAI_API_KEY in .env file
B) Export AZURE_OPENAI_API_KEY=<value> in terminal
C) Add to Azure Key Vault for production
A) Set DALL_E_DEFAULT_SIZE in .env file
B) Export DALL_E_DEFAULT_SIZE=<value> in terminal
C) Add to Azure Key Vault for production
A) Set IMAGE_OUTPUT_FORMAT in .env file
B) Export IMAGE_OUTPUT_FORMAT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set APIM_GATEWAY_URL in .env file
B) Export APIM_GATEWAY_URL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set VISION_MODEL in .env file
B) Export VISION_MODEL=<value> in terminal
C) Add to Azure Key Vault for production
A) Set DALL_E_DEPLOYMENT in .env file
B) Export DALL_E_DEPLOYMENT=<value> in terminal
C) Add to Azure Key Vault for production
A) Set OPENAI_CHAT_API_VERSION in .env file
B) Export OPENAI_CHAT_API_VERSION=<value> in terminal
C) Add to Azure Key Vault for production
A) Set USE_JWT_FOR_IMAGE in .env file
B) Export USE_JWT_FOR_IMAGE=<value> in terminal
C) Add to Azure Key Vault for production
A) Set OPENAI_IMAGE_API_VERSION in .env file
B) Export OPENAI_IMAGE_API_VERSION=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 148: Test Image Generation (Minimal) - FIXED to use FLUX models

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Test Image Generation (Minimal) - FIXED to use FLUX models
import time

TEST_PROMPT = "A tiny sketch of a futuristic Azure data center shaped like a cloud, line art"
print(f"[test] Attempting generation with model={image_model}")

start_time = time.time()
result = generate_image(image_model, TEST_PROMPT, '512x512')
elapsed = time.time() - start_time

if result.get('b64'):
    b64_result = result['b64']
    print(f"[test] Success in {elapsed:.2f}s; preview below (first 80 chars):")
    print(b6...
```

**Issues Found**:
- File I/O operations detected

**Severity**: LOW

**Potential Resolutions**:
A) Verify file paths are correct
B) Check file permissions
C) Create required directories if missing

**Recommended**: Option A (most common solution)

---

## Cell 149: Set Azure OpenAI resource name manually if not discovered

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Set Azure OpenAI resource name manually if not discovered
# Replace PLACEHOLDER_RESOURCE with your actual Azure OpenAI resource (e.g., aoai-master-lab or openai-xyz123)
resource_name = os.environ.get('OPENAI_RESOURCE_NAME') or 'PLACEHOLDER_RESOURCE'
print(f"[resource-name] Using resource_name={resource_name}")
_ = discover_openai_endpoint(resource_name=resource_name)
print(f"[resource-name] OPENAI_ENDPOINT={OPENAI_ENDPOINT}")
```

**Issues Found**:
- Environment variable required: OPENAI_RESOURCE_NAME

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_RESOURCE_NAME in .env file
B) Export OPENAI_RESOURCE_NAME=<value> in terminal
C) Add to Azure Key Vault for production

**Recommended**: Option A (most common solution)

---

## Cell 150: Manual Deployment Commands (Fallback)

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 151: (Empty cell)

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 152: Exercise 2.5: Dynamic Column Analysis

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 153: Exercise 2.5: Dynamic Column Analysis

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Exercise 2.5: Dynamic Column Analysis
print(" Dynamic MCP Analysis with User-Defined Columns")
print("=" * 80)

try:
    # --- Define columns for analysis ---
    # These variables can be changed to analyze different aspects of the data
    group_by_column = 'Product'  # Change to 'Product', 'CustomerID', etc.
    metric_column = 'Quantity'   # Change to 'Quantity', 'TotalSales', etc.

    # Use the file key from the successful sales analysis in Exercise 2.1
    if 'excel_cache_key' not in loc...
```

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 154: Exercise 2.6: AI-Generated Sales Insights

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 155: Test MCP-Enabled Agent

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

## Cell 156: Post-Upgrade Verification for Agents and AzureOpenAI

**Type**: code
**Status**: Static Analysis
**Execution Time**: N/A

**Source Code Preview**:
```python
# Post-Upgrade Verification for Agents and AzureOpenAI
import importlib, json

ver_openai = None
try:
    import openai
    ver_openai = getattr(openai, '__version__', 'unknown')
except Exception as ex:
    print(f'[verify] Failed to import openai: {ex}')

ver_agents = None
try:
    import openai_agents
    ver_agents = getattr(openai_agents, '__version__', 'unknown')
except Exception as ex:
    print(f'[verify] Failed to import openai-agents: {ex}')

print(f'[verify] openai version: {ver_openai...
```

**Issues Found**:
- OpenAI API import: openai
- OpenAI API import: openai_agents

**Severity**: HIGH

**Potential Resolutions**:
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity
A) Set OPENAI_API_KEY environment variable
B) Install openai package: pip install openai
C) Verify API key validity

**Recommended**: Option A (most common solution)

---

## Cell 157: Agent Dependency Note for MCP Labs

**Type**: markdown
**Status**: Static Analysis
**Execution Time**: N/A

**Issues Found**: None detected
**Severity**: INFO

---

# Issues by Category

## Infrastructure

- Cell 12: Azure Management API usage [HIGH]
- Cell 27: Azure Management API usage [HIGH]
- Cell 29: Azure Management API usage [HIGH]

## Dependencies

*No dependencies issues found*

## Configuration

- Cell 3: Environment variable required: APIM_SERVICE [HIGH]
- Cell 3: Environment variable required: API_ID [HIGH]
- Cell 3: Environment variable required: BICEP_DIR [HIGH]
- Cell 5: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 5: Environment variable required: AZ_CLI [HIGH]
- Cell 5: Environment variable required: CODESPACES [HIGH]
- Cell 5: Environment variable required: AZURE_CLI_PATH [HIGH]
- Cell 5: Environment variable required: CODESPACE_NAME [HIGH]
- Cell 7: Environment variable required: OPENAI_ENDPOINT [HIGH]
- Cell 8: Environment variable required: AZURE_CLIENT_ID [CRITICAL]
- Cell 8: Environment variable required: AZURE_CLIENT_SECRET [CRITICAL]
- Cell 8: Environment variable required: AZ_CLI [HIGH]
- Cell 8: Environment variable required: AZURE_CLI_PATH [HIGH]
- Cell 8: Environment variable required: AZURE_TENANT_ID [CRITICAL]
- Cell 10: Environment variable required: APIM_SERVICE [HIGH]
- Cell 10: Environment variable required: API_ID [HIGH]
- Cell 10: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 12: Environment variable required: AZURE_CLIENT_ID [CRITICAL]
- Cell 12: Environment variable required: VIRTUAL_ENV [HIGH]
- Cell 12: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 12: Environment variable required: AZURE_CLIENT_SECRET [CRITICAL]
- Cell 12: Environment variable required: AZ_CLI [HIGH]
- Cell 12: Environment variable required: AZURE_CLI_PATH [HIGH]
- Cell 12: Environment variable required: AZ_OPS_STRATEGY [HIGH]
- Cell 12: Environment variable required: AZURE_TENANT_ID [CRITICAL]
- Cell 12: Environment variable required: AZURE_SUBSCRIPTION_ID [CRITICAL]
- Cell 17: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 17: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 17: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 17: Environment variable required: APIM_API_ID [HIGH]
- Cell 22: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 22: Environment variable required: AZ_PATH [HIGH]
- Cell 22: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 22: Environment variable required: APIM_API_ID [HIGH]
- Cell 22: Environment variable required: AZURE_CLI_PATH [HIGH]
- Cell 27: Environment variable required: AZURE_CLIENT_ID [CRITICAL]
- Cell 27: Environment variable required: AZURE_TENANT_ID [CRITICAL]
- Cell 27: Environment variable required: AZURE_CLIENT_SECRET [CRITICAL]
- Cell 29: Environment variable required: BICEP_DIR [HIGH]
- Cell 31: Environment variable required: APIM_API_ID [HIGH]
- Cell 32: Environment variable required: APIM_GATEWAY_URL [HIGH]
- Cell 32: Environment variable required: APIM_API_KEY [HIGH]
- Cell 32: Environment variable required: INFERENCE_API_PATH [HIGH]
- Cell 37: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 37: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 37: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 37: Environment variable required: APIM_API_ID [HIGH]
- Cell 43: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 43: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 43: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 43: Environment variable required: APIM_API_ID [HIGH]
- Cell 45: Environment variable required: OPENAI_API_VERSION [HIGH]
- Cell 45: Environment variable required: APIM_GATEWAY_URL [HIGH]
- Cell 45: Environment variable required: INFERENCE_API_PATH [HIGH]
- Cell 45: Environment variable required: APIM_API_KEY [HIGH]
- Cell 50: Environment variable required: OPENAI_API_VERSION [HIGH]
- Cell 50: Environment variable required: APIM_GATEWAY_URL [HIGH]
- Cell 50: Environment variable required: INFERENCE_API_PATH [HIGH]
- Cell 50: Environment variable required: APIM_API_KEY [HIGH]
- Cell 55: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 55: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 55: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 55: Environment variable required: APIM_API_ID [HIGH]
- Cell 55: Environment variable required: AZ_CLI [HIGH]
- Cell 55: Environment variable required: AZURE_TENANT_ID [CRITICAL]
- Cell 56: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 56: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 56: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 56: Environment variable required: APIM_API_ID [HIGH]
- Cell 56: Environment variable required: AZ_CLI [HIGH]
- Cell 57: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 57: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 57: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 57: Environment variable required: APIM_API_ID [HIGH]
- Cell 57: Environment variable required: AZ_CLI [HIGH]
- Cell 57: Environment variable required: AZURE_TENANT_ID [CRITICAL]
- Cell 58: Environment variable required: SUBSCRIPTION_ID [HIGH]
- Cell 58: Environment variable required: APIM_SERVICE_NAME [CRITICAL]
- Cell 58: Environment variable required: RESOURCE_GROUP [CRITICAL]
- Cell 58: Environment variable required: APIM_API_ID [HIGH]
- Cell 113: Environment variable required: INFERENCE_API_PATH [HIGH]
- Cell 113: Environment variable required: APIM_SCOPE [HIGH]
- Cell 113: Environment variable required: APIM_GATEWAY_URL [HIGH]
- Cell 113: Environment variable required: APIM_GATEWAY [HIGH]
- Cell 113: Environment variable required: DALL_E_DEPLOYMENT [HIGH]
- Cell 113: Environment variable required: FLUX_DEPLOYMENT [HIGH]
- Cell 113: Environment variable required: OPENAI_CHAT_API_VERSION [HIGH]
- Cell 113: Environment variable required: USE_JWT_FOR_IMAGE [HIGH]
- Cell 113: Environment variable required: OPENAI_IMAGE_API_VERSION [HIGH]
- Cell 115: Environment variable required: INFERENCE_API_PATH [HIGH]
- Cell 115: Environment variable required: DALL_E_DEFAULT_SIZE [HIGH]
- Cell 115: Environment variable required: APIM_GATEWAY_URL [HIGH]
- Cell 115: Environment variable required: IMAGE_OUTPUT_FORMAT [HIGH]
- Cell 115: Environment variable required: VISION_MODEL [HIGH]
- Cell 115: Environment variable required: DALL_E_DEPLOYMENT [HIGH]
- Cell 115: Environment variable required: FLUX_DEPLOYMENT [HIGH]
- Cell 115: Environment variable required: USE_JWT_FOR_IMAGE [HIGH]
- Cell 115: Environment variable required: OPENAI_IMAGE_API_VERSION [HIGH]
- Cell 115: Environment variable required: FLUX_DEFAULT_SIZE [HIGH]
- Cell 121: Environment variable required: REDIS_PORT [HIGH]
- Cell 121: Environment variable required: REDIS_HOST [HIGH]
- Cell 121: Environment variable required: REDIS_KEY [HIGH]
- Cell 135: Environment variable required: COSMOS_KEY [HIGH]
- Cell 135: Environment variable required: COSMOS_ENDPOINT [HIGH]
- Cell 141: Environment variable required: LOG_ANALYTICS_WORKSPACE_ID [HIGH]
- Cell 146: Environment variable required: AZURE_TENANT_ID [CRITICAL]
- Cell 147: Environment variable required: INFERENCE_API_PATH [HIGH]
- Cell 147: Environment variable required: AZURE_OPENAI_API_KEY [HIGH]
- Cell 147: Environment variable required: DALL_E_DEFAULT_SIZE [HIGH]
- Cell 147: Environment variable required: IMAGE_OUTPUT_FORMAT [HIGH]
- Cell 147: Environment variable required: APIM_GATEWAY_URL [HIGH]
- Cell 147: Environment variable required: VISION_MODEL [HIGH]
- Cell 147: Environment variable required: DALL_E_DEPLOYMENT [HIGH]
- Cell 147: Environment variable required: OPENAI_CHAT_API_VERSION [HIGH]
- Cell 147: Environment variable required: USE_JWT_FOR_IMAGE [HIGH]
- Cell 147: Environment variable required: OPENAI_IMAGE_API_VERSION [HIGH]
- Cell 149: Environment variable required: OPENAI_RESOURCE_NAME [HIGH]

## Network

- Cell 17: HTTP/API requests detected [MEDIUM]
- Cell 37: HTTP/API requests detected [MEDIUM]
- Cell 43: HTTP/API requests detected [MEDIUM]
- Cell 45: HTTP/API requests detected [MEDIUM]
- Cell 55: HTTP/API requests detected [MEDIUM]
- Cell 56: HTTP/API requests detected [MEDIUM]
- Cell 57: HTTP/API requests detected [MEDIUM]
- Cell 58: HTTP/API requests detected [MEDIUM]
- Cell 108: HTTP/API requests detected [MEDIUM]
- Cell 113: HTTP/API requests detected [MEDIUM]
- Cell 115: HTTP/API requests detected [MEDIUM]
- Cell 123: HTTP/API requests detected [MEDIUM]
- Cell 125: HTTP/API requests detected [MEDIUM]
- Cell 147: HTTP/API requests detected [MEDIUM]

## File Io

- Cell 10: File I/O operations detected [LOW]
- Cell 22: File I/O operations detected [LOW]
- Cell 27: File I/O operations detected [LOW]
- Cell 29: File I/O operations detected [LOW]
- Cell 31: File I/O operations detected [LOW]
- Cell 80: File I/O operations detected [LOW]
- Cell 83: File I/O operations detected [LOW]
- Cell 115: File I/O operations detected [LOW]
- Cell 123: File I/O operations detected [LOW]
- Cell 146: File I/O operations detected [LOW]
- Cell 148: File I/O operations detected [LOW]

## Performance

- Cell 5: Potentially long-running operation [MEDIUM]
- Cell 12: Potentially long-running operation [MEDIUM]
- Cell 27: Potentially long-running operation [MEDIUM]
- Cell 45: Potentially long-running operation [MEDIUM]
- Cell 55: Potentially long-running operation [MEDIUM]
- Cell 56: Potentially long-running operation [MEDIUM]
- Cell 57: Potentially long-running operation [MEDIUM]
- Cell 58: Potentially long-running operation [MEDIUM]
- Cell 108: Potentially long-running operation [MEDIUM]
- Cell 129: Potentially long-running operation [MEDIUM]
- Cell 131: Potentially long-running operation [MEDIUM]

## Deprecation

- Cell 45: Some collections imports moved to collections.abc [LOW]
- Cell 47: Some collections imports moved to collections.abc [LOW]

# Recommendations for Successful Execution

## Pre-execution Checklist

- [ ] Install all required Python packages
- [ ] Set all required environment variables
- [ ] Configure Azure credentials (az login)
- [ ] Verify network connectivity
- [ ] Create required directories and files
- [ ] Verify API keys and tokens

## Execution Strategy

1. **Environment Setup Phase**
   - Create .env file with all required variables
   - Install dependencies: `pip install -r requirements.txt`
   - Authenticate to Azure: `az login`

2. **Configuration Validation Phase**
   - Run cells 1-10 to validate imports
   - Verify environment variables are loaded
   - Test Azure connectivity

3. **Incremental Execution Phase**
   - Execute cells in small batches
   - Monitor for errors after each batch
   - Document any manual interventions needed

4. **Error Recovery Strategy**
   - For missing packages: Install and restart kernel
   - For API errors: Verify credentials and retry
   - For timeout errors: Increase timeout or optimize

---

*Report generated: 2025-11-17T01:27:05.898298*
*Analysis type: Static code analysis without execution*
*Next step: Execute notebook with monitoring to capture runtime issues*
