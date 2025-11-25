# MCP Server Port Fix Guide

## 🎯 Problem Identified

**Root Cause:** Port mismatch in Container Apps configuration

```
Expected: TargetPort 8080
Actual:   Containers listen on port 80
Result:   "Degraded - 0/1 replicas ready"
```

---

## ✅ RECOMMENDED SOLUTION: Fix Port Configuration

**Time:** ~2 minutes (much faster than delete/recreate)

**What it does:** Updates ingress configuration from port 8080 → 80

---

## 🚀 Choose Your Method

### Option 1: CLI Script (Fastest)

**Bash (Linux/WSL):**
```bash
cd "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab"
./fix_mcp_ports.sh
```

**Python (Cross-platform):**
```bash
python3 fix_mcp_ports.py
```

---

### Option 2: From Jupyter Notebook (Best for reproducibility)

**Add a new cell and paste this:**

```python
%run notebook_cell_fix_mcp_ports.py
```

Or manually copy the content from `notebook_cell_fix_mcp_ports.py` into a new cell.

**Benefits:**
- ✅ Runs directly in notebook
- ✅ Auto-waits 60 seconds for replicas
- ✅ Auto-tests connectivity afterward
- ✅ Shows progress in real-time

---

### Option 3: Manual CLI (Individual servers)

**Fix one server at a time:**

```bash
# Fix Weather server
az containerapp ingress update \
  --name mcp-weather-pavavy6pu5 \
  --resource-group lab-master-lab \
  --target-port 80

# Fix OnCall server
az containerapp ingress update \
  --name mcp-oncall-pavavy6pu5 \
  --resource-group lab-master-lab \
  --target-port 80

# Repeat for: github, spotify, product-catalog, place-order, ms-learn
```

---

### Option 4: Azure Portal (Manual)

**For each server:**
1. Go to Azure Portal → Container Apps
2. Find: `mcp-{server}-pavavy6pu5`
3. Click: **Ingress**
4. Change: **Target port** from `8080` → `80`
5. Click: **Save**
6. Wait 30-60 seconds for new revision

**Repeat for all 7 servers** (tedious!)

---

## ⏱ After Running the Fix

### 1. Wait for Replicas (30-60 seconds)

Container Apps need time to:
- Create new revision
- Start new replicas
- Health check passes
- Route traffic

### 2. Verify Success

**Check in Portal:**
- Status should change: `Degraded` → `Running`
- Replicas: `0/1` → `1/1`

**Check via CLI:**
```bash
az containerapp show \
  --name mcp-weather-pavavy6pu5 \
  --resource-group lab-master-lab \
  --query "properties.runningStatus" \
  --output tsv
```

Expected: `Running`

### 3. Test Connectivity

```bash
python3 test_mcp_servers.py
```

**Expected output:**
```
Testing WEATHER... OK:200 (234.5ms)
Testing ONCALL... OK:200 (189.2ms)
Testing GITHUB... OK:200 (201.8ms)
Testing SPOTIFY... OK:200 (156.3ms)
Testing PRODUCT_CATALOG... OK:200 (203.7ms)
Testing PLACE_ORDER... OK:200 (198.1ms)
Testing MS_LEARN... OK:200 (211.4ms)

Total Servers: 7
  Success (200-399): 7  ✅
```

---

## ❌ Alternative: Delete & Recreate (NOT Recommended)

**Why NOT recommended:**
- ⏱ Takes 10-15 minutes (vs 2 minutes for port fix)
- 🔧 Requires redeployment
- 💾 More complex
- 🐛 Higher risk of new issues

**When to use:** Only if port fix fails multiple times

**How to do it:**
1. Check notebook for cleanup cell (usually near deployment cells)
2. Run cleanup for MCP servers only
3. Re-run deployment step 4 (MCP servers)
4. Update `master-lab.env` with new URLs

---

## 🔍 Troubleshooting

### Fix Script Fails

**Error: "Please run 'az login'"**
```bash
az login
```

**Error: "Resource not found"**
- Check resource group name: `lab-master-lab`
- Check server names have correct suffix: `pavavy6pu5`

**Error: "Unauthorized"**
- Verify your Azure account has permissions
- Try: `az account show` to confirm active subscription

### Servers Still Degraded After Fix

**Wait longer:**
```bash
# Check status
az containerapp revision list \
  --name mcp-weather-pavavy6pu5 \
  --resource-group lab-master-lab \
  --output table
```

**Check logs:**
```bash
az containerapp logs show \
  --name mcp-weather-pavavy6pu5 \
  --resource-group lab-master-lab \
  --tail 50
```

**Look for:**
- Container startup errors
- Image pull failures
- Application crashes

### Some Servers Work, Others Don't

**Run fix individually:**
```bash
# Fix only the broken ones
az containerapp ingress update \
  --name mcp-github-pavavy6pu5 \
  --resource-group lab-master-lab \
  --target-port 80
```

---

## 📊 Expected Timeline

| Step | Time | Status Check |
|------|------|--------------|
| Run fix script | 30s | Scripts completes |
| Wait for replicas | 60s | Portal shows "Running" |
| Test connectivity | 10s | All servers return 200 |
| **TOTAL** | **~2 min** | ✅ Ready to use |

---

## ✅ Success Criteria

After the fix, you should have:

1. **Azure Portal:**
   - All 7 Container Apps show: `Running`
   - All have: `1/1 replicas ready`
   - Ingress target port: `80`

2. **Connectivity Test:**
   - `test_mcp_servers.py` shows: `7/7 Success`
   - All servers return: `OK:200`

3. **Notebook Cell 2:**
   - Initializes without errors
   - Shows: `✅ HTTP 200 - Server is reachable`
   - Creates `mcp` client object

---

## 🎓 Why This Happened

**Likely causes:**
1. Bicep template had wrong port (8080 instead of 80)
2. Container images changed their listening port
3. Default port configuration wasn't updated

**The fix:** Update Container App ingress to match actual container port

**Prevention:** Always verify container listening port matches ingress target port

---

## 📞 Need Help?

**If fix doesn't work:**
1. Share error messages from fix script
2. Share Container App logs: `az containerapp logs show ...`
3. Share revision status: `az containerapp revision list ...`

**Created:** 2025-10-27
**Files:**
- `fix_mcp_ports.sh` (Bash script)
- `fix_mcp_ports.py` (Python script)
- `notebook_cell_fix_mcp_ports.py` (Notebook version)
