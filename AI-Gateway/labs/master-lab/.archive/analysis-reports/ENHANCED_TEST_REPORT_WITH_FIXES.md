# Enhanced Testing Report with Iterative Fixes

**Generated:** 2025-11-11T02:48:49.229050
**Notebook:** master-ai-gateway-consolidated.ipynb
**Testing Method:** Context-aware with iterative fix-and-rerun

## Summary

**Total Cells Tested:** 95
**Cells Needing Fixes:** 17
**Total Fixes Applied:** 18

## Test Results by Cell


### Cell 38

**Topic:** deployment
**Services:** APIM, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] Failed to apply policy: ERROR: 'policy' is misspelled or not recognized by the system.

**Fixes Applied:** 1


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

### Cell 39

**Topic:** deployment
**Services:** APIM, Azure OpenAI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 41

**Topic:** testing
**Services:** None
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 43

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 45

**Topic:** deployment
**Services:** APIM, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] Failed to apply policy: ERROR: 'policy' is misspelled or not recognized by the system.

**Fixes Applied:** 1


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

### Cell 47

**Topic:** load_balancing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 49

**Topic:** load_balancing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 51

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 53

**Topic:** rate_limiting
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 55

**Topic:** rate_limiting
**Services:** APIM, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] Failed to apply policy: ERROR: 'policy' is misspelled or not recognized by the system.

**Fixes Applied:** 1


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

### Cell 57

**Topic:** deployment
**Services:** APIM
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: HTTP_401
- Error Message: [ERROR] Mixed auth failed (401)

**Fixes Applied:** 1


#### Fix 1: Fix authentication error 401

**Type:** `auth_error`

**Code:**
```python
# Authentication error - check:
# 1. APIM_API_KEY is set correctly in master-lab.env
# 2. API key has not expired
# 3. Run Cell 3 to reload environment

# Add to request:
headers = {
    'Ocp-Apim-Subscription-Key': os.getenv('APIM_API_KEY'),
    'Content-Type': 'application/json'
}

```

### Cell 59

**Topic:** content_safety
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: HTTP_400
- Error Message: Content blocked: Error code: 400 - {'error': {'message': "The response was filtered due to the prompt triggering Azure OpenAI's content management policy. Please modify your prompt and retry. To learn

**Status:** ✅ No fixes needed

### Cell 61

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 64

**Topic:** deployment
**Services:** APIM, MCP, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] Unexpected error: Command '['c:\\Users\\lproux\\OneDrive - Microsoft\\bkp\\Documents\\GitHub\\.venv\\Scripts\\az.BAT', '--version']' timed out after 10 seconds

**Fixes Applied:** 1


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

### Cell 65

**Topic:** deployment
**Services:** APIM, Azure OpenAI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 69

**Topic:** mcp
**Services:** MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 71

**Topic:** deployment
**Services:** MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] weather: MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection

**Status:** ✅ No fixes needed

### Cell 72

**Topic:** deployment
**Services:** MCP, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] github: MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection 

**Status:** ✅ No fixes needed

### Cell 73

**Topic:** deployment
**Services:** MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] oncall: MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection 

**Status:** ✅ No fixes needed

### Cell 75

**Topic:** mcp
**Services:** MCP, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] spotify: MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection

**Fixes Applied:** 1


#### Fix 1: Verify MCP server availability

**Type:** `mcp_service_check`

**Code:**
```python
# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")

```

### Cell 77

**Topic:** mcp
**Services:** MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed b

**Fixes Applied:** 1


#### Fix 1: Verify MCP server availability

**Type:** `mcp_service_check`

**Code:**
```python
# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")

```

### Cell 79

**Topic:** mcp
**Services:** MCP
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] Failed to fetch schedule: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established con

**Fixes Applied:** 1


#### Fix 1: Verify MCP server availability

**Type:** `mcp_service_check`

**Code:**
```python
# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")

```

### Cell 81

**Topic:** mcp
**Services:** MCP, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed b

**Fixes Applied:** 1


#### Fix 1: Verify MCP server availability

**Type:** `mcp_service_check`

**Code:**
```python
# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")

```

### Cell 83

**Topic:** rate_limiting
**Services:** MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [mcp][error] MCP initialization or call failed: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or e

**Status:** ✅ No fixes needed

### Cell 86

**Topic:** semantic_caching
**Services:** MCP, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed b

**Status:** ✅ No fixes needed

### Cell 88

**Topic:** mcp
**Services:** MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed b

**Fixes Applied:** 1


#### Fix 1: Verify MCP server availability

**Type:** `mcp_service_check`

**Code:**
```python
# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")

```

### Cell 89

**Topic:** mcp
**Services:** MCP, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] MCPError: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed b

**Fixes Applied:** 1


#### Fix 1: Verify MCP server availability

**Type:** `mcp_service_check`

**Code:**
```python
# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")

```

### Cell 92

**Topic:** mcp
**Services:** MCP, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: None
- Error Message: [ERROR] Workflow failed: MCP initialization error: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection f

**Fixes Applied:** 1


#### Fix 1: Verify MCP server availability

**Type:** `mcp_service_check`

**Code:**
```python
# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")

```

### Cell 94

**Topic:** semantic_caching
**Services:** Redis
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 99

**Topic:** deployment
**Services:** APIM, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: HTTP_403
- Error Message: [ERROR] Unexpected error: Command '['c:\\Users\\lproux\\OneDrive - Microsoft\\bkp\\Documents\\GitHub\\.venv\\Scripts\\az.BAT', '--version']' timed out after 10 seconds

**Fixes Applied:** 2


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

#### Fix 2: Fix authentication error 403

**Type:** `auth_error`

**Code:**
```python
# Authentication error - check:
# 1. APIM_API_KEY is set correctly in master-lab.env
# 2. API key has not expired
# 3. Run Cell 3 to reload environment

# Add to request:
headers = {
    'Ocp-Apim-Subscription-Key': os.getenv('APIM_API_KEY'),
    'Content-Type': 'application/json'
}

```

### Cell 100

**Topic:** deployment
**Services:** APIM, Azure Search
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ✅
- Has Error: False
- Error Code: HTTP_404

**Status:** ✅ No fixes needed

### Cell 102

**Topic:** deployment
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: True
- Error Code: NameError
- Error Message: ERROR: NameError: name 'IMAGE_API_VERSION' is not defined

**Fixes Applied:** 1


#### Fix 1: Add environment variable validation

**Type:** `add_env_var_check`

**Code:**
```python
# Add before using the variable:
required_vars = ['APIM_GATEWAY_URL', 'APIM_API_KEY', 'RESOURCE_GROUP']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    raise RuntimeError(f"Missing environment variables: {missing}. Run Cell 3 first.")

```

### Cell 104

**Topic:** deployment
**Services:** Azure OpenAI, Azure CLI
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Fixes Applied:** 1


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

### Cell 105

**Topic:** deployment
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 106

**Topic:** deployment
**Services:** Azure OpenAI, MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 109

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 111

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 113

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 115

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 117

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 119

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 121

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 123

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 125

**Topic:** semantic_caching
**Services:** None
**Expected Outcome:** cache_hit

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 127

**Topic:** semantic_caching
**Services:** Redis
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 129

**Topic:** deployment
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 131

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 133

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 135

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 137

**Topic:** rate_limiting
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 139

**Topic:** semantic_caching
**Services:** MCP, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 141

**Topic:** content_safety
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 143

**Topic:** chat
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 145

**Topic:** testing
**Services:** None
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 149

**Topic:** mcp
**Services:** MCP
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 151

**Topic:** mcp
**Services:** MCP
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 153

**Topic:** mcp
**Services:** APIM, MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 155

**Topic:** deployment
**Services:** None
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 157

**Topic:** testing
**Services:** None
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 159

**Topic:** deployment
**Services:** MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 161

**Topic:** chat
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 163

**Topic:** semantic_caching
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 165

**Topic:** deployment
**Services:** Cosmos DB
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 167

**Topic:** deployment
**Services:** APIM, Azure Search
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 169

**Topic:** deployment
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 171

**Topic:** testing
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 173

**Topic:** content_safety
**Services:** None
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 174

**Topic:** content_safety
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 176

**Topic:** testing
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 178

**Topic:** testing
**Services:** APIM, Azure OpenAI
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 180

**Topic:** deployment
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 182

**Topic:** testing
**Services:** None
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 185

**Topic:** general
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 187

**Topic:** deployment
**Services:** APIM, Azure OpenAI
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 188

**Topic:** deployment
**Services:** APIM, Azure OpenAI
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 189

**Topic:** deployment
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 190

**Topic:** deployment
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 191

**Topic:** general
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 192

**Topic:** general
**Services:** None
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 197

**Topic:** mcp
**Services:** APIM, Azure OpenAI, MCP
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 198

**Topic:** mcp
**Services:** APIM, MCP, Azure Search
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 200

**Topic:** deployment
**Services:** Azure OpenAI, MCP
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 203

**Topic:** deployment
**Services:** APIM, MCP, Azure Search
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 210

**Topic:** mcp
**Services:** APIM, MCP
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 211

**Topic:** deployment
**Services:** APIM, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Fixes Applied:** 1


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

### Cell 212

**Topic:** deployment
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 213

**Topic:** testing
**Services:** APIM
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 218

**Topic:** mcp
**Services:** MCP
**Expected Outcome:** validation_pass

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 220

**Topic:** semantic_caching
**Services:** MCP
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 221

**Topic:** semantic_caching
**Services:** MCP
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 224

**Topic:** deployment
**Services:** APIM, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Fixes Applied:** 1


#### Fix 1: Remove get_az_cli() - use az_cli from Cell 5

**Type:** `remove_duplicate_function`

**Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5

```

### Cell 225

**Topic:** deployment
**Services:** APIM, Azure CLI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 226

**Topic:** deployment
**Services:** APIM, Azure OpenAI
**Expected Outcome:** no_error

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 227

**Topic:** deployment
**Services:** Azure OpenAI
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

### Cell 229

**Topic:** semantic_caching
**Services:** Azure OpenAI
**Expected Outcome:** unknown

**Actual Outcome:**
- Success: ❌
- Has Error: False
- Error Code: None

**Status:** ✅ No fixes needed

## Fix Types Summary

- `remove_duplicate_function`: 8 occurrences
- `mcp_service_check`: 7 occurrences
- `auth_error`: 2 occurrences
- `add_env_var_check`: 1 occurrences

## Recommendations

1. **Apply All Fixes:** Review each fix and apply to the corresponding cell
2. **Rerun Cells:** After applying fixes, rerun each cell to verify
3. **Iterate:** If cell still fails, analyze new error and apply additional fixes
4. **Verify 100% Success:** Continue until all cells execute without errors

## Next Steps

1. Create updated notebook with all fixes applied
2. Test updated notebook incrementally
3. Verify all cells achieve 100% success rate
4. Document any cells that cannot be automatically fixed
