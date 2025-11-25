# Python Installation Locations

## System-Wide Python Installations

### 1. Python 3.11.9 (For AutoGen)
```
Windows Path:  C:\Python311\python.exe
WSL Path:      /mnt/c/Python311/python.exe
Added to PATH: Yes
```

**Use for:**
- Creating new venvs with Python 3.11
- Running Python 3.11 scripts directly

### 2. Python 3.12.8 (For Future Use)
```
Windows Path:  C:\Python312\python.exe
WSL Path:      /mnt/c/Python312/python.exe
Added to PATH: Yes
```

**Use for:**
- Creating venvs with Python 3.12
- Future projects requiring Python 3.12

---

## Virtual Environments (Project-Specific)

### 3. .venv-py311 (NEW - Active for Notebook)
```
Location:      C:\Users\lproux\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab\.venv-py311
Python:        .venv-py311\Scripts\python.exe
Version:       3.11.9
AutoGen:       0.2.35 ✓
Status:        ACTIVE - Use this for your notebook!
```

**This is your working environment with:**
- ✓ AutoGen 0.2.35
- ✓ All requirements.txt packages
- ✓ Jupyter kernel registered
- ✓ VS Code default

### 4. .venv (ORIGINAL - Python 3.13)
```
Location:      C:\Users\lproux\Documents\GitHub\MCP-servers-internalMSFT-and-external\.venv
Python:        .venv\Scripts\python.exe
Version:       3.13.9
Status:        Keep for other projects
```

---

## Quick Access Commands

### From PowerShell:
```powershell
# Python 3.11 (system)
C:\Python311\python.exe --version

# Python 3.12 (system)
C:\Python312\python.exe --version

# Activate notebook environment
.\activate-py311.ps1
```

### From WSL:
```bash
# Python 3.11 (system)
/mnt/c/Python311/python.exe --version

# Python 3.12 (system)
/mnt/c/Python312/python.exe --version

# Notebook venv
.venv-py311/Scripts/python.exe --version
```

---

## Summary

**For your notebook, use:** `.venv-py311` 
- Already configured in VS Code
- Has AutoGen 0.2.35 working
- Jupyter kernel: "Python 3.11 (AutoGen)"

**System Python locations:**
- Python 3.11: `C:\Python311`
- Python 3.12: `C:\Python312`
