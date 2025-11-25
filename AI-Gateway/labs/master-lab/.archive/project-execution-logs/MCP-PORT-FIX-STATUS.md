# MCP Container Apps - Port Mismatch Fix

**Date**: 2025-11-15
**Status**: ROOT CAUSE IDENTIFIED - Fixing Port Configuration
**Issue**: Health checks failing due to port mismatch

---

## ROOT CAUSE DISCOVERED

### The Problem

**Azure Container Apps Configuration**:
- Ingress `targetPort`: 8080 (configured)
- Health Probes: None configured (using default TCP probe on port 8080)

**MCP Application Reality**:
```
Logs show: "12:24:21 Listening on :80..."
```

**Result**: Health check TCP probe tries port 8080, app listens on port 80 → FAIL

---

## Evidence Chain

### 1. Deployment Status
```bash
az containerapp list -g lab-master-lab
# Result: 7/7 Container Apps deployed, provisioningState: "Succeeded"
```

### 2. Runtime Status
```bash
az containerapp revision show ... --query "properties.{health:healthState, running:runningState}"
# Result:
{
  "health": "Unhealthy",
  "running": "Degraded"
}
```

### 3. Container Logs
```json
{"Log": "12:24:21 Listening on :80..."}
```

### 4. Ingress Configuration
```json
{
  "targetPort": 8080,  // ← MISMATCH
  "probes": null,      // ← No custom health probe
  "external": true,
  "fqdn": "mcp-weather-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io"
}
```

---

## Fix Strategy

### Option A: Change Target Port (80 → Azure expects this)
**CHOSEN - FASTEST**

Update all 7 Container Apps to use targetPort: 80

```bash
for app in mcp-weather mcp-oncall mcp-github mcp-spotify mcp-product-catalog mcp-place-order mcp-ms-learn; do
  az containerapp ingress update \
    -g lab-master-lab \
    -n ${app}-pavavy6pu5 \
    --target-port 80
done
```

**Pros**:
- Fast (no redeployment, just config change)
- Matches actual app behavior
- Automatic revision creation

**Cons**:
- Doesn't match Bicep template (8080)

---

### Option B: Change App Listen Port (80 → 8080)
Update container to listen on 8080 via environment variable

```bash
az containerapp update \
  -g lab-master-lab \
  -n mcp-weather-pavavy6pu5 \
  --container-name weather \
  --env-vars "PORT=8080"
```

**Pros**:
- Matches Bicep template intention
- Follows Container Apps best practices

**Cons**:
- Requires redeployment (slower)
- Need to update all 7 apps
- May require app code change if PORT env var not supported

---

### Option C: Add Custom Health Probe
Add HTTP health probe pointing to port 80

**Pros**:
- Explicit health check configuration
- More robust

**Cons**:
- More complex
- Still doesn't fix port mismatch
- Requires Bicep template update

---

## Fix Implementation

### Step 1: Fix Weather App (Test)

```bash
# Update target port from 8080 → 80
az containerapp ingress update \
  -g lab-master-lab \
  -n mcp-weather-pavavy6pu5 \
  --target-port 80

# Wait 30-60 seconds for new revision
sleep 60

# Test HTTP connectivity
curl -v https://mcp-weather-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io/health
```

**Expected**: 200 OK response

---

### Step 2: Apply to All 7 Apps

```bash
#!/bin/bash
APPS=(
  "mcp-weather-pavavy6pu5"
  "mcp-oncall-pavavy6pu5"
  "mcp-github-pavavy6pu5"
  "mcp-spotify-pavavy6pu5"
  "mcp-product-catalog-pavavy6pu5"
  "mcp-place-order-pavavy6pu5"
  "mcp-ms-learn-pavavy6pu5"
)

for app in "${APPS[@]}"; do
  echo "[*] Updating $app target port to 80..."
  az containerapp ingress update \
    -g lab-master-lab \
    -n $app \
    --target-port 80 \
    --output none
  echo "[✓] $app updated"
done

echo ""
echo "Waiting 90 seconds for new revisions to deploy..."
sleep 90

echo ""
echo "Testing HTTP connectivity..."
python3 << 'EOF'
import httpx

urls = {
    "weather": "https://mcp-weather-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io",
    "oncall": "https://mcp-oncall-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io",
    "github": "https://mcp-github-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io",
    "spotify": "https://mcp-spotify-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io",
    "product-catalog": "https://mcp-product-catalog-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io",
    "place-order": "https://mcp-place-order-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io",
    "ms-learn": "https://mcp-ms-learn-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io"
}

results = {}
for name, url in urls.items():
    try:
        response = httpx.get(f"{url}/health", timeout=15.0)
        print(f"✅ {name}: {response.status_code}")
        results[name] = response.status_code
    except Exception as e:
        print(f"❌ {name}: {str(e)[:60]}")
        results[name] = "ERROR"

up = sum(1 for r in results.values() if r == 200)
print(f"\n=== SUMMARY ===")
print(f"MCP Apps UP: {up}/7")
print(f"MCP Apps DOWN: {7-up}/7")
EOF
```

---

## Post-Fix Verification

### Health Check Status
```bash
az containerapp revision list \
  -g lab-master-lab \
  -n mcp-weather-pavavy6pu5 \
  --query "[0].{name:name, health:properties.healthState, replicas:properties.replicas}" \
  -o json
```

**Expected**:
```json
{
  "health": "Healthy",
  "name": "mcp-weather-pavavy6pu5--<new-revision>",
  "replicas": 1
}
```

### HTTP Connectivity
```bash
curl https://mcp-weather-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io/health
```

**Expected**: `200 OK` with health status response

---

## Impact on Notebook

### Cells That Will Start Working

After MCP apps are healthy and responding:

- **Cells 82-94**: Lab 10 MCP examples (13 cells) ✅
- **Cell 96**: Product catalog MCP ✅
- **Cell 98**: AutoGen with MCP ✅
- **Cell 105**: Workflow with MCP ✅
- **Cells 146-150**: MCP authorization tests (5 cells) ✅

**Total**: ~30 cells will be unblocked

---

## Phase 1 Status Update

### ✅ COMPLETED
1. Identified APIM subscription key (`b64e6a3117b64b81a8438a28ced92cb0`)
2. Verified master-lab.env has correct APIM configuration
3. Confirmed MCP URLs in .env are correct (niceriver domain)
4. Diagnosed MCP health check failure (port mismatch)

### 🔄 IN PROGRESS
1. Fixing MCP Container App target port (8080 → 80)
2. Testing HTTP connectivity after port fix

### ⏭️ PENDING (Phase 1 remaining)
1. Verify client initialization in notebook cells
2. Test Cell 41 (basic chat completion with APIM key)
3. Add client initialization cell if needed

### ⏭️ PENDING (Phase 2)
1. Fix Access Control lab cells (59-64)
2. JWT authentication configuration
3. Sequential cell fixes

---

## Success Criteria

### Phase 1 Complete When:
- [x] APIM_API_KEY exists in master-lab.env
- [x] MCP Container Apps deployed (7/7)
- [ ] MCP Container Apps healthy (currently 0/7, fixing...)
- [ ] MCP HTTP connectivity (expect 7/7 after port fix)
- [ ] `client` variable initialized in notebook
- [ ] Cell 41 returns 200 (not 401)

---

## Timeline

| Task | Est. Time | Status |
|------|-----------|--------|
| Identify port mismatch | 30 min | ✅ DONE |
| Update weather app (test) | 2 min | 🔄 IN PROGRESS |
| Verify weather app healthy | 2 min | ⏭️ NEXT |
| Update all 7 apps | 5 min | ⏭️ PENDING |
| Verify all apps healthy | 3 min | ⏭️ PENDING |
| Test HTTP connectivity | 3 min | ⏭️ PENDING |
| **Total** | **45 min** | |

---

**Created**: 2025-11-15
**Root Cause**: Container Apps targetPort (8080) ≠ App listen port (80)
**Fix**: Change ingress target port to 80 for all apps
**Next**: Apply fix to all 7 Container Apps

