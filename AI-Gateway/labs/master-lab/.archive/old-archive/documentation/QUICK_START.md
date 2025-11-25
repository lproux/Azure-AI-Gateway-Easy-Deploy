# 🚀 Quick Start Guide - MCP Servers

## ✅ Current Status

**2 Real MCP Servers Deployed and Healthy:**
1. Excel Analytics MCP - `http://excel-mcp-72998.eastus.azurecontainer.io:8000`
2. Research Documents MCP - `http://docs-mcp-72998.eastus.azurecontainer.io:8000`

## 📝 What Was Fixed

**Cell 2** in `master-ai-gateway.ipynb` has been updated to:
- ✅ Only initialize Excel and Docs MCP (the 2 real servers)
- ✅ Check for existing initialization to prevent duplicates
- ✅ Provide clear status messages
- ✅ Remove references to the 7 non-existent servers

## 🎯 Next Steps

### 1. Restart Your Jupyter Kernel

If you have the notebook open:
1. **Kernel** → **Restart Kernel** (or press `0 0` twice)
2. This clears the old `mcp` object from memory

### 2. Run Cell 1 (Environment Setup)

Run the first cell to load environment variables.

### 3. Run Cell 2 (MCP Initialization)

Run the updated Cell 2. You should see:

```
🔄 Initializing MCP Client...
✅ MCP Client initialized successfully!

📡 Real MCP Servers Deployed:
   1. Excel Analytics: http://excel-mcp-72998.eastus.azurecontainer.io:8000
   2. Research Documents: http://docs-mcp-72998.eastus.azurecontainer.io:8000

💡 Note: Only 2 real MCP servers are deployed from workshop.
   Other servers (weather, oncall, etc.) were placeholder images.
```

### 4. Test MCP Servers

Run a test cell to verify servers work:

```python
# Test Excel MCP
try:
    result = mcp.excel._call("health_check", {})
    print("✅ Excel MCP is working!")
except Exception as e:
    print(f"❌ Excel MCP error: {e}")

# Test Docs MCP  
try:
    result = mcp.docs._call("health_check", {})
    print("✅ Docs MCP is working!")
except Exception as e:
    print(f"❌ Docs MCP error: {e}")
```

### 5. Execute Lab Cells

- **Cells 1-25**: Infrastructure setup - should work as before
- **Cells 26+**: Lab exercises
  - Labs using Excel or Docs MCP: ✅ Should work
  - Labs using other 7 servers: ⚠️ Will need to be skipped or modified

## 🔍 Troubleshooting

### If Cell 2 Still Shows Old Errors:

1. **Close and reopen the notebook file** in VS Code/Jupyter
2. **Restart the kernel** completely
3. **Re-run Cell 1 and Cell 2**

### If Servers Don't Respond:

```bash
# Check server status
az container show --name excel-mcp-72998 --resource-group lab-master-lab

# Restart if needed
az container restart --name excel-mcp-72998 --resource-group lab-master-lab
```

## 📚 Full Documentation

- **DEPLOYMENT_SUMMARY.md** - Complete deployment details
- **MCP_SERVER_DOCUMENTATION.md** - Server capabilities and API
- **mcp-deployment-urls.txt** - Quick URL reference

---

**Everything is ready! Just restart your kernel and re-run Cells 1 & 2.** 🎉
