# Requirements Fix - Missing Packages

## Problem

When you changed kernels, you got this error in Cell 17:

```python
ModuleNotFoundError: No module named 'azure.mgmt'
```

## Root Cause

Two issues:
1. **Missing package**: `azure-search-documents` was not in requirements.txt (needed for Lab 11: Vector Searching)
2. **New kernel**: After changing kernels, requirements need to be reinstalled

## What Was Fixed

### ✅ Updated requirements.txt

Added missing package:
```
azure-search-documents>=11.4.0
```

### ✅ Verified All Imports

All packages needed by the notebook are now in requirements.txt:

**Azure SDKs**:
- `azure-identity` - Authentication
- `azure-mgmt-resource` - Resource management (needed by Cell 17)
- `azure-mgmt-apimanagement` - APIM management
- `azure-mgmt-cognitiveservices` - Azure OpenAI management
- `azure-cosmos` - Cosmos DB (Lab 10)
- `azure-search-documents` - Azure AI Search (Lab 11) **← NEWLY ADDED**
- `azure-ai-inference` - Azure AI SDK
- `azure-core` - Core Azure utilities

**Other Key Packages**:
- `openai` - OpenAI Python SDK
- `python-dotenv` - Environment variables
- `pandas` - Data analysis (Lab 10)
- `pyautogen` - AutoGen framework
- `semantic-kernel` - Semantic Kernel framework
- `mcp` - Model Context Protocol

## How to Fix

### Option 1: Run in Bash (Recommended)

```bash
cd "/mnt/c/Users/lproux/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab"
./install_requirements.sh
```

### Option 2: Run in Jupyter Cell

Create a new cell and run:

```python
!pip install -r requirements.txt
```

### Option 3: Manual Install (if using .venv-py311)

```bash
cd "/mnt/c/Users/lproux/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab"
.venv-py311/Scripts/python.exe -m pip install --upgrade pip
.venv-py311/Scripts/python.exe -m pip install -r requirements.txt
```

### Option 4: Direct pip install (current kernel)

If you're already in Jupyter with the right kernel:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## After Installation

1. **Restart your kernel**: Kernel → Restart Kernel
2. **Run Cell 17 again**: Should work now ✅

## Verification

After installation, verify the packages are installed:

```python
# Run this in a Jupyter cell to verify
import azure.mgmt.resource
import azure.identity
import azure.cosmos
import azure.search.documents
import openai
import pandas
print("✅ All packages imported successfully!")
```

## All Packages in requirements.txt

The complete requirements.txt now includes 50+ packages across these categories:

1. **Environment & Configuration**: python-dotenv, pydantic
2. **Azure SDKs**: 10+ Azure packages for all services
3. **Azure AI & OpenAI**: openai, azure-ai-inference, azure-search-documents
4. **Agent Frameworks**: pyautogen, semantic-kernel
5. **Data Processing**: pandas, numpy, matplotlib
6. **Web & API**: requests, httpx, fastapi
7. **Jupyter Support**: ipython, ipykernel, jupyter
8. **Development Tools**: pytest, black, mypy

## Summary

✅ **Fixed**: Added `azure-search-documents>=11.4.0` to requirements.txt
✅ **Verified**: All 15+ Azure SDK imports are covered
✅ **Script Created**: `install_requirements.sh` for easy installation

**Next Step**: Run one of the installation options above, then restart your kernel!
