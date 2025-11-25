# Cell 44 Load Balancing Fix - Testing Log

**Cell:** 44
**Issue:** Load balancing not working - all requests go to UK South only
**Severity:** CRITICAL
**Date:** 2025-11-17

## A. Analyze Current Code

Current backend configuration:
```python
backends_config = [
    {'id': 'foundry1', 'url': f'https://foundry1-{resource_suffix}.openai.azure.com/openai', 'location': 'uksouth', 'priority': 1, 'weight': 100},
    {'id': 'foundry2', 'url': f'https://foundry2-{resource_suffix}.openai.azure.com/openai', 'location': 'eastus', 'priority': 2, 'weight': 50},
    {'id': 'foundry3', 'url': f'https://foundry3-{resource_suffix}.openai.azure.com/openai', 'location': 'norwayeast', 'priority': 2, 'weight': 50},
]
```

**Problem:** Priority-based routing
- foundry1: priority 1 (highest) - used first
- foundry2, foundry3: priority 2 - only used if foundry1 is down

## B. Analyze Current Output

From cell 47 test results:
```
Request 1: 0.85s - Region: UK South - Backend: Unknown
Request 2: 0.81s - Region: UK South - Backend: Unknown
Request 3: 0.71s - Region: UK South - Backend: Unknown
Request 4: 0.71s - Region: UK South - Backend: Unknown
Request 5: 0.82s - Region: UK South - Backend: Unknown

Region Distribution:
  UK South: 5 requests (100.0%)
```

**Conclusion:** 100% of requests to UK South confirms priority-based routing is active.

## C. Create Resolution

**Fix:** Set all backends to priority 1 with equal weights for true round-robin:

```python
backends_config = [
    {'id': 'foundry1', 'url': f'https://foundry1-{resource_suffix}.openai.azure.com/openai', 'location': 'uksouth', 'priority': 1, 'weight': 1},
    {'id': 'foundry2', 'url': f'https://foundry2-{resource_suffix}.openai.azure.com/openai', 'location': 'eastus', 'priority': 1, 'weight': 1},
    {'id': 'foundry3', 'url': f'https://foundry3-{resource_suffix}.openai.azure.com/openai', 'location': 'norwayeast', 'priority': 1, 'weight': 1},
]
```

**Rationale:**
- All same priority (1) = no priority-based routing
- All same weight (1) = equal distribution (round-robin)
- According to Azure APIM docs: "Requests are distributed evenly across the backends in the pool by default" when priority and weight are equal

## D. Create Predicted Output

After fix, cell 47 should show:
```
Request 1: ~0.7s - Region: UK South - Backend: foundry1
Request 2: ~0.8s - Region: East US - Backend: foundry2
Request 3: ~0.9s - Region: Norway East - Backend: foundry3
Request 4: ~0.7s - Region: UK South - Backend: foundry1
Request 5: ~0.8s - Region: East US - Backend: foundry2

Region Distribution:
  UK South: 2 requests (40.0%)
  East US: 2 requests (40.0%)
  Norway East: 1 request (20.0%)
```

**Acceptable variance:** ±20% per region (due to distributed nature of APIM)
- Target: ~33% each (1.67 requests out of 5)
- Acceptable range: 1-3 requests per region

**Success Criteria:**
✓ At least 2 of 3 regions receive requests
✓ No single region receives >70% of requests
✓ Backend pool created successfully with 3 backends
✓ All 3 backends show priority=1, weight=1

## E. Run the Cell
(To be executed)

## F. Analyze Actual Output
(To be captured)

## G. Compare Expected vs Actual
(To be analyzed)

## H. Analyze Discrepancies
(To be documented)

## I. Verify Match
(To be confirmed)

## J. If No Match → Restart at A
(If needed)

## K. Run Full Notebook to Cell 47
(Sequential test from cell 1)

## L. Success Confirmation
(Final validation)

---

## References
- Azure APIM Backend Pools: https://learn.microsoft.com/en-us/azure/api-management/backends#load-balanced-pool
- Load Balancing Options: Round-robin (default when priority/weight equal)
- Priority-based: Lower number = higher priority (1 > 2)
