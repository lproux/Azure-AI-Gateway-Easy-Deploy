# Notebook Refactoring Checklist

Quick reference for implementing notebook simplifications.

---

## Pre-Refactoring Safety

- [ ] Create backup: `master-ai-gateway-REORGANIZED.backup.ipynb`
- [ ] Create git branch: `git checkout -b refactor/notebook-simplification`
- [ ] Document current notebook hash/state
- [ ] Test that current notebook runs successfully end-to-end

---

## Phase 1: Low-Risk Cleanup (1-2 hours)

### Remove Obsolete Cell Reference Comments

- [ ] Cell 11: Remove "Load BICEP_DIR (set by Cell 3)"
- [ ] Cell 46: Remove "DefaultAzureCredential already imported earlier (cell 22)"
- [ ] Cell 46: Remove "see policy cell 59" reference
- [ ] Cell 78: Remove "see dual auth ce..." reference
- [ ] Cell 81: Update "Require Cell 5" → "Requires: az_cli global variable"
- [ ] Cell 86: Remove "initialized in Cell 9 via MCPClient()" reference
- [ ] Cell 100: Remove "Use globally initialized MCP client from Cell 9"
- [ ] Cell 116: Update all 4 cell references (lines referencing cells 5 and 9)
- [ ] Cell 121: Update all 2 cell references (lines referencing cell 5)
- [ ] Cell 170: Remove "Cell 99" reference
- [ ] Cell 228: Update all 4 cell references (lines referencing cells 5 and 9)
- [ ] Cell 241: Update "Require Cell 5" reference

**Pattern to replace:**
- "Require Cell X" → "Requires: <variable_name> (from <section_name>)"
- "see cell X" → Remove or describe what to see
- "From cell X" → Remove completely

### Remove Commented-Out Code

- [ ] Cell 11: Review 4 comment blocks (12 lines) - remove if obsolete
- [ ] Cell 24: Review 2 comment blocks (6 lines) - remove if obsolete
- [ ] Cell 41: Review 1 comment block (3 lines) - remove if obsolete
- [ ] Cell 55: Review 1 comment block (4 lines) - remove if obsolete
- [ ] Cell 109: Review 1 comment block (4 lines) - remove if obsolete
- [ ] Cell 214: Review 1 comment block (3 lines) - remove if obsolete
- [ ] Cell 217: Review 1 comment block (3 lines) - remove if obsolete

### Fix Section Headers

- [ ] Remove duplicate "Section 1" marker at cell 4
- [ ] Remove duplicate "Section 4" marker at cell 69
- [ ] Remove duplicate "Section 1" marker at cell 85
- [ ] Remove duplicate "Section 2" marker at cell 112
- [ ] Remove duplicate "Section 3" marker at cell 113
- [ ] Remove duplicate "Section 2" marker at cell 118
- [ ] Ensure consistent header format: `## Section X: Name`

### Test Phase 1
- [ ] Run notebook in clean kernel
- [ ] Verify all cells execute without errors
- [ ] Compare outputs with backup notebook
- [ ] Commit changes: `git commit -m "Phase 1: Remove obsolete comments and clean section headers"`

---

## Phase 2: Import Consolidation (3-4 hours)

### Update Cell 38 (Consolidated Imports)

Replace current content with comprehensive imports:

```python
# =============================================================================
# CONSOLIDATED IMPORTS - Run this cell before any lab cells
# =============================================================================

# Standard library
import os
import sys
import json
import asyncio
import subprocess
import tempfile
import shutil
import time
import re
import ast
import traceback
import base64
import io
from pathlib import Path
from typing import Optional, Dict, List
from collections import Counter
from io import BytesIO
import uuid
import concurrent.futures

# Data & visualization
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch

# HTTP & networking
import requests
import httpx

# Azure Core
from azure.identity import DefaultAzureCredential, ClientSecretCredential, AzureCliCredential, get_bearer_token_provider
from azure.core.credentials import AzureKeyCredential

# Azure Management
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import Account, Sku as CogSku, Deployment, DeploymentModel, DeploymentProperties

# Azure AI
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage

# Azure Data
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError
from azure.search.documents.indexes.models import SearchIndex, SearchField

# OpenAI
from openai import AzureOpenAI, AuthenticationError, NotFoundError

# MCP (Model Context Protocol)
from mcp import ClientSession, McpError
from mcp.client.streamable_http import streamablehttp_client

# Additional libraries
from IPython.display import display
import nest_asyncio
import redis.asyncio as redis
from dotenv import load_dotenv
import PIL.Image as Image

# Apply nest_asyncio for Jupyter compatibility
nest_asyncio.apply()

print("✓ All imports loaded successfully")
```

- [ ] Update cell 38 with comprehensive imports

### Remove Duplicate Imports from Cells

**High-priority cells** (remove standard library and Azure imports):

- [ ] Cell 41: Remove `requests`, `DefaultAzureCredential`
- [ ] Cell 47: Remove `requests`, `DefaultAzureCredential`
- [ ] Cell 49: Remove `Counter`
- [ ] Cell 51: Remove `matplotlib.pyplot`, `pandas`, `Counter`, `Patch`
- [ ] Cell 59: Remove `requests`, `os` (⚠️ Not in Access Control, but nearby)
- [ ] Cell 76: Remove `AuthenticationError`
- [ ] Cell 78: Remove `os`, `AuthenticationError`
- [ ] Cell 82: Remove all 4 Azure imports
- [ ] Cell 111: Remove `redis.asyncio`
- [ ] Cell 116: Remove `os`, `subprocess`, `shutil`, `time`, `tempfile`
- [ ] Cell 117: Remove `os`, `requests`, `json`
- [ ] Cell 119: Remove `os`, `base64`, `json`, `requests`, `Optional`, `display`, `matplotlib.pyplot`
- [ ] Cell 121: Remove `os`, `re`, `json`, `subprocess`, `shutil`, `pathlib`
- [ ] Cell 123: Remove `os`, `requests`, `textwrap`, `json`
- [ ] Cell 136: Remove `concurrent.futures`
- [ ] Cell 144: Remove `redis.asyncio`
- [ ] Cell 176: Remove `time`
- [ ] Cell 182: Keep (specific Azure Cosmos imports may not be in main)
- [ ] Cell 184: Keep (specific Azure Search imports may not be in main)
- [ ] Cell 193: Remove `json`, `requests`, `time`, `os`
- [ ] Cell 195: Remove `os`, `DefaultAzureCredential`, `get_bearer_token_provider`
- [ ] Cell 197: Remove `pandas`
- [ ] Cell 202: Remove `os`, `pathlib`
- [ ] Cell 204: Remove `os`, `json`, `time`, `requests`, `Optional`
- [ ] Cell 205: Remove `base64`, `math` (math not in consolidated, check if needed)
- [ ] Cell 229: Remove `requests`
- [ ] Cell 230: Remove `requests`
- [ ] Cell 235: Remove `pandas`, `pathlib`, `json`, `traceback`
- [ ] Cell 242: Remove `os`, `pathlib`
- [ ] Cell 243: Remove `requests`, `json`

**MCP cells** (keep specialized imports, remove common ones):

- [ ] Cell 86: Remove `os`, `sys`, `asyncio`, `json`, `pathlib`; keep MCP helpers
- [ ] Cell 88-106: Remove `os`, `json`, `ast`, `traceback`; keep MCP helpers
- [ ] Cell 214-217: Remove `json`, `asyncio`, `time`; keep specialized MCP imports

**Note:** Cells 60-66 are in Access Control section - DO NOT MODIFY

### Test Phase 2
- [ ] Restart kernel and run cell 38 first
- [ ] Run all subsequent cells
- [ ] Verify no import errors
- [ ] Check that all functionality works
- [ ] Commit changes: `git commit -m "Phase 2: Consolidate imports to single cell"`

---

## Phase 3: Function Deduplication (4-6 hours)

### Create Deployment Utilities Cell

Insert new cell after cell 2:

```python
# =============================================================================
# DEPLOYMENT UTILITIES
# Reusable functions for Azure resource deployment
# =============================================================================

from pathlib import Path
from azure.mgmt.resource import ResourceManagementClient
import subprocess
import json
import time

def check_resource_group_exists(resource_client: ResourceManagementClient, rg_name: str) -> bool:
    """Check if a resource group exists."""
    try:
        resource_client.resource_groups.get(rg_name)
        return True
    except Exception:
        return False

def compile_bicep(bicep_path: Path) -> Path:
    """Compile Bicep template to ARM JSON."""
    json_path = bicep_path.with_suffix('.json')
    result = subprocess.run(
        ['az', 'bicep', 'build', '--file', str(bicep_path), '--outfile', str(json_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Bicep compilation failed: {result.stderr}")
    return json_path

def check_deployment_exists(resource_client: ResourceManagementClient, rg_name: str, deployment_name: str) -> bool:
    """Check if a deployment exists in a resource group."""
    try:
        resource_client.deployments.get(rg_name, deployment_name)
        return True
    except Exception:
        return False

def deploy_template(resource_client: ResourceManagementClient, rg_name: str, deployment_name: str, template: dict, parameters: dict) -> dict:
    """Deploy an ARM template to a resource group."""
    deployment_properties = {
        'mode': 'Incremental',
        'template': template,
        'parameters': parameters
    }

    deployment = resource_client.deployments.begin_create_or_update(
        rg_name,
        deployment_name,
        {'properties': deployment_properties}
    )

    return deployment.result()

def get_deployment_outputs(resource_client: ResourceManagementClient, rg_name: str, deployment_name: str) -> dict:
    """Get outputs from a completed deployment."""
    deployment = resource_client.deployments.get(rg_name, deployment_name)
    return deployment.properties.outputs if deployment.properties.outputs else {}

print("✓ Deployment utilities loaded")
```

- [ ] Insert new "Deployment Utilities" cell after cell 2
- [ ] Update cell numbering in this checklist (all subsequent cells shift by 1)

### Remove Duplicate Functions

- [ ] Cell 3 (now 4): Remove duplicate deployment functions, import from utilities
- [ ] Cell 20 (now 21): Remove `check_resource_group_exists`, use utility version
- [ ] Cell 22 (now 23): Remove all duplicate deployment functions, import from utilities
- [ ] Cell 29 (now 30): Remove duplicate `az()` function (keep version in cell 2)

### Update Function References

- [ ] Find all calls to deployment functions
- [ ] Verify they work with consolidated versions
- [ ] Test deployment workflow end-to-end

### Test Phase 3
- [ ] Restart kernel
- [ ] Run cells in order: imports → utilities → deployment
- [ ] Verify all deployment functions work
- [ ] Test at least one full deployment cycle
- [ ] Commit changes: `git commit -m "Phase 3: Consolidate duplicate functions"`

---

## Final Validation

### Comprehensive Testing

- [ ] Restart kernel and clear all outputs
- [ ] Run entire notebook from top to bottom
- [ ] Verify all 25 labs still function correctly
- [ ] Check Access Control section (cells 60-66 in original, may shift) works perfectly
- [ ] Compare execution results with backup notebook

### Documentation

- [ ] Update any README files with new cell organization
- [ ] Document the consolidated import cell requirement
- [ ] Note any breaking changes (should be none)

### Git Workflow

- [ ] Review all changes: `git diff main`
- [ ] Ensure Access Control cells untouched
- [ ] Create pull request with summary of changes
- [ ] Request review from notebook owner
- [ ] Merge to main after approval

---

## Phase 4: Future Improvements (Optional)

### Helper Function Library

- [ ] Create `call_apim_endpoint()` helper for common API patterns
- [ ] Consolidate credential creation patterns
- [ ] Create config dictionary for environment variables

### Structural Reorganization

- [ ] Group labs by category
- [ ] Add comprehensive table of contents
- [ ] Create "Utilities & Helpers" section
- [ ] Separate test cells from lab cells

### Documentation

- [ ] Add detailed comments to complex sections
- [ ] Create architecture diagrams
- [ ] Document dependencies between cells
- [ ] Add troubleshooting section

---

## Rollback Plan

If issues occur during refactoring:

1. **Immediate rollback:**
   ```bash
   git checkout master-ai-gateway-REORGANIZED.ipynb
   ```

2. **Partial rollback:**
   ```bash
   git checkout HEAD~1 master-ai-gateway-REORGANIZED.ipynb  # Go back 1 commit
   ```

3. **From backup:**
   ```bash
   cp master-ai-gateway-REORGANIZED.backup.ipynb master-ai-gateway-REORGANIZED.ipynb
   ```

---

## Success Metrics

After completion, verify:

- [ ] Total cells reduced by ~10-15
- [ ] Zero duplicate imports
- [ ] Zero duplicate functions
- [ ] All cell reference comments removed
- [ ] All section headers standardized
- [ ] Notebook executes successfully start to finish
- [ ] All 25 labs pass their tests
- [ ] Access Control section (Lab 06) works perfectly

---

## Notes

- **Access Control cells to preserve:** Originally cells 56-66 (will shift if cells added/removed before them)
- **Always test after each phase** before proceeding to next
- **Keep backup** until thoroughly validated
- **Document any issues** encountered for future reference

---

**Last Updated:** 2025-11-13
**Notebook Version:** master-ai-gateway-REORGANIZED.ipynb (248 cells)
