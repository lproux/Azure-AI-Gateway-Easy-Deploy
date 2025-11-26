# Dev Container Configuration

This directory contains the Dev Container configuration for the entire Azure AI Gateway repository. This configuration is used when opening the repository root in GitHub Codespaces or VS Code Dev Containers.

## What's Configured

### Base Environment
- **Base Image**: `mcr.microsoft.com/devcontainers/python:1-3.11-bullseye`
- **Python Version**: 3.11
- **Operating System**: Debian Bullseye

### Installed Tools

#### Azure & Cloud Tools
- **Azure CLI** (latest) with Bicep support
- **GitHub CLI** (gh)
- Azure CLI extensions:
  - application-insights
  - front-door
  - api-center

#### Development Tools
- **Node.js 20** (for MCP server development)
- **Docker-in-Docker** (for container builds)
- **Git** (latest)
- System utilities: jq, curl, wget, tree, vim

#### Python Packages
All packages from `AI-Gateway/labs/master-lab/requirements.txt` including:
- Azure SDKs (identity, mgmt-*, cosmos, search, etc.)
- OpenAI SDK
- MCP SDK
- Jupyter and notebook support
- Data science libraries (pandas, matplotlib)
- Agent frameworks (Semantic Kernel, AutoGen)

### VS Code Extensions

Automatically installed extensions:

#### Python & Jupyter
- ms-toolsai.jupyter (full suite)
- ms-python.python
- ms-python.vscode-pylance
- ms-python.black-formatter
- ms-python.isort
- ms-python.pylint

#### Azure Development
- ms-azuretools.vscode-azureresourcegroups
- ms-azuretools.vscode-azurefunctions
- ms-azuretools.vscode-bicep
- ms-vscode.azurecli
- ms-azuretools.vscode-apimanagement

#### AI & Productivity
- github.copilot
- github.copilot-chat

#### API & Data
- humao.rest-client
- 42crunch.vscode-openapi
- mechatroner.rainbow-csv
- grapecity.gc-excelviewer

#### Documentation & Git
- yzhang.markdown-all-in-one
- davidanson.vscode-markdownlint
- bierner.markdown-mermaid
- eamodio.gitlens
- github.vscode-pull-request-github

#### General Development
- editorconfig.editorconfig
- usernamehw.errorlens
- christian-kohler.path-intellisense
- visualstudioexptteam.vscodeintellicode

## Usage

### GitHub Codespaces

#### Method 1: Direct Link
Click the badge in the repository README:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lproux/Azure-AI-Gateway-Easy-Deploy?quickstart=1)

#### Method 2: GitHub UI
1. Navigate to the repository on GitHub
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main**

#### Method 3: Codespaces Dashboard
1. Go to https://github.com/codespaces
2. Click **New codespace**
3. Select this repository
4. Click **Create codespace**

**First-time setup**: ~3-5 minutes
**Subsequent starts**: ~30-60 seconds

### VS Code Dev Containers

#### Prerequisites
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Install [VS Code](https://code.visualstudio.com/)
3. Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

#### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/lproux/Azure-AI-Gateway-Easy-Deploy.git
   cd Azure-AI-Gateway-Easy-Deploy
   ```

2. Open in VS Code:
   ```bash
   code .
   ```

3. Reopen in Container:
   - VS Code will detect the `.devcontainer` configuration
   - Click **Reopen in Container** when prompted
   - Or use Command Palette (`F1`) → **Dev Containers: Reopen in Container**

**First-time build**: ~5-8 minutes
**Subsequent starts**: ~30-60 seconds

## Configuration Details

### Port Forwarding

The following ports are automatically forwarded:

| Port | Purpose | Auto-forward |
|------|---------|--------------|
| 8000 | MCP HTTP Server | notify |
| 8080 | Alternative HTTP | silent |
| 8888 | Jupyter Server | notify |
| 3000 | Development Server | silent |

### Mounted Directories

The following host directories are mounted into the container:

- `~/.azure` → `/home/vscode/.azure` (Azure CLI credentials)
- `~/.ssh` → `/home/vscode/.ssh` (SSH keys for Git)

This allows you to:
- Persist Azure authentication between container rebuilds
- Use your existing SSH keys for Git operations
- Avoid re-authenticating every time

### Resource Requirements

**Minimum:**
- 4 CPU cores
- 8GB RAM
- 32GB storage

**Recommended:**
- 8 CPU cores
- 16GB RAM
- 64GB storage

For GitHub Codespaces:
- 4-core machine: Included in free tier (60 hours/month)
- 8-core machine: Premium tier or pay-as-you-go

## Post-Create Setup

The `post-create.sh` script runs automatically after container creation and:

1. **Updates system packages** - Latest security patches
2. **Installs system dependencies** - jq, curl, tree, etc.
3. **Sets up Python environment** - Installs all packages from master-lab requirements
4. **Configures Node.js** - Installs MCP Inspector and Prettier
5. **Installs Azure CLI extensions** - Application Insights, API Center, etc.
6. **Configures workspace** - Git settings, shell aliases

### Available Aliases

After setup, you have access to convenient shell aliases:

**Navigation:**
```bash
masterlab    # cd AI-Gateway/labs/master-lab
labs         # cd AI-Gateway/labs
apim         # cd AzureOpenAI-with-APIM
ll           # ls -lah (detailed listing)
```

**Git:**
```bash
gs           # git status
gd           # git diff
gl           # git log (pretty format)
ga           # git add
gc           # git commit -m
gp           # git push
```

**Python:**
```bash
venv         # source .venv/bin/activate
mkvenv       # create and activate virtual environment
nb           # start Jupyter notebook server
```

**Azure:**
```bash
azlogin      # az login --use-device-code
azaccount    # az account show --output table
azgroups     # az group list --output table
azregions    # list all Azure regions
azapim       # az apim list --output table
```

**Quick Access:**
```bash
readme       # Open main README.md
testing      # Open TESTING.md guide
notebook     # Open easy deploy notebook (34 cells)
notebookfull # Open full notebook (152 cells)
validate     # Run setup validation script
```

## Files Opened Automatically

When the Codespace starts, these files open automatically:

1. `README.md` - Repository overview
2. `AI-Gateway/labs/master-lab/README.md` - Master Lab documentation
3. `AI-Gateway/labs/master-lab/TESTING.md` - Complete testing guide
4. `AI-Gateway/labs/master-lab/master-ai-gateway-easy-deploy.ipynb` - Main notebook

This gives you immediate access to documentation and the primary notebook.

## Customization

### Adding Extensions

Edit `.devcontainer/devcontainer.json` and add to the `extensions` array:

```json
"customizations": {
  "vscode": {
    "extensions": [
      "existing.extension",
      "your.new-extension"
    ]
  }
}
```

### Installing Additional Packages

**Python packages:**
Add to `AI-Gateway/labs/master-lab/requirements.txt` and rebuild container.

**System packages:**
Edit `post-create.sh` and add to the `apt-get install` command.

**Node.js packages:**
Edit `post-create.sh` and add to the `npm install -g` command.

### Changing Python Version

Edit `.devcontainer/devcontainer.json`:

```json
"image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye"
```

Available versions: 3.9, 3.10, 3.11, 3.12

## Troubleshooting

### Container fails to build

**Solution:**
1. Check Docker Desktop is running (local only)
2. Ensure sufficient disk space (>10GB free)
3. Try rebuilding: `Dev Containers: Rebuild Container`
4. Check logs: View → Output → Dev Containers

### Extensions not loading

**Solution:**
1. Wait for container to fully start
2. Reload window: `Developer: Reload Window`
3. Manually install: Extensions → Search → Install
4. Check extension compatibility with Linux

### Python packages missing

**Solution:**
1. Verify requirements installed:
   ```bash
   pip list | grep azure
   ```
2. Reinstall:
   ```bash
   pip install -r AI-Gateway/labs/master-lab/requirements.txt
   ```
3. Rebuild container if persistent

### Azure authentication fails

**Solution:**
1. Use device code flow:
   ```bash
   az login --use-device-code
   ```
2. Check `~/.azure` mount is working
3. Re-authenticate:
   ```bash
   az logout
   az login --use-device-code
   ```

### Port already in use

**Solution:**
1. Check running processes:
   ```bash
   lsof -i :8000  # or other port number
   ```
2. Kill process or change port in configuration
3. Restart container

## Lab-Specific Configurations

### Master Lab
The master lab has its own `.devcontainer` configuration at:
`AI-Gateway/labs/master-lab/.devcontainer/`

This configuration is more specific and optimized for running the master lab notebook.

**To use Master Lab config:**
1. Navigate to `AI-Gateway/labs/master-lab`
2. Open this folder in VS Code (not the root)
3. Reopen in Container

**Key differences:**
- Opens master lab notebook by default
- Installs only master lab requirements
- Optimized aliases for lab workflow
- Workspace configuration specific to lab

### Choosing Between Configs

**Use Root Config** (this one) when:
- Exploring multiple labs
- Working across AI-Gateway and AzureOpenAI-with-APIM
- Developing new labs or contributing
- Need full repository context

**Use Master Lab Config** when:
- Focused on running master-ai-gateway-easy-deploy.ipynb
- Want minimal, optimized environment
- Learning the labs sequentially
- Following TESTING.md guide

Both configurations install the same tools and packages, but have different:
- Default workspace folders
- Auto-opened files
- Shell aliases
- Focus and optimization

## Environment Variables

The container respects these environment variables:

### Azure
- `AZURE_SUBSCRIPTION_ID` - Default subscription
- `AZURE_TENANT_ID` - Azure AD tenant
- `AZURE_CLIENT_ID` - Service principal ID (optional)
- `AZURE_CLIENT_SECRET` - Service principal secret (optional)

### Jupyter
- `JUPYTER_PORT` - Default: 8888
- `JUPYTER_TOKEN` - Authentication token

### Python
- `PYTHONIOENCODING` - Set to UTF-8 to prevent Unicode errors

Set these in GitHub Codespaces:
1. Repository → Settings → Secrets and variables → Codespaces
2. Add New Secret/Variable

Set these in Dev Containers:
1. Create `.env` file in workspace (gitignored)
2. Add variables: `AZURE_SUBSCRIPTION_ID=xxx`

## Performance Optimization

### For GitHub Codespaces

**Faster startup:**
- Pre-build configurations (GitHub Actions)
- Use 8-core machine for large operations
- Keep Codespace running during active work

**Cost optimization:**
- Stop Codespace when not in use
- Set auto-stop timeout (Settings → 30 minutes)
- Delete unused Codespaces
- Use 4-core for development, 8-core for deployments

### For Local Dev Containers

**Faster builds:**
- Allocate more CPU/RAM to Docker (8GB+ recommended)
- Use SSD for Docker storage
- Keep frequently-used base images cached

**Disk space:**
- Regularly prune unused images: `docker system prune -a`
- Monitor disk usage: `docker system df`
- Clean up old containers and volumes

## Security Considerations

### Mounted Credentials
- `~/.azure` and `~/.ssh` are mounted read-only by default
- Credentials never leave your machine (local dev containers)
- Codespaces credentials are GitHub-managed

### Secrets Management
- Never commit secrets to Git
- Use environment variables or Azure Key Vault
- `.env` files are gitignored
- Service principals preferred over personal accounts (production)

### Network Security
- Container has outbound internet access
- Inbound access only through forwarded ports
- HTTPS enforced for Azure connections

## Additional Resources

- [Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [Complete Testing Guide](../AI-Gateway/labs/master-lab/TESTING.md)
- [Master Lab README](../AI-Gateway/labs/master-lab/README.md)
- [Repository README](../README.md)

## Support

For issues with the Dev Container configuration:
1. Check [TESTING.md](../AI-Gateway/labs/master-lab/TESTING.md) troubleshooting section
2. Verify [Docker Desktop](https://docs.docker.com/desktop/) is running (local)
3. Check [GitHub Codespaces status](https://www.githubstatus.com/)
4. Review container logs: View → Output → Dev Containers
5. [Open an issue](https://github.com/lproux/Azure-AI-Gateway-Easy-Deploy/issues)

---

**Last Updated**: 2025-11-26
**Container Version**: 1.0
**Base Image**: mcr.microsoft.com/devcontainers/python:1-3.11-bullseye
