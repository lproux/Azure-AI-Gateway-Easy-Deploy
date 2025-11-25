# Master AI Gateway Lab - Dev Container

This dev container provides a complete, cross-platform development environment for the Master AI Gateway Lab notebook.

## Features

### Base Environment
- **Python 3.11** (Debian Bullseye)
- **Node.js 20** for MCP tooling
- **Git** with GitHub CLI
- **Docker-in-Docker** for container builds
- **Azure CLI** with Bicep support

### Python Packages (from requirements.txt)
- **Azure SDKs**: Identity, Key Vault, Storage, Resource Management, API Management, Cognitive Services
- **Azure AI & OpenAI**: OpenAI SDK, Azure AI Inference
- **Model Context Protocol (MCP)**: MCP SDK, httpx
- **Agent Frameworks**: Microsoft Agent Framework, Semantic Kernel, AutoGen
- **Data Analysis**: pandas, openpyxl, matplotlib, Pillow
- **Web & API**: requests, httpx, FastAPI, uvicorn
- **Authentication**: PyJWT, cryptography, MSAL
- **Jupyter**: IPython, ipykernel, jupyter, nbconvert
- **Development Tools**: pytest, black, isort, pylint, mypy

### VS Code Extensions
- **Jupyter**: Full notebook support with renderers and slideshows
- **Python**: Pylance, Black formatter, isort, pylint
- **Azure**: Resource Groups, Functions, Bicep, CLI, API Management
- **AI**: GitHub Copilot, Copilot Chat
- **API Development**: REST Client, OpenAPI
- **Data**: Rainbow CSV, Excel Viewer
- **Markdown**: All-in-one, linter, Mermaid diagrams
- **Git**: GitLens, Pull Request Manager
- **General**: EditorConfig, Error Lens, Path Intellisense, IntelliCode

### Azure CLI Extensions
- Application Insights
- Front Door
- API Center

### NPM Global Packages
- `@modelcontextprotocol/inspector` - MCP server testing
- `prettier` - Code formatting

## Configuration

### VS Code Settings
- Python interpreter: `/usr/local/bin/python`
- Line length: 100 characters
- Format on save: Enabled
- Auto-organize imports: Enabled
- Jupyter line numbers: On
- Type checking: Basic

### Mounted Directories
- `~/.azure` - Azure CLI credentials (read-only)
- `~/.ssh` - SSH keys (read-only)

### Forwarded Ports
- **8000** - MCP HTTP Server
- **8080** - Alternative HTTP
- **8888** - Jupyter Server
- **3000** - Development Server

### System Requirements
- **CPUs**: 4 cores minimum
- **Memory**: 8 GB minimum
- **Storage**: 32 GB minimum

## Usage

### Opening in Dev Container

#### VS Code
1. Install **Remote - Containers** extension
2. Open folder in VS Code
3. Click "Reopen in Container" when prompted
4. Wait for container build and post-create script

#### GitHub Codespaces
1. Click "Code" → "Codespaces" → "New codespace"
2. Wait for container creation
3. Notebook and README will open automatically

### First-Time Setup

After container creation, the post-create script automatically:
1. Updates system packages
2. Installs system dependencies (jq, curl, etc.)
3. Installs all Python packages from requirements.txt
4. Installs MCP Inspector and prettier via npm
5. Adds Azure CLI extensions
6. Configures GitHub CLI
7. Creates workspace directories
8. Sets up shell aliases
9. Creates workspace README

### Quick Start

```bash
# Navigate to lab
lab

# Login to Azure
azlogin

# Open notebook
notebook

# Or start Jupyter server
nb
```

### Available Commands

#### Navigation
- `lab` - Go to lab directory
- `ws` - Go to workspace directory
- `policies` - Go to policies directory
- `ll` - List files (detailed)

#### Azure
- `azlogin` - Login with device code
- `azaccount` - Show current account
- `azgroups` - List resource groups
- `azregions` - List Azure regions
- `azapim` - List APIM instances

#### Jupyter
- `nb` - Start Jupyter server (0.0.0.0:8888)
- `notebook` - Open master-ai-gateway.ipynb in VS Code

#### Git
- `gs` - git status
- `gd` - git diff
- `gl` - git log (pretty)
- `ga` - git add
- `gc` - git commit -m
- `gp` - git push

#### Python
- `venv` - Activate virtual environment
- `mkvenv` - Create new venv and activate

#### MCP Development
- `mcprun` - Run MCP HTTP server (uvicorn)
- `mcpinspect` - Launch MCP Inspector
- `mcptest` - Run pytest

#### Policy Management
- `policies` - Navigate to policies directory
- `policyls` - List policy files

#### Quick Access
- `readme` - Open README.md
- `report` - Open COMPREHENSIVE-TEST-REPORT.md

## Workspace Structure

```
~/lab-workspace/
├── README.md           # Workspace documentation
├── policies/           # APIM policy XML files
├── config/             # Configuration files (.env, settings)
└── data/               # Data files (Excel, CSV, etc.)
```

## Cross-Platform Support

This dev container is designed to work seamlessly across:
- **Windows** (with WSL2)
- **macOS**
- **Linux**
- **GitHub Codespaces**

Azure credentials are mounted from the host system (read-only), so you can authenticate once on your host machine and use those credentials in the container.

## Troubleshooting

### Container Build Issues
- Ensure Docker is running
- Check available disk space (need 32 GB minimum)
- Try rebuilding: Command Palette → "Remote-Containers: Rebuild Container"

### Python Package Issues
- Re-run post-create script: `bash .devcontainer/post-create.sh`
- Manually install requirements: `pip install -r requirements.txt`

### Azure CLI Authentication
- Login from container: `azlogin`
- Or mount credentials from host (automatic with mounts config)

### Jupyter Issues
- Restart kernel: Command Palette → "Jupyter: Restart Kernel"
- Check Python interpreter: Should be `/usr/local/bin/python`

## Files Created

This dev container configuration includes:
- `devcontainer.json` - Main configuration
- `post-create.sh` - Setup script
- `README.md` - This file
- `../requirements.txt` - Python dependencies

## Notebook Information

**File**: `master-ai-gateway.ipynb`
**Total Cells**: 205
**Test Status**: ✅ All tests passed (100% success rate)

### Sections
1. **Section 0**: Deployment & Configuration (168 cells)
2. **Section 6**: Agent Frameworks (10 cells)
3. **Section 7**: OAuth & Authorization (8 cells)
4. **Section 2**: Sales Analysis with MCP (9 cells)
5. **Lab 25**: Secure Responses API (7 cells)
6. **Consolidated Policy Lab** (3 cells)

## Support

For issues or questions:
- Check `COMPREHENSIVE-TEST-REPORT.md` for test results
- Review workspace README: `~/lab-workspace/README.md`
- Consult main notebook documentation

## Version Information

- **Python**: 3.11
- **Node.js**: 20
- **Azure CLI**: Latest
- **Git**: Latest
- **Docker**: Latest (in-docker)

Last Updated: 2025-11-09
