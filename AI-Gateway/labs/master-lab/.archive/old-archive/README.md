# Archive Directory

This directory contains historical files from the master-lab development process.

**Archived:** 2025-10-30
**Purpose:** Preserve development history while keeping active directory clean

---

## Contents

### backups/ (20+ files)
Notebook backups and configuration file backups:
- `master-ai-gateway-backup-*.ipynb` - Timestamped notebook backups
- `master-ai-gateway.ipynb.backup-*` - Development checkpoints
- `master-ai-gateway.ipynb.bkp-*` - Dated backups
- `master-ai-gateway.ipynb.pre-test-backup.*` - Pre-test snapshots
- `master-ai-gateway-executed.ipynb` - Executed version
- `master-ai-gateway-modified.ipynb` - Modified version
- `master-cleanup.ipynb` - Old cleanup notebook
- `legacy-env-bridge` - Old .env file (replaced by master-lab.env)
- `master-lab.env.backup*` - Environment file history
- `notebook_mcp_helpers.py.backup*` - Helper code history

**Use Case:** Recover previous notebook state, compare changes over time

### documentation/ (50+ markdown files)
Historical documentation and reports:
- `CLEANUP_AND_REORGANIZATION_COMPLETE.md` - Previous cleanup documentation
- Cell fix reports (CELL_*_FIX_REPORT.md)
- Deployment guides (DEPLOYMENT_*.md)
- MCP server documentation (MCP_*.md)
- Test results and summaries
- Planning documents
- Quick start guides

**Use Case:** Reference previous fixes, understand development history

### scripts/ (130+ files)
Development scripts and deployment files:
- **Python scripts (80+):** Fix scripts, build scripts, test automation
  - `add_sp_creation_cell.py`
  - `analyze_*.py`
  - `fix_*.py`
  - `deploy_*.py`
  - `test_*.py`
  - `refactor_*.py`
  - And 70+ more

- **Shell scripts (10+):** Deployment and automation
  - `create_service_principal.sh`
  - `fix_mcp_ports.sh`
  - `deploy_*.sh`
  - PowerShell scripts (*.ps1)

- **Deployment templates (15+):** Bicep and JSON
  - `deploy-01-core.bicep/json`
  - `deploy-02-ai-foundry.bicep/json`
  - `deploy-03-supporting.bicep/json`
  - `deploy-04-mcp.bicep/json`
  - `master-deployment.bicep/json`
  - Parameter files (params*.json)

- **Output files (20+):** JSON, TXT, CSV, LOG
  - Step output files (step*-outputs.json)
  - Execution logs (*.log, *.txt)
  - Deployment records (*.csv)

**Use Case:** Reuse automation logic, understand build process, reference deployment templates

### test_* (7 directories)
Test build directories for MCP servers:
- `test_weather_build/`
- `test_oncall_build/`
- `test_spotify_build/`
- `test_github_build/`
- `test_product_catalog_build/`
- `test_place_order_build/`
- `test_results/`

**Use Case:** Reference test builds, understand MCP server setup

### Other
- `__pycache__/` - Python bytecode cache

---

## Why Files Were Archived

These files served important purposes during development but are not needed for running the notebook:

1. **Backups** - Created during iterative fixes and enhancements
2. **Documentation** - Interim reports superseded by final documentation
3. **Scripts** - One-time fix/build scripts that already ran successfully
4. **Tests** - Build verification that has been completed
5. **Outputs** - Deployment results now captured in master-lab.env

---

## Active Files (In Parent Directory)

The current working files are:
- `master-ai-gateway.ipynb` - Main notebook
- `master-lab.env` - Environment configuration
- `notebook_mcp_helpers.py` - Helper functions
- `.azure-credentials.env` - Azure credentials
- `.mcp-servers-config` - MCP configuration
- `policies/*.xml` - APIM policies
- `README.md` - Documentation

---

## Recovery

To restore any archived file:

```bash
# Example: Restore a backup notebook
cp archive/backups/master-ai-gateway-backup-20251030-002625.ipynb ./

# Example: Reuse a fix script
cp archive/scripts/fix_cell_50.py ./
python fix_cell_50.py

# Example: Reference old documentation
cat archive/documentation/CLEANUP_AND_REORGANIZATION_COMPLETE.md
```

---

## Cleanup Policy

**Archive = Preserve, Not Delete**

All files were moved to archive (not deleted) to:
- Preserve development history
- Enable recovery if needed
- Document the evolution of the project
- Provide reference for future work

**Safe to Delete?**

If you need to save space, you can delete:
1. `test_*/` directories (can rebuild if needed)
2. `__pycache__/` (Python cache, regenerates automatically)
3. Older backups in `backups/` (keep most recent 2-3)

**Do NOT Delete:**
1. `documentation/CLEANUP_AND_REORGANIZATION_COMPLETE.md` (important history)
2. Latest backup in `backups/`
3. `scripts/` (valuable automation reference)

---

**Archive Size:** 16 MB
**Archive Files:** 202 files
**Organized:** 2025-10-30
