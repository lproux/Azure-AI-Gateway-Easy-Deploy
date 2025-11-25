# Python 3.11 Setup Instructions

The installer has been downloaded to:
`C:\Users\lproux\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab\python-3.11.9-amd64.exe`

## Option 1: Manual Install (RECOMMENDED - 2 minutes)

1. **Open File Explorer** and navigate to:
   ```
   C:\Users\lproux\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab\
   ```

2. **Double-click** `python-3.11.9-amd64.exe`

3. **IMPORTANT**: Check these boxes:
   - ✅ "Add python.exe to PATH"
   - ✅ "Install for all users" (optional)

4. Click **"Install Now"**

5. Wait ~2 minutes for installation

## Option 2: Use Existing Python (if you have 3.11)

Run this in PowerShell to check:
```powershell
py -3.11 --version
```

If you see "Python 3.11.x", you already have it!

## After Python 3.11 is installed:

Open PowerShell in the project directory and run:

```powershell
cd C:\Users\lproux\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab

# Create venv with Python 3.11
py -3.11 -m venv .venv-py311

# Activate it
.\.venv-py311\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt

# Verify autogen works
python -c "import autogen; print('SUCCESS:', autogen.__file__)"
```

## Then in VS Code:

1. Press `Ctrl+Shift+P`
2. Type: "Python: Select Interpreter"
3. Choose: `.venv-py311\Scripts\python.exe`
4. Restart Kernel
5. Run your notebook!

