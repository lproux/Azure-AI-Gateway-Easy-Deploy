# QUICK REFERENCE CARD
## Master AI Gateway Notebook - Critical Fixes

**Date:** 2025-11-13 | **Status:** BROKEN ❌ | **Fix Time:** 30 min

---

## THE PROBLEM (3 Sentences)

1. **Cell 7** tries to load `master-lab.env` before Cell 24 creates it → FileNotFoundError
2. **Cell 15** tries to initialize MCP servers before Cell 24 writes their URLs → KeyError
3. **Cell 28** tries to normalize endpoints before Cell 24 generates the base file → Incomplete data

**Root cause:** Notebook tries to INITIALIZE before DEPLOYMENT completes.

---

## THE FIX (3 Moves)

| Cell | Current Pos | Move To | Why |
|------|-------------|---------|-----|
| 28 | 28 | After 24 | Normalize after generation |
| 7 | 7 | After 28 | Load after normalization |
| 15 | 15 | After 7 | Initialize after loading |

**Result:** Order becomes: 24 → 28 → 7 → 15 ✅

---

## THE CLEANUP (5 Deletions)

| Cell | Reason | Keep Instead |
|------|--------|--------------|
| 1 | Empty | (none) |
| 13 | Duplicate env template | Cell 24 |
| 16 | Duplicate env loader | Cell 24 |
| 22 | Duplicate auth/deploy | Cells 21 + 11 |
| 32 | Duplicate pip install | Cell 27 |

---

## CORRECT EXECUTION ORDER

```
┌─ SETUP ─────────────────────────────────────┐
│ 2:  az() function                           │
│ 3:  Deployment helpers                      │
│ 27: pip install requirements                │
│ 38: Master imports                          │
└─────────────────────────────────────────────┘
          ↓
┌─ CONFIGURE ─────────────────────────────────┐
│ 14: Check Azure CLI                         │
│ 20: Set deployment config                   │
│ 21: Azure authentication                    │
└─────────────────────────────────────────────┘
          ↓
┌─ DEPLOY ────────────────────────────────────┐
│ 11: Main deployment (~40 min) ☕☕☕          │
│     ├─ Step 1: APIM, Log Analytics          │
│     ├─ Step 2: AI Foundry (3 hubs, 14 models│
│     ├─ Step 3: Redis, Search, Cosmos        │
│     └─ Step 4: MCP Servers (7 apps)         │
└─────────────────────────────────────────────┘
          ↓
┌─ CONFIGURE FILES ───────────────────────────┐
│ 24: Generate master-lab.env ⭐              │
│ 28: Normalize endpoints ⭐                  │
└─────────────────────────────────────────────┘
          ↓
┌─ INITIALIZE ────────────────────────────────┐
│ 7:  Load master-lab.env ⭐                  │
│ 15: Initialize MCP servers ⭐               │
└─────────────────────────────────────────────┘
          ↓
┌─ TEST & LABS ───────────────────────────────┐
│ 30+: Tests and verification                 │
│ 70+: 25 lab exercises                       │
└─────────────────────────────────────────────┘
```

⭐ = Moved cells (must be in this order!)

---

## BEFORE vs AFTER

### BEFORE (Broken) ❌

```
Cell 7:  Load .env        ❌ File doesn't exist!
Cell 11: Deploy           ✓ Creates resources
Cell 15: Init MCP         ❌ URLs not in env yet!
Cell 24: Generate .env    ✓ NOW it exists (too late!)
Cell 28: Normalize        ⚠️ Reads incomplete .env
```

### AFTER (Fixed) ✅

```
Cell 11: Deploy           ✓ Creates resources
Cell 24: Generate .env    ✓ Writes 50+ variables
Cell 28: Normalize        ✓ Adds OPENAI_ENDPOINT
Cell 7:  Load .env        ✓ File exists!
Cell 15: Init MCP         ✓ URLs in env!
```

---

## DEPENDENCY RULES

**Golden Rule:** CREATE → GENERATE → LOAD → USE

```
Cell 11 (Deploy)
  ↓ creates resources
Cell 24 (Generate .env from outputs)
  ↓ writes file
Cell 28 (Normalize endpoints)
  ↓ updates file
Cell 7 (Load .env)
  ↓ loads into os.environ
Cell 15 (Initialize MCP)
  ↓ uses os.environ
Labs (Use MCP)
```

**Any violation = BROKEN NOTEBOOK**

---

## VALIDATION CHECKLIST

After fixes:

- [ ] Cell 24 runs BEFORE Cell 7
- [ ] Cell 28 runs BEFORE Cell 7
- [ ] Cell 7 runs BEFORE Cell 15
- [ ] master-lab.env exists after Cell 24
- [ ] master-lab.env has OPENAI_ENDPOINT after Cell 28
- [ ] No errors when running Cell 7
- [ ] No errors when running Cell 15
- [ ] Cells 1,13,16,22,32 deleted
- [ ] Documentation updated (Cells 4,5,10)

---

## COMMON ERRORS & FIXES

| Error | Cause | Fix |
|-------|-------|-----|
| FileNotFoundError: master-lab.env | Cell 7 ran too early | Move Cell 7 after Cell 24 |
| KeyError: MCP_SERVER_WEATHER_URL | Cell 15 ran too early | Move Cell 15 after Cell 7 |
| NameError: apim_gateway_url | Cell 7 didn't load env | Ensure Cell 7 ran successfully |
| Deployment failed | Azure quota/permissions | Check subscription limits |
| Import error | Packages not installed | Run Cell 27 (pip install) |

---

## CRITICAL VARIABLES

### Created by Cell 11 (Deployment)
```python
step1_outputs  # APIM, Log Analytics, App Insights
step2_outputs  # AI Foundry hubs and models
step3_outputs  # Redis, Search, Cosmos, Content Safety
step4_outputs  # MCP server URLs
```

### Created by Cell 24 (Generate .env)
```bash
APIM_GATEWAY_URL           # From step1_outputs
APIM_SUBSCRIPTION_KEY      # From APIM API
MCP_SERVER_WEATHER_URL     # From step4_outputs
MCP_SERVER_GITHUB_URL      # From step4_outputs
REDIS_HOST                 # From step3_outputs
SEARCH_ENDPOINT            # From step3_outputs
# ... 50+ more variables
```

### Created by Cell 28 (Normalize)
```bash
OPENAI_ENDPOINT            # Derived from APIM_GATEWAY_URL + INFERENCE_API_PATH
```

### Loaded by Cell 7 (Load to os.environ)
```python
os.getenv('APIM_GATEWAY_URL')
os.getenv('MCP_SERVER_WEATHER_URL')
# All variables now accessible via os.getenv()
```

### Used by Cell 15 (MCP Init)
```python
mcp.weather    # Uses MCP_SERVER_WEATHER_URL
mcp.github     # Uses MCP_SERVER_GITHUB_URL
mcp.oncall     # Uses MCP_SERVER_ONCALL_URL
# ... 8 MCP servers total
```

---

## FILES CREATED

| File | Created By | Contains |
|------|------------|----------|
| master-lab.env | Cell 24 | 50+ environment variables |
| deploy-01-core.json | Cell 11 (via bicep) | ARM template |
| deploy-02-foundry.json | Cell 11 (via bicep) | ARM template |
| deploy-03-supporting.json | Cell 11 (via bicep) | ARM template |
| deploy-04-mcp.json | Cell 11 (via bicep) | ARM template |

**Note:** .azure-credentials.env is MANUAL (user creates before running)

---

## TIMING

| Phase | Cells | Duration |
|-------|-------|----------|
| Setup | 2,3,27,38 | 2 min |
| Configure | 14,20,21 | 1 min |
| **Deploy** | **11** | **40 min** ☕ |
| Generate Config | 24,28 | 15 sec |
| Initialize | 7,15 | 30 sec |
| Test | 30,34,42 | 1 min |
| Labs | 70+ | Variable |

**Total (deploy + init):** ~45 minutes

---

## RESOURCES CREATED

| Step | Resources | Count |
|------|-----------|-------|
| 0 | Resource Group | 1 |
| 1 | APIM, Log Analytics, App Insights | 3 |
| 2 | AI Hubs (3), AI Models (14) | 17 |
| 3 | Redis, Search, Cosmos, Content Safety | 4 |
| 4 | Container Apps Env, MCP Servers (7) | 8 |

**Total:** ~33 Azure resources

**Cost:** ~$50/day (all resources running)

---

## SPECIFIC CELL QUESTIONS ANSWERED

### Q: What does cell 2 do?
**A:** Defines `az()` helper function for Azure CLI commands with JSON parsing and auto-login.

### Q: Can cell 2 be merged with cell 3?
**A:** NO. Cell 3 depends on cell 2 (calls `az()` in its functions).

### Q: What does cell 3 do?
**A:** Defines deployment helpers: `compile_bicep()`, `deploy_template()`, `get_deployment_outputs()`, `ensure_deployment()`.

### Q: What does it depend on?
**A:** Cell 2 (`az()` function).

### Q: What does cell 10 do?
**A:** It's markdown (documentation), not code. Explains the 4-step deployment.

### Q: Is cell 10 trying to initialize MCP?
**A:** NO. Cell 15 (code) initializes MCP, not cell 10 (markdown).

### Q: Which cells load endpoints before deployment?
**A:** Cell 7 (loads .env before it exists) and Cell 15 (tries to connect before URLs exist).

### Q: Which cells create master-lab.env?
**A:** Cell 24 (primary creator), Cell 28 (updater).

### Q: Which cells read master-lab.env?
**A:** Cell 7 (load_dotenv), Cell 28 (read to normalize), Cell 86+ (labs).

---

## ONE-PAGE FIX CHECKLIST

```
┌─────────────────────────────────────────────────────────────┐
│ MASTER AI GATEWAY NOTEBOOK - FIX CHECKLIST                 │
├─────────────────────────────────────────────────────────────┤
│ [ ] 1. Backup notebook (cp to BACKUP.ipynb)                │
│ [ ] 2. Move Cell 28 → after Cell 24                        │
│ [ ] 3. Move Cell 7 → after new Cell 28                     │
│ [ ] 4. Move Cell 15 → after new Cell 7                     │
│ [ ] 5. Delete Cell 1 (empty)                               │
│ [ ] 6. Delete Cell 13 (dup env)                            │
│ [ ] 7. Delete Cell 16 (dup env)                            │
│ [ ] 8. Delete Cell 22 (dup auth)                           │
│ [ ] 9. Delete Cell 32 (dup pip)                            │
│ [ ] 10. Update Cell 4 docs (new order)                     │
│ [ ] 11. Update Cell 5 docs (new order)                     │
│ [ ] 12. Update Cell 10 docs (prerequisites)                │
│ [ ] 13. Add validation cell after Cell 24                  │
│ [ ] 14. Test: Run Cells 2,3,27,38 (setup)                  │
│ [ ] 15. Test: Run Cells 14,20,21 (config)                  │
│ [ ] 16. Test: Mock Cell 24 with fake outputs               │
│ [ ] 17. Test: Cell 7 loads .env without error              │
│ [ ] 18. Test: Cell 15 attempts MCP init                    │
│ [ ] 19. Full test: Deploy (40 min) if budget allows        │
│ [ ] 20. Verify: All 25 labs work                           │
└─────────────────────────────────────────────────────────────┘

Time estimate: 30 min (fixes) + 15 min (dry test) + 45 min (full test)
Total: 90 minutes

Critical fixes only (items 2-4): 5 minutes
```

---

## EMERGENCY ROLLBACK

If something breaks:

```bash
# Restore from backup
cp master-ai-gateway-BACKUP.ipynb master-ai-gateway-REORGANIZED.ipynb

# Or use git
git checkout master-ai-gateway-REORGANIZED.ipynb
```

---

## SUCCESS INDICATORS

✅ Notebook is FIXED when:
- Cell 7 runs without FileNotFoundError
- Cell 15 runs without KeyError
- Cell 42 (chat completion) returns AI response
- Labs 01-25 execute successfully
- No duplicate cells (1,13,16,22,32) remain

---

## CONTACT FOR HELP

**Analysis Documents:**
- COMPREHENSIVE_DEPENDENCY_MAP.md (full details)
- VISUAL_DEPENDENCY_DIAGRAM.md (flowcharts)
- ACTIONABLE_FIX_PLAN.md (step-by-step guide)
- QUICK_REFERENCE_CARD.md (this document)

**Common Issues:**
- Deployment fails → Check Azure quota
- Import errors → Run Cell 27 first
- Auth fails → Check .azure-credentials.env
- MCP connection fails → Verify Container Apps running

---

**END OF QUICK REFERENCE CARD**

**Print this page for quick access during fixes!** 🖨️
