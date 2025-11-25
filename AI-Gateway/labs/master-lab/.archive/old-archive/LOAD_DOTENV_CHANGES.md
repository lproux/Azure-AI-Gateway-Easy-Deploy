# Load Dotenv Changes Summary

## ✅ What Was Fixed

Changed all policy and lab cells from using pre-loaded `os.environ` to explicitly loading `master-lab.env` using `load_dotenv()`.

**Why**: Makes cells kernel-restart resilient - they load their own configuration instead of relying on variables from previous cells.

---

## 📋 Cells Updated

### Cell 30: Apply JWT Only Policy
**Before**:
```python
import requests, os, subprocess, time
subscription_id = os.environ.get('SUBSCRIPTION_ID')  # Might be empty after kernel restart
```

**After**:
```python
import requests, os, subprocess, time
from pathlib import Path
from dotenv import load_dotenv

# Load environment from master-lab.env
env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print(f"[config] Loaded: {env_file.absolute()}")

subscription_id = os.environ.get('SUBSCRIPTION_ID')  # ✅ Always loaded
```

---

### Cell 32: Apply Dual Auth Policy
- Same pattern: loads `master-lab.env` before using `os.environ.get()`

---

### Cell 34: Reset to API Key Policy
- Same pattern: loads `master-lab.env` before using `os.environ.get()`

---

### Cell 54: Token Metrics (Lab 02)
- Same pattern: loads `master-lab.env` before configuring APIM policy

---

### Cell 60: Lab 03 (Load Balancing)
- Same pattern: loads `master-lab.env` before using environment variables

---

## 🎯 Benefits

### Before (os.environ only):
```python
# Cell A
os.environ['SUBSCRIPTION_ID'] = 'xxx'  # Set in earlier cell

# Cell B (after kernel restart)
subscription_id = os.environ.get('SUBSCRIPTION_ID')  # ❌ Empty! Kernel was restarted
```

### After (load_dotenv):
```python
# Cell B (kernel restart safe)
from dotenv import load_dotenv
load_dotenv('master-lab.env')  # ✅ Loads fresh from file
subscription_id = os.environ.get('SUBSCRIPTION_ID')  # ✅ Always has value!
```

---

## 📝 Pattern Used

All updated cells follow this pattern:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment from master-lab.env
env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print(f"[config] Loaded: {env_file.absolute()}")
else:
    print("[warn] master-lab.env not found")

# Now use os.environ.get() as before
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESOURCE_GROUP')
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
```

---

## 🔄 Kernel Restart Workflow

### Old Way (Fragile):
```
1. Run Cell 021 (Generate master-lab.env)
2. Run Cell 022 (Load into os.environ)
3. Restart kernel  ← ❌ All variables lost!
4. Run Cell 030 (JWT Policy)  ← ❌ SUBSCRIPTION_ID is None
```

### New Way (Resilient):
```
1. Run Cell 021 (Generate master-lab.env)
2. Restart kernel  ← ✅ No problem!
3. Run Cell 030 (JWT Policy)  ← ✅ Auto-loads master-lab.env
   Output: [config] Loaded: /path/to/master-lab.env
```

---

## ✅ Verification

When you run any of the updated cells, you should see:
```
[config] Loaded: /mnt/c/Users/lproux/.../master-lab.env
```

This confirms the environment is loaded fresh from the file!

---

**Date**: 2025-11-21
**Cells Updated**: 30, 32, 34, 54, 60
**Pattern**: load_dotenv('master-lab.env') before os.environ.get()
