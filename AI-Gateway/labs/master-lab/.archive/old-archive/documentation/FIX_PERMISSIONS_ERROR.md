# Fix Service Principal Permissions Error

## Problem

Deployment fails at Step 2 (AI Foundry) with:
```
Authorization failed for template resource...
The client does not have permission to perform action
'Microsoft.Authorization/roleAssignments/write'
```

**Cause**: Service Principal has **Contributor** role but needs **User Access Administrator** role to create role assignments.

---

## Solution Options

Choose ONE of the following options:

### Option A: Grant Role via Azure Portal (Easiest - GUI)

1. Open [Azure Portal](https://portal.azure.com)
2. Navigate to **Subscriptions** → Select your subscription
3. Click **Access control (IAM)** in left menu
4. Click **+ Add** → **Add role assignment**
5. **Role**: Search for and select **User Access Administrator**
6. Click **Next**
7. **Assign access to**: User, group, or service principal
8. Click **+ Select members**
9. Search for: `master-lab-sp-` (your Service Principal name)
10. Select it and click **Select**
11. Click **Review + assign**
12. Click **Review + assign** again

**Done!** Now re-run Cell 17 in the notebook.

---

### Option B: Grant Role via Command Line (PowerShell/CMD)

Open a **NEW** PowerShell or Command Prompt window (not in VS Code, not in Jupyter), then run:

```powershell
az role assignment create `
  --assignee 4a5d0f1a-578e-479a-8ba9-05770ae9ce6b `
  --role "User Access Administrator" `
  --scope /subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c
```

**Why a new window?** Your current Azure CLI has cache corruption. A fresh session should work.

**Done!** Now re-run Cell 17 in the notebook.

---

### Option C: Use Azure CLI Credentials Instead (No SP)

If you can't grant the role, use Azure CLI credentials instead:

#### Step 1: Remove Service Principal file
Delete or rename `.azure-credentials.env`

#### Step 2: Re-run authentication cell
Run Cell 15 in notebook - it will detect no SP and fall back to Azure CLI

#### Step 3: Clear Azure CLI cache
```powershell
# In a NEW PowerShell window
Remove-Item "$env:USERPROFILE\.azure\msal_http_cache" -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.azure\msal_token_cache.*" -ErrorAction SilentlyContinue
az account clear
az login
```

#### Step 4: Re-run deployment
Run Cell 17 - it will use your Azure CLI credentials (which typically have Owner permissions)

---

### Option D: Reinstall Azure CLI (Last Resort)

If Azure CLI is completely broken:

1. Download latest Azure CLI: https://aka.ms/installazurecliwindows
2. Uninstall current version
3. Install new version
4. Run: `az login`
5. Try Option B again

---

## Recommended Approach

**For production/automated deployments**: Use **Option A or B** (grant role to Service Principal)
- More stable, no cache issues
- Better for CI/CD pipelines
- Recommended for labs that others will use

**For personal/one-time use**: Use **Option C** (Azure CLI credentials)
- Simpler, no role assignment needed
- Works if you have Owner/Contributor on subscription
- Faster to get started

---

## Verification

After applying any option, verify by running:

```powershell
# Check Service Principal roles (if using Option A/B)
az role assignment list --assignee 4a5d0f1a-578e-479a-8ba9-05770ae9ce6b --output table

# Should show both:
# - Contributor
# - User Access Administrator
```

---

## Next Steps

1. Apply ONE of the solutions above
2. Re-run Cell 17 in [master-ai-gateway.ipynb](master-ai-gateway.ipynb)
3. Deployment should now succeed (~40 minutes total)

---

## Technical Details

The AI Foundry Bicep module creates role assignments:
- **AI Project Manager** role → Service Principal (to manage projects)
- **Cognitive Services User** role → APIM (to call AI endpoints)

These are required for the AI Gateway to function. Without **User Access Administrator** permission, the Service Principal cannot create these role assignments.
