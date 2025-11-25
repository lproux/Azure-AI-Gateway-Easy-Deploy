# Deep Context-Aware Analysis Report

**Generated:** 2025-11-11T03:05:25.880264
**Notebook:** master-ai-gateway-consolidated.ipynb
**Analysis Type:** Expected vs Actual Output Comparison with Deep Context Understanding

---

## Executive Summary

**Total Cells Analyzed:** 95
**Cells Needing Fixes:** 88
**Cells Matching Expected:** 7

### Fix Priority Breakdown

- **HIGH Priority:** 9 cells (critical issues blocking functionality)
- **MEDIUM Priority:** 79 cells (improvements recommended)
- **Total Fixes Needed:** 88

---

## Cell-by-Cell Analysis


## 📂 Test 1: Basic Chat Completion

### Cell 38 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab: Token Metrics Configuration
# Deploy token metrics emitting policy for monitoring and analytics

import os
import subprocess
import shutil
import time
import tempfile

def get_az_cli():
    """...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---

### Cell 39 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 01: Test 1 - Basic Chat Completion
# This cell initializes the AzureOpenAI client and tests basic chat completion

# Import required libraries (in case they weren't imported earlier)
import os
f...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: Success
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** Success

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** Expected indicators (✅, Test passed, Success) not found in output
- **Discrepancies:** Success indicators missing

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Success - found indicators: Success
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Test 2: Streaming Response

### Cell 41 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 01: Test 2 - Streaming Response

print('[*] Testing streaming...')
stream = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Count from 1 to 5'...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** output_without_clear_status
- **Summary:** Has output but unclear if successful
- **Has Output:** Yes
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** Expected indicators (✅, Test passed, Success) not found in output
- **Discrepancies:** Success indicators missing

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Has output but unclear if successful
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Test 3: Multiple Requests

### Cell 43 ✅ MATCHES EXPECTED

**Source Preview:**
```python
for i in range(5):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Request {i+1}'}],
        max_tokens=10
    )
    print(f...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: ✅
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** ✅

#### Comparison
- **Matches Expected:** ✅ Yes
- **Confidence:** HIGH
- **Reasoning:** Output matches expected success indicators

---


## 📂 <a id='lab02'></a>## Lab 02: Backend Pool Load Balancing![Backend Pool Load Balancing](../../images/backend-pool-load-balancing.gif)📖 [Workshop Guide](https://azure-samples.github.io/AI-Gateway/docs/azure-openai/dynamic-failover)### ObjectiveMaster multi-region load balancing with priority-based routing and automatic failover across Azure regions.### What You'll Learn- **Priority Routing:** Configure priority 1 (UK South) with fallback to priority 2 regions- **Round-Robin Distribution:** Balance traffic across Sweden Central and West Europe (50/50 weight)- **Automatic Retry:** APIM retries on HTTP 429 (rate limit) transparently- **Regional Headers:** Track which region served each request via `x-ms-region` header- **Performance Analysis:** Visualize response times and regional distribution---### Backend Pool ConfigurationAzure API Management supports three load balancing strategies:<details><summary><b>1. Round-Robin Distribution</b></summary>Distributes requests evenly across all backends with equal weight.**Configuration:**- All backends have the same priority level- Equal weight distribution (or default weights)- Requests rotate sequentially through backends**Use Case:** When all regions have equal capacity and you want even distribution.</details><details><summary><b>2. Priority-Based Routing</b></summary>Lower priority values receive traffic first, with automatic failover to higher priority backends.**Example Configuration:**- **East US:** Priority 1 (primary)- **West US:** Priority 2 (fallback)- **Sweden Central:** Priority 3 (fallback)**Use Case:** When you have a preferred region for latency or cost reasons.</details><details><summary><b>3. Weighted Load Balancing</b></summary>Assigns different traffic proportions within the same priority level.**Example Configuration:**- **East US:** Priority 1, Weight 100- **West US:** Priority 2, Weight 50- **Sweden Central:** Priority 2, Weight 50When Priority 1 is unavailable, traffic splits 50/50 between Priority 2 backends.**Use Case:** When backends have different capacities or you want controlled traffic distribution.</details>---### Circuit Breaker Configuration> **💡 Tip:** Each backend should have a circuit breaker rule to handle failures gracefully.**Recommended Settings:**- **Failure Count:** 1 (trip after single failure)- **Failure Interval:** 5 minutes- **Custom Range:** HTTP 429 (rate limit)- **Trip Duration:** 1 minute- **Retry-After Header:** EnabledThis configuration ensures that when a backend hits its rate limit (HTTP 429), APIM automatically routes traffic to other backends for 1 minute.---### Monitoring Regional Distribution> **⚠️ Note:** The `x-ms-region` header in responses indicates which backend processed the request.This header allows you to:- Verify load distribution patterns- Monitor failover behavior- Analyze regional performance- Debug routing issues**Example Response Headers:**```x-ms-region: eastusx-ms-region: westusx-ms-region: swedencentral```---### Expected Outcome![result](../../backend-pool-load-balancing/result.png)**Success Criteria:**- Priority 1 backend handles initial requests- Automatic failover to priority 2 when priority 1 exhausted- Equal distribution across priority 2 backends (50/50)- No 429 errors returned to client (APIM retries internally)- Response time visualization shows regional patterns---

### Cell 45 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab: Load Balancing Configuration
# Deploy backend pool load balancing policy with retry logic

import os
import subprocess
import shutil
import time
import tempfile

def get_az_cli():
    """Find A...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---


## 📂 Test 1: Load Distribution

### Cell 47 ✅ MATCHES EXPECTED

**Source Preview:**
```python
print('Testing load balancing across 3 regions...')
responses = []
regions = []  # Track which region processed each request

for i in range(20):
    start = time.time()
    
    # Make request and ca...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: ✅
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** ✅

#### Comparison
- **Matches Expected:** ✅ Yes
- **Confidence:** HIGH
- **Reasoning:** Output matches expected success indicators

---


## 📂 Test 2: Visualize Response Times

### Cell 49 ✅ MATCHES EXPECTED

**Source Preview:**
```python
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Create DataFrame with response times and regions
df = pd.DataFrame({
    'Request': range(1, len(responses)+1), 
...
```

#### Expected Outcome
- **Type:** general
- **Summary:** Should: All tests pass
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: ✅
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** ✅

#### Comparison
- **Matches Expected:** ✅ Yes
- **Confidence:** HIGH
- **Reasoning:** Output matches expected success indicators

---


## 📂 <a id='lab03'></a>

### Cell 51 ✅ MATCHES EXPECTED

**Source Preview:**
```python
for i in range(10):
    client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Log test {i}'}],
        max_tokens=5
    )
utils.print_ok('Lab 03:...
```

#### Expected Outcome
- **Type:** general
- **Summary:** Should: Task completes successfully
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: ✅
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** ✅

#### Comparison
- **Matches Expected:** ✅ Yes
- **Confidence:** HIGH
- **Reasoning:** Output matches expected success indicators

---


## 📂 <a id='lab04'></a>

### Cell 53 ✅ MATCHES EXPECTED

**Source Preview:**
```python
total_tokens = 0
for i in range(5):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'Tell me about AI'}],
        max_tokens=5...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: ✅, Complete
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** ✅, Complete

#### Comparison
- **Matches Expected:** ✅ Yes
- **Confidence:** HIGH
- **Reasoning:** Output matches expected success indicators

---


## 📂 <a id='lab05'></a>## Lab 05: Token Rate Limiting![Token Rate Limiting](../../images/token-rate-limiting.gif)📖 [Workshop Guide](https://azure-samples.github.io/AI-Gateway/docs/azure-openai/rate-limit)### ObjectiveImplement intelligent rate limiting and quota management to prevent abuse and control AI service costs.### What You'll Learn- **Token-Based Rate Limiting:** Limit requests by tokens per minute (TPM) instead of simple request count- **Quota Policies:** Set per-subscription quotas for fair resource allocation- **HTTP 429 Handling:** Proper rate limit error responses with retry-after headers- **Throttling Strategies:** Different approaches for user tier-based limiting- **Cost Control:** Prevent runaway costs from excessive API usage---### Understanding the azure-openai-token-limit PolicyThe `azure-openai-token-limit` policy is a specialized APIM policy that tracks and limits token consumption for Azure OpenAI requests.<details><summary><b>Policy Configuration Example</b></summary>```xml<inbound>    <azure-openai-token-limit         tokens-per-minute="1000"         counter-key="@(context.Subscription.Id)"         estimate-prompt-tokens="true"         remaining-tokens-variable-name="remainingTokens" /></inbound>```**Key Parameters:**- **`tokens-per-minute`**: Maximum tokens allowed per minute (e.g., 1000 TPM)- **`counter-key`**: Identifier to track usage (typically subscription ID, user ID, or API key)- **`estimate-prompt-tokens`**: When `true`, APIM estimates prompt tokens before sending to backend- **`remaining-tokens-variable-name`**: Optional variable to store remaining token count</details>---### How Token Limiting Works> **💡 Tip:** Token-based rate limiting is more accurate than request-based limiting for LLM APIs.**Request Flow:**1. **Request Arrives:** Client sends chat completion request to APIM2. **Token Estimation:** APIM estimates prompt tokens (if enabled)3. **Counter Check:** Policy checks current token usage against limit4. **Decision:**   - ✅ **Within Limit:** Request forwarded to Azure OpenAI   - ❌ **Limit Exceeded:** Returns HTTP 429 with `Retry-After` header5. **Token Counting:** After response, actual token usage is tracked---### HTTP 429 Response Handling> **⚠️ Note:** When the token limit is exceeded, APIM returns HTTP 429 (Too Many Requests).**Example Response:**```httpHTTP/1.1 429 Too Many RequestsRetry-After: 30Content-Type: application/json{  "statusCode": 429,  "message": "Rate limit is exceeded. Try again in 30 seconds."}```**Client Best Practices:**- Implement exponential backoff- Respect the `Retry-After` header- Monitor token usage proactively- Consider request batching---### Advanced Configuration Scenarios<details><summary><b>Per-User Rate Limiting</b></summary>```xml<azure-openai-token-limit     tokens-per-minute="5000"     counter-key="@(context.Request.Headers.GetValueOrDefault("User-ID","anonymous"))"     estimate-prompt-tokens="true" />```Tracks token usage per individual user instead of per subscription.</details><details><summary><b>Tiered Rate Limiting</b></summary>```xml<choose>    <when condition="@(context.Subscription.Name == "premium")">        <azure-openai-token-limit             tokens-per-minute="10000"             counter-key="@(context.Subscription.Id)" />    </when>    <otherwise>        <azure-openai-token-limit             tokens-per-minute="1000"             counter-key="@(context.Subscription.Id)" />    </otherwise></choose>```Different limits for premium vs. standard tier users.</details><details><summary><b>Custom Error Response</b></summary>```xml<inbound>    <azure-openai-token-limit         tokens-per-minute="1000"         counter-key="@(context.Subscription.Id)" /></inbound><on-error>    <choose>        <when condition="@(context.LastError.Source == "azure-openai-token-limit")">            <return-response>                <set-status code="429" reason="Rate Limit Exceeded" />                <set-header name="Retry-After" exists-action="override">                    <value>60</value>                </set-header>                <set-body>@{                    return new JObject(                        new JProperty("error", new JObject(                            new JProperty("code", "rate_limit_exceeded"),                            new JProperty("message", "Token quota exceeded. Please try again later."),                            new JProperty("type", "tokens")                        ))                    ).ToString();                }</set-body>            </return-response>        </when>    </choose></on-error>```Provides a custom, user-friendly error response.</details>---### Testing Rate Limits**Testing Strategy:**1. Set a low token limit (e.g., 50 TPM) for testing2. Send multiple requests quickly3. Verify HTTP 429 response when limit exceeded4. Check `Retry-After` header value5. Wait and verify request succeeds after limit resets**Python Test Example:**```pythonimport timefrom openai import OpenAIclient = OpenAI(api_key="your-key", base_url="https://your-apim.azure-api.net")for i in range(10):    try:        response = client.chat.completions.create(            model="gpt-4o-mini",            messages=[{"role": "user", "content": "Test message"}]        )        print(f"Request {i+1}: Success")    except Exception as e:        if "429" in str(e):            print(f"Request {i+1}: Rate limited - {e}")        else:            raise    time.sleep(1)```---### Expected Outcome![result](../../token-rate-limiting/result.png)**Success Criteria:**- Rate limiter returns HTTP 429 when quota exceeded- Retry-After header indicates when to retry- Different quotas enforced per subscription tier- Token counting is accurate and consistent- Users receive clear error messages when limited---

### Cell 55 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 05: Token-Based Rate Limiting
# This lab demonstrates proper APIM token rate limiting using azure-openai-token-limit policy

import os
import subprocess
import shutil
import time
import tempfile...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---


## 📂 <a id='lab06'></a>## Lab 06: Access Controlling![Access Controlling](../../images/access-controlling.gif)📖 [Workshop Guide](https://azure-samples.github.io/AI-Gateway/)### ObjectiveSecure AI gateway endpoints using OAuth 2.0 and Microsoft Entra ID (formerly Azure AD) for enterprise authentication.### What You'll Learn- **OAuth 2.0 Flow:** Implement token-based authentication with Entra ID- **JWT Validation:** Validate JSON Web Tokens in APIM policies- **RBAC Integration:** Control access based on Azure roles and groups- **API Scopes:** Define granular permissions for different API operations- **Token Claims:** Extract user identity and roles from access tokens---### Understanding OAuth 2.0 with Microsoft Entra ID> **💡 Tip:** OAuth 2.0 provides token-based authentication without exposing credentials in each request.**Authentication Flow:**1. **User Login:** Client application redirects user to Entra ID login2. **Authentication:** User enters credentials and consents to permissions3. **Token Issuance:** Entra ID issues JWT access token4. **API Request:** Client includes token in `Authorization: Bearer <token>` header5. **Token Validation:** APIM validates token signature, expiration, and claims6. **Request Processing:** If valid, request forwarded to Azure OpenAI backend---### JWT Validation PolicyAzure API Management uses the `validate-jwt` policy to secure endpoints.<details><summary><b>Basic JWT Validation Example</b></summary>```xml<inbound>    <validate-jwt         header-name="Authorization"         failed-validation-httpcode="401"         failed-validation-error-message="Unauthorized. Access token is missing or invalid.">        <openid-config url="https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration" />        <audiences>            <audience>api://your-api-client-id</audience>        </audiences>        <issuers>            <issuer>https://sts.windows.net/{tenant-id}/</issuer>        </issuers>        <required-claims>            <claim name="roles" match="any">                <value>AI.User</value>                <value>AI.Admin</value>            </claim>        </required-claims>    </validate-jwt></inbound>```**Key Components:**- **`header-name`**: HTTP header containing the JWT (typically "Authorization")- **`openid-config`**: URL to Entra ID's OpenID Connect metadata- **`audiences`**: Valid audience (aud) claim values- **`issuers`**: Trusted token issuers- **`required-claims`**: Claims that must be present in the token</details>---### Microsoft Entra ID Integration> **⚠️ Note:** You need to register your application in Microsoft Entra ID before implementing OAuth 2.0.**Setup Steps:**1. **Register Application:**   - Go to Azure Portal → Entra ID → App Registrations   - Create new registration   - Note the Application (client) ID and Tenant ID2. **Configure API Permissions:**   - Add API permissions for your application   - Define custom scopes (e.g., `AI.Read`, `AI.Write`)   - Grant admin consent if required3. **Create App Roles:**   - Define roles in app manifest (e.g., `AI.User`, `AI.Admin`)   - Assign users/groups to roles4. **Configure APIM:**   - Add `validate-jwt` policy to API   - Reference Entra ID tenant and client IDs   - Map roles to API operations---### Role-Based Access Control (RBAC)<details><summary><b>Policy Example: Different Access for Different Roles</b></summary>```xml<inbound>    <validate-jwt header-name="Authorization">        <openid-config url="https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration" />        <audiences>            <audience>api://your-api-client-id</audience>        </audiences>    </validate-jwt>        <!-- Admin users get priority routing -->    <choose>        <when condition="@(context.Request.Headers.GetValueOrDefault("Authorization","").AsJwt()?.Claims.GetValueOrDefault("roles","").Contains("AI.Admin") == true)">            <set-backend-service backend-id="openai-premium-backend" />        </when>        <!-- Regular users get standard backend -->        <otherwise>            <set-backend-service backend-id="openai-standard-backend" />        </otherwise>    </choose></inbound>```This example routes admin users to a premium backend with higher quotas.</details><details><summary><b>Policy Example: Scope-Based Operation Control</b></summary>```xml<inbound>    <validate-jwt header-name="Authorization">        <openid-config url="https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration" />        <required-claims>            <claim name="scp" match="any">                <value>AI.Read</value>                <value>AI.Write</value>            </claim>        </required-claims>    </validate-jwt>        <!-- Check if operation requires write permission -->    <choose>        <when condition="@(context.Request.Method != "GET")">            <validate-jwt header-name="Authorization">                <required-claims>                    <claim name="scp" match="any">                        <value>AI.Write</value>                    </claim>                </required-claims>            </validate-jwt>        </when>    </choose></inbound>```This ensures only tokens with `AI.Write` scope can perform non-GET operations.</details>---### Token Claims and User IdentityJWT tokens contain claims that provide user context.**Common Claims:**- **`sub`**: Subject (unique user identifier)- **`name`**: User's display name- **`email`**: User's email address- **`roles`**: User's assigned roles- **`scp`**: Delegated permissions (scopes)- **`aud`**: Audience (intended recipient)- **`iss`**: Issuer (who issued the token)- **`exp`**: Expiration timestamp**Extracting Claims in Policy:**```xml<set-header name="X-User-Email" exists-action="override">    <value>@(context.Request.Headers.GetValueOrDefault("Authorization","").AsJwt()?.Claims.GetValueOrDefault("email", "unknown"))</value></set-header>```---### Testing Access Control**Test Scenarios:**1. **No Token:** Request without Authorization header → 401 Unauthorized2. **Invalid Token:** Request with malformed/expired token → 401 Unauthorized3. **Valid Token:** Request with valid Entra ID token → 200 OK4. **Insufficient Permissions:** Token without required role/scope → 403 Forbidden5. **Token Expiration:** Request after token expires → 401 Unauthorized**Python Example with Azure Identity:**```pythonfrom azure.identity import DefaultAzureCredentialfrom openai import AzureOpenAIimport requests# Get token from Azure Identitycredential = DefaultAzureCredential()token = credential.get_token("api://your-api-client-id/.default")# Use token with OpenAI clientclient = AzureOpenAI(    azure_endpoint="https://your-apim.azure-api.net",    api_key=token.token,  # JWT token used as API key    api_version="2024-02-15-preview")response = client.chat.completions.create(    model="gpt-4o-mini",    messages=[{"role": "user", "content": "Hello!"}])```---### Security Best Practices> **💡 Security Checklist:**- ✅ Always validate JWT signature using OpenID configuration- ✅ Check token expiration (`exp` claim)- ✅ Verify audience (`aud`) matches your API- ✅ Validate issuer (`iss`) is from trusted Entra ID- ✅ Use HTTPS only (never HTTP for authentication)- ✅ Implement proper error handling (don't leak sensitive info)- ✅ Log authentication failures for security monitoring- ✅ Rotate client secrets regularly- ✅ Use least-privilege principle for role assignments---### Expected Outcome**Success Criteria:**- Unauthenticated requests return HTTP 401 Unauthorized- Valid Entra ID tokens grant access successfully- JWT validation policy correctly verifies token signatures- User roles properly restrict access to specific operations- Token expiration is enforced correctly- Clear error messages guide users on authentication issues---

### Cell 57 ❌ NEEDS FIX

**Source Preview:**
```python
import os, json, requests
from azure.identity import DefaultAzureCredential

# Lab 06: Access Control with JWT (Bearer) + fallback API key
# This lab demonstrates OAuth 2.0 authentication with Azure E...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred: SystemExit
- **Has Output:** Yes
- **Has Error:** Yes
- **Error Details:** SystemExit

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: SystemExit
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Error occurred: SystemExit
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 <a id='lab07'></a>

### Cell 59 ❌ NEEDS FIX

**Source Preview:**
```python
# Test with safe content
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'What is the weather like?'}],
    max_tokens=20
)
print(f'Safe c...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Content filtered, Safety check passed
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** output_without_clear_status
- **Summary:** Has output but unclear if successful
- **Has Output:** Yes
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** Expected indicators (Content filtered, Safety check passed) not found in output
- **Discrepancies:** Success indicators missing

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Has output but unclear if successful
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 <a id='lab08'></a>

### Cell 61 ✅ MATCHES EXPECTED

**Source Preview:**
```python
models_to_test = ['gpt-4o-mini', 'gpt-4.1-mini']
for model in models_to_test:
    response = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': 'Hello'}...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: ✅, Complete
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** ✅, Complete

#### Comparison
- **Matches Expected:** ✅ Yes
- **Confidence:** HIGH
- **Reasoning:** Output matches expected success indicators

---


## 📂 APIM ❤️ AI Foundry

### Cell 64 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab: Private Connectivity Configuration
# Deploy private connectivity policy with managed identity authentication

import os
import subprocess
import shutil
import time
import tempfile

def get_az_c...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---

### Cell 65 ✅ MATCHES EXPECTED

**Source Preview:**
```python
# Lab 09: AI Foundry SDK - Chat Completion via APIM
# CRITICAL: ChatCompletionsClient requires the FULL endpoint path including deployment

# Import required libraries
from azure.ai.inference import C...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: Success, Complete
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** Success, Complete

#### Comparison
- **Matches Expected:** ✅ Yes
- **Confidence:** HIGH
- **Reasoning:** Output matches expected success indicators

---


## 📂 <a id='lab10'></a>

### Cell 69 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 10: MCP Server Integration - Simplified Initialization
# MCP servers in this notebook use HTTP POST to /mcp/ endpoint
# Helper classes (WeatherMCP, GitHubMCP, etc.) handle this automatically

im...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** success
- **Summary:** Success - found indicators: Success, Complete
- **Has Output:** Yes
- **Has Error:** No
- **Indicators Found:** Success, Complete

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** Expected indicators (✅, Success, Complete) not found in output
- **Discrepancies:** Success indicators missing

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Success - found indicators: Success, Complete
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 11: Understanding MCP Connection Methods![Model Context Protocol](../../images/model-context-protocol.gif)📖 [Workshop Guide - MCP Integration](https://azure-samples.github.io/AI-Gateway/)---### What is Model Context Protocol (MCP)?> **💡 Definition:** Model Context Protocol is an open standard that enables AI models to securely connect to external data sources and tools.**Key Benefits:**- **Standardized Integration:** Universal protocol for connecting LLMs to tools- **Secure Access:** Built-in OAuth 2.0 authentication support- **Tool Discovery:** Automatic discovery of available tools and their schemas- **Bi-directional Communication:** Supports both request/response and streaming patterns- **Vendor Neutral:** Works across different AI platforms and models**Use Cases:**- Connect AI to enterprise databases- Integrate with third-party APIs (GitHub, Slack, etc.)- Access real-time data (weather, stock prices, etc.)- Execute business logic securely- Retrieve context from knowledge bases---### MCP Architecture Overview**Component Stack:**```┌─────────────────────────────────────┐│   AI Application (Client)          ││   - ChatGPT, Claude, Custom Apps   │└──────────────┬──────────────────────┘               │ MCP Protocol┌──────────────▼──────────────────────┐│   Azure API Management Gateway      ││   - Authentication & Authorization  ││   - Rate Limiting & Caching        ││   - Load Balancing & Monitoring    │└──────────────┬──────────────────────┘               │ HTTP/SSE┌──────────────▼──────────────────────┐│   MCP Server                        ││   - Tool Definitions               ││   - Business Logic                 ││   - Data Access                    │└─────────────────────────────────────┘```**Data Flow:**1. AI application sends MCP request to APIM2. APIM validates OAuth token and enforces policies3. Request forwarded to MCP server4. MCP server executes tool and returns result5. APIM proxies response back to client6. AI model processes tool result and generates response---### Two MCP Connection Patterns**Important:** This lab uses HTTP-based MCP servers that communicate via POST requests to `/mcp/` endpoints.<details><summary><b>Pattern 1: HTTP-Based MCP</b> (✅ Used in this notebook)</summary>**How It Works:**- **Protocol:** HTTP POST requests- **Endpoint:** `{server_url}/mcp/`- **Format:** JSON-RPC 2.0- **Communication:** Request/response pattern**Advantages:**- Simple, reliable, works with standard HTTP clients- Easy to test with curl or Postman- Works through standard load balancers and API gateways- No special client libraries required- Firewall-friendly (standard HTTP/HTTPS)**Example Request:**```httpPOST https://mcp-weather.example.com/mcp/Content-Type: application/jsonAuthorization: Bearer <token>{  "jsonrpc": "2.0",  "id": 1,  "method": "tools/call",  "params": {    "name": "get_weather",    "arguments": {      "location": "Seattle"    }  }}```**Helper Classes in This Notebook:**- `WeatherMCP` - Weather data retrieval- `GitHubMCP` - GitHub repository operations- `OnCallMCP` - On-call schedule management- `SlackMCP` - Slack messaging integration**Examples:** See cells 58-60, 77-78 for working implementations</details><details><summary><b>Pattern 2: SSE-Based MCP</b> (⚠️ Advanced, server-dependent)</summary>**How It Works:**- **Protocol:** Server-Sent Events (SSE)- **Endpoint:** `{server_url}/sse` or `/mcp` or `/events` (varies by server)- **Format:** Streaming responses- **Communication:** Bi-directional streaming**Advantages:**- Real-time updates and streaming responses- Efficient for long-running operations- Supports server-initiated events- Better for interactive applications**Challenges:**- Requires endpoint discovery (path varies by server)- More complex client implementation- May not work through all proxies/firewalls- Requires SSE-compatible infrastructure**Use Cases:**- Real-time progress updates- Streaming AI responses- Long-running tool executions- Live data feeds**Note:** This pattern requires the MCP server to explicitly support SSE. Not all servers implement this.</details>---### MCP Through Azure API Management> **⚠️ Security Note:** Always authenticate MCP requests through APIM to ensure secure tool access.**APIM Policy Example for MCP:**```xml<inbound>    <!-- Validate OAuth 2.0 token -->    <validate-jwt header-name="Authorization">        <openid-config url="https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration" />        <audiences>            <audience>api://mcp-server</audience>        </audiences>        <required-claims>            <claim name="roles" match="any">                <value>MCP.User</value>            </claim>        </required-claims>    </validate-jwt>        <!-- Rate limit MCP tool calls -->    <rate-limit-by-key         calls="100"         renewal-period="60"         counter-key="@(context.Request.Headers.GetValueOrDefault("Authorization","").AsJwt()?.Subject)" />        <!-- Route to MCP backend -->    <set-backend-service backend-id="mcp-server-backend" />        <!-- Add tracking headers -->    <set-header name="X-MCP-Request-ID" exists-action="override">        <value>@(context.RequestId)</value>    </set-header></inbound><outbound>    <!-- Log MCP tool usage -->    <log-to-eventhub logger-id="mcp-logger">        @{            return new JObject(                new JProperty("timestamp", DateTime.UtcNow),                new JProperty("user", context.Request.Headers.GetValueOrDefault("Authorization","").AsJwt()?.Subject),                new JProperty("tool", context.Request.Body.As<JObject>(preserveContent: true)["params"]["name"]),                new JProperty("duration", context.Elapsed.TotalMilliseconds)            ).ToString();        }    </log-to-eventhub></outbound>```---### Why Previous Connectivity Tests Showed 404The diagnostic in earlier versions tested base URLs (`https://server.com`) without specific endpoints. This always returned 404 because:1. ❌ `GET https://mcp-weather.com` → 404 (no endpoint defined for root)2. ❌ `GET https://mcp-weather.com/mcp/` → 404 (wrong HTTP method)3. ✅ `POST https://mcp-weather.com/mcp/` → 200 (correct endpoint and method)**Key Insight:** MCP servers don't respond to GET requests on their root URL. They require POST to `/mcp/` with JSON-RPC payload.---### Working Examples in This Notebook**See these cells for working MCP implementations:**- **Cell 58:** Weather MCP using `WeatherMCP` helper  - Retrieves current weather data  - Demonstrates basic tool calling  - **Cell 59:** GitHub MCP using `GitHubMCP` helper  - Repository operations (search, read files)  - Shows authenticated MCP requests  - **Cell 60:** OnCall MCP using `OnCallMCP` helper  - On-call schedule management  - Demonstrates enterprise integrationAll use HTTP POST to `/mcp/` endpoint, which is why they work reliably.---### Testing MCP Connections**Manual Test with curl:**```bash# Test MCP server availabilitycurl -X POST https://mcp-weather.example.com/mcp/   -H "Content-Type: application/json"   -H "Authorization: Bearer YOUR_TOKEN"   -d '{    "jsonrpc": "2.0",    "id": 1,    "method": "tools/list",    "params": {}  }'# Expected response:{  "jsonrpc": "2.0",  "id": 1,  "result": {    "tools": [      {        "name": "get_weather",        "description": "Get current weather for a location",        "inputSchema": {...}      }    ]  }}```**Python Test:**```pythonimport requestsfrom azure.identity import DefaultAzureCredential# Get OAuth tokencredential = DefaultAzureCredential()token = credential.get_token("api://mcp-server/.default")# Call MCP serverresponse = requests.post(    "https://your-apim.azure-api.net/mcp/",    headers={        "Authorization": f"Bearer {token.token}",        "Content-Type": "application/json"    },    json={        "jsonrpc": "2.0",        "id": 1,        "method": "tools/call",        "params": {            "name": "get_weather",            "arguments": {"location": "Seattle"}        }    })print(response.json())```---### Best Practices for MCP Integration> **💡 Production Checklist:**- ✅ **Authentication:** Always use OAuth 2.0 for MCP servers- ✅ **Rate Limiting:** Protect MCP servers from abuse- ✅ **Monitoring:** Log all tool calls for audit and debugging- ✅ **Error Handling:** Implement proper retry logic for transient failures- ✅ **Timeout Configuration:** Set appropriate timeouts for long-running tools- ✅ **Input Validation:** Validate tool arguments before execution- ✅ **Caching:** Cache frequently used tool results when appropriate- ✅ **Circuit Breaker:** Implement circuit breaking for unreliable tools- ✅ **Documentation:** Maintain clear tool schemas and examples- ✅ **Testing:** Regularly test MCP endpoints for availability---

### Cell 71 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 10 Example: Weather MCP Server
# Demonstrates weather data retrieval via MCP

# Approach 1: Using WeatherMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTTPMC...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Successfully deployed, Deployment complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 72 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 10 Example: GitHub MCP Server
# Demonstrates GitHub repository operations via MCP

# Approach 1: Using GitHubMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHT...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Successfully deployed, Deployment complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 73 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 10 Example: OnCall MCP Server
# Demonstrates on-call schedule management via MCP

# Approach 1: Using OnCallMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTT...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Successfully deployed, Deployment complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 11: spotify

### Cell 75 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 11: Spotify MCP Integration
# Demonstrates music service integration via MCP

# Approach 1: Using SpotifyMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTTPMC...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 12: Weather + AI Analysis

### Cell 77 ❌ NEEDS FIX

**Source Preview:**
```python
# OnCall: Get on-call engineers

from notebook_mcp_helpers import OnCallMCP
import os

# Get OnCall MCP server URL from environment variable
oncall_server_url = os.getenv('MCP_SERVER_ONCALL_URL', 'htt...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 13: OnCall Schedule via MCP

### Cell 79 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 13: OnCall Schedule Access
# Query on-call schedules via MCP server (fixed: removed undefined SSEMCPClient)

def fetch_oncall_schedule():
    # Prefer existing initialized 'oncall' client (creat...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 14: GitHub Repository Access

### Cell 81 ❌ NEEDS FIX

**Source Preview:**
```python
# GitHub: Search and explore repositories

from notebook_mcp_helpers import GitHubMCP
import os

# Get GitHub MCP server URL from environment variable
github_server_url = os.getenv('MCP_SERVER_GITHUB_...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 15: GitHub + AI Code Analysis

### Cell 83 ❌ NEEDS FIX

**Source Preview:**
```python
# GitHub: Repository analysis (MCP + direct fallback + repo existence validation)
import os, socket, requests, json, textwrap, time, base64
from notebook_mcp_helpers import GitHubMCP

OWNER = os.geten...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Troubleshooting GitHub MCP Connectivity (Lab 15)

### Cell 86 ❌ NEEDS FIX

**Source Preview:**
```python
# Spotify: Search for tracks

from notebook_mcp_helpers import SpotifyMCP
import os

# Get Spotify MCP server URL from environment variable
spotify_server_url = os.getenv('MCP_SERVER_SPOTIFY_URL', 'ht...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 17: Spotify + AI Music Recommendations

### Cell 88 ❌ NEEDS FIX

**Source Preview:**
```python
# Spotify: Get playlists and tracks

from notebook_mcp_helpers import SpotifyMCP
import os

# Get Spotify MCP server URL from environment variable
spotify_server_url = os.getenv('MCP_SERVER_SPOTIFY_UR...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 89 ❌ NEEDS FIX

**Source Preview:**
```python
# Product Catalog: Browse and search products

from notebook_mcp_helpers import ProductCatalogMCP
import os

# Get Product Catalog MCP server URL from environment variable
product_catalog_server_url =...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 23: Multi-Server Orchestration

### Cell 92 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 23: Multi-Server Orchestration
# Use multiple MCP servers together for a complete workflow
# FIX: Removed undefined SSEMCPClient (not imported). Reuse existing helper clients already initialized...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Test: Cache Performance

### Cell 94 ❌ NEEDS FIX

**Source Preview:**
```python
import redis.asyncio as redis

questions = [
    'How to make coffee?',
    'What is the best way to brew coffee?',
    'Tell me about coffee preparation',
    'Coffee making tips?'
]

times = []
for ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Cache hit, Cache miss, Semantic match
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** output_without_clear_status
- **Summary:** Has output but unclear if successful
- **Has Output:** Yes
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** Expected indicators (Cache hit, Cache miss, Semantic match) not found in output
- **Discrepancies:** Success indicators missing

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Has output but unclear if successful
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Test: Generate Images

### Cell 99 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab: Model Routing Configuration
# Deploy model routing policy for intelligent model selection and gating

import os
import subprocess
import shutil
import time
import tempfile

def get_az_cli():
  ...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred (type unknown)
- **Has Output:** Yes
- **Has Error:** Yes

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: None
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---

### Cell 100 ❌ NEEDS FIX

**Source Preview:**
```python
# Deployment discovery for image & vision models
import os, requests, json
from typing import Dict, List

inference_api_path = os.getenv("INFERENCE_API_PATH", "inference")
# Safely derive gateway URL;...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** http_error
- **Summary:** HTTP error: 404
- **Has Output:** Yes
- **Has Error:** Yes
- **Error Details:** HTTP_404

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got http_error: HTTP_404
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `fix_endpoint`
- **Priority:** MEDIUM
- **Confidence:** MEDIUM
- **Description:** Fix endpoint URL (404 Not Found)

**Fix Code:**
```python
# Check endpoint URL:
# - Verify API is deployed
# - Check path is correct
# - Ensure APIM gateway URL is correct
print(f"Endpoint: {url}")  # Add debugging
```

---


## 📂 Image & Vision Model Flow (Updated)

### Cell 102 ❌ NEEDS FIX

**Source Preview:**
```python
# Updated Lab 22 Image Generation & Vision Analysis (model-name direct fallback)
import os, base64, json, requests
from typing import Optional

# Core config
inference_api_path = os.getenv("INFERENCE_...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** error
- **Summary:** Error occurred: NameError
- **Has Output:** Yes
- **Has Error:** Yes
- **Error Details:** NameError

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Expected success but got error: NameError
- **Discrepancies:** Error occurred when success expected

#### 💡 Recommended Fix
- **Type:** `add_env_var_check`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Add environment variable validation

**Fix Code:**
```python
# Add at top of cell:
import os
required_vars = ['RESOURCE_GROUP', 'APIM_GATEWAY_URL']  # Adjust as needed
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing: {missing}. Run Cell 3 (Environment Loader) first")
    raise RuntimeError(f"Missing environment variables: {missing}")
```

---


## 📂 Azure OpenAI Image Model Deployment (CLI Attempt)

### Cell 104 ❌ NEEDS FIX

**Source Preview:**
```python
# Azure OpenAI image model deployment via CLI
import os
import re
import json
import subprocess
import shutil
from pathlib import Path

# Azure CLI PATH detection helper
def get_az_cli():
    """Find ...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Duplicate function definition found - should use Cell 5 instead
- **Discrepancies:** Duplicate get_az_cli() function

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---

### Cell 105 ❌ NEEDS FIX

**Source Preview:**
```python
print('Master Lab Testing Complete!')
print(f'Tested {31} labs successfully.')
print('To cleanup: Run master-cleanup.ipynb')
utils.print_ok('All labs completed successfully!')

```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Successfully deployed, Deployment complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 106 ❌ NEEDS FIX

**Source Preview:**
```python
import os, requests, textwrap, json
from typing import List

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TARGET_REPO = os.getenv("GITHUB_REPO", "lproux/MCP-servers-internalMSFT-and-external")
API_ROOT = ...
```

#### Expected Outcome
- **Type:** deployment
- **Summary:** Azure resource deployment should succeed
- **Success Indicators:** Successfully deployed, Deployment complete, ✅
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Azure resource deployment should succeed
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 01: Additional Tests - Error Handling

### Cell 109 ❌ NEEDS FIX

**Source Preview:**
```python
# Test invalid model
try:
    client.chat.completions.create(
        model='invalid-model',
        messages=[{'role': 'user', 'content': 'test'}]
    )
except Exception as e:
    print(f'Expected er...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 01: Test - Max Tokens Limiting

### Cell 111 ❌ NEEDS FIX

**Source Preview:**
```python
for max_tokens in [10, 50, 100]:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'Explain AI'}],
        max_tokens=max_tokens...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 01: Test - Temperature Variations

### Cell 113 ❌ NEEDS FIX

**Source Preview:**
```python
for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'Write a creative sentence'}],
        ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 01: Test - System Prompts

### Cell 115 ❌ NEEDS FIX

**Source Preview:**
```python
system_prompts = [
    'You are a helpful assistant.',
    'You are a sarcastic comedian.',
    'You are a professional technical writer.',
    'You are a poet.'
]

for prompt in system_prompts:
    r...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 01: Test - Multi-turn Conversation

### Cell 117 ❌ NEEDS FIX

**Source Preview:**
```python
conversation = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': 'What is Azure?'},
]

# Turn 1
response = client.chat.completions.create(
    model=...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 02: Test - Concurrent Requests

### Cell 119 ❌ NEEDS FIX

**Source Preview:**
```python
import concurrent.futures

def make_request(i):
    start = time.time()
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Requ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 02: Test - Failover Simulation

### Cell 121 ❌ NEEDS FIX

**Source Preview:**
```python
print('Testing failover behavior...')
for i in range(15):
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content':...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 02: Test - Load Distribution Analysis

### Cell 123 ❌ NEEDS FIX

**Source Preview:**
```python
# Simulate high load
load_results = []
for i in range(50):
    start = time.time()
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'conte...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 19: Test - Cache Hit Rate Analysis

### Cell 125 ❌ NEEDS FIX

**Source Preview:**
```python
cache_stats = {'hits': 0, 'misses': 0}
test_questions = [
    'What is Python?',
    'Explain Python programming',
    'Tell me about Python language'
]

for i in range(30):
    q = random.choice(test...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 19: Test - Redis Connection

### Cell 127 ❌ NEEDS FIX

**Source Preview:**
```python
import redis.asyncio as redis

# Resolve Redis connection settings without redefining earlier variables if already present
# Prefer existing globals, then environment (.env / master-lab.env), then ste...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 22: Test - Multiple Image Styles

### Cell 129 ❌ NEEDS FIX

**Source Preview:**
```python
prompts = [
    'A serene mountain landscape at dawn',
    'Abstract geometric patterns in blue and gold',
    'A cyberpunk city street at night'
]

for i, prompt in enumerate(prompts):
    print(f'Ge...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 22: Test - Image Analysis

### Cell 131 ❌ NEEDS FIX

**Source Preview:**
```python
# Use GPT-4o (multimodal) to analyze generated image
# (assuming we have a generated image from previous test)
print('Image generation and analysis complete')
utils.print_ok('Lab 22 fully tested!')

```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 03: Advanced Logging Tests

### Cell 133 ❌ NEEDS FIX

**Source Preview:**
```python
# Query logs
print('Check Azure Portal -> Log Analytics for detailed logs')
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 04: Token Usage Analytics

### Cell 135 ❌ NEEDS FIX

**Source Preview:**
```python
usage_data = []
for i in range(20):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Test {i}'}],
        max_tokens=random.r...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 05: Rate Limit Testing with Delays

### Cell 137 ❌ NEEDS FIX

**Source Preview:**
```python
for delay in [0.1, 0.5, 1.0]:
    print(f'Testing with {delay}s delay...')
    for i in range(5):
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messag...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Rate limit applied, 429 Too Many Requests
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 06: Test Multiple Authentication Scenarios

### Cell 139 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab 11: Spotify MCP Integration (updated with agent dependency safety)
# Demonstrates music service integration via MCP
# Adds a lightweight dependency check for openai-agents compatibility.

import...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 07: Content Safety - Multiple Test Cases

### Cell 141 ❌ NEEDS FIX

**Source Preview:**
```python
test_prompts = [
    ('Safe: Weather question', 'What is the weather today?'),
    ('Safe: Recipe', 'How to bake cookies?'),
    ('Test: Borderline', 'Tell me about conflicts'),
    ('Safe: Education'...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Content filtered, Safety check passed
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 08: Model Routing - Performance Comparison

### Cell 143 ❌ NEEDS FIX

**Source Preview:**
```python
models = ['gpt-4o-mini', 'gpt-4.1-mini', 'gpt-4.1']
results = []

for model in models:
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{'r...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 09: AI Foundry SDK - Streaming

### Cell 145 ❌ NEEDS FIX

**Source Preview:**
```python
print('Testing Foundry SDK streaming...')
response = inference_client.complete(
    messages=[UserMessage(content='Count to 10')],
    model='gpt-4o-mini',
    stream=True
)

for chunk in response:
  ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 11: MCP - List All Server Tools

### Cell 149 ❌ NEEDS FIX

**Source Preview:**
```python
# List all configured MCP servers and attempt to list their tools (HTTP JSON-RPC to /mcp/)
def list_all_mcp_servers_and_tools():
    if not MCP_SERVERS:
        print('[ERROR] MCP_SERVERS dict is empt...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 12: MCP from API - Test Multiple Servers

### Cell 151 ❌ NEEDS FIX

**Source Preview:**
```python
# Fix: 'mcp_servers' not defined. Reuse existing 'mcp_urls' if already built,
# otherwise construct from MCP_SERVERS dict (available globally) or step4_outputs.
if 'mcp_urls' in globals() and isinstan...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 13: MCP Client Authorization

### Cell 153 ❌ NEEDS FIX

**Source Preview:**
```python
# MCP OAuth authorization test with APIM (Cell 99)

print("=== MCP Authorization Test ===")

# Reuse existing credential (ClientSecretCredential) and MCP_SERVERS
if 'credential' not in globals():
    ...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 14: A2A Agents - Multi-Agent Communication

### Cell 155 ❌ NEEDS FIX

**Source Preview:**
```python
# Agent-to-Agent (A2A) communication test via existing agent outputs and LLM refinement
print('Testing A2A agent communication...')

required = ['planner', 'critic', 'summarizer']
missing = [r for r i...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Agent response, Tool used, Task completed
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 15: OpenAI Agents - Create Assistant

### Cell 157 ❌ NEEDS FIX

**Source Preview:**
```python
# Using Azure AI Agents (fallback stub if project_client is not defined)

if 'project_client' not in globals():
    # Minimal in-memory stub to avoid NameError and simulate Agents API behavior
    imp...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Agent response, Tool used, Task completed
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 16: AI Agent Service - Multiple Agents

### Cell 159 ❌ NEEDS FIX

**Source Preview:**
```python
import time

# Multi-agent scenario (planning, critic, summarizer) using existing agents_client + client
print('AI Agent Service: multi-agent test...')

# Create agents
agents = {
    'planner': agent...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Agent response, Tool used, Task completed
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 18: Function Calling - Multiple Functions

### Cell 161 ❌ NEEDS FIX

**Source Preview:**
```python
functions = [
    {
        'name': 'get_weather',
        'description': 'Get weather for a location',
        'parameters': {
            'type': 'object',
            'properties': {
              ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 19: Semantic Caching - Cache Invalidation Test

### Cell 163 ❌ NEEDS FIX

**Source Preview:**
```python
# Test cache with varying prompts
base_prompt = 'Explain machine learning'
variations = [
    'Explain machine learning',
    'Describe machine learning',
    'What is machine learning?',
    'Tell me...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Cache hit, Cache miss, Semantic match
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 20: Message Storing - Store and Retrieve

### Cell 165 ❌ NEEDS FIX

**Source Preview:**
```python
# Cosmos DB message storage (uses existing env + step outputs; avoids printing secrets)

from azure.cosmos import CosmosClient, PartitionKey  # new import

# Resolve endpoint/key (prefer existing vars...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 21: Vector Searching - Create and Search Index

### Cell 167 ❌ NEEDS FIX

**Source Preview:**
```python
from azure.search.documents.indexes.models import SearchIndex, SearchField  # keep existing import

# === Create (or confirm) index via APIM ===
index_name = 'test-index'
search_endpoint = (globals()....
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 22: Image Generation - Batch Generation

### Cell 169 ❌ NEEDS FIX

**Source Preview:**
```python
prompts = [
    'A peaceful zen garden',
    'Abstract art with vibrant colors',
    'Futuristic technology'
]

for i, prompt in enumerate(prompts[:2]):  # Generate first 2
    print(f'\nGenerating: {...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 24: FinOps Framework - Cost Analysis

### Cell 171 ❌ NEEDS FIX

**Source Preview:**
```python
# Simulate cost tracking
costs = []
for i in range(10):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'test'}],
        max_...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab 25: Secure Responses API

### Cell 173 ❌ NEEDS FIX

**Source Preview:**
```python
# Test secure response handling
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Test secure response'}],
    max_tokens=20
)
print(f'Secu...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 174 ❌ NEEDS FIX

**Source Preview:**
```python
secure_policy_xml_file = "secure-policy.xml"

with open(secure_policy_xml_file, 'r') as file:
    policy_xml = file.read()
    policy_xml = policy_xml.replace('{backend-id}', backend_id)
    utils.upd...
```

#### Expected Outcome
- **Type:** general
- **Summary:** Should: Task completes successfully
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should: Task completes successfully
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 176 ❌ NEEDS FIX

**Source Preview:**
```python
import json, requests, time

access_token = None

def pretty_out(resp):
    utils.print_response_code(response)
    print(f"Response headers: {json.dumps(dict(response.headers), indent = 4)}")
    if ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 178 ❌ NEEDS FIX

**Source Preview:**
```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Get an ARM (management) access token via get_bearer_token_provider
token_provid...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 180 ❌ NEEDS FIX

**Source Preview:**
```python
import pandas as pd

query = "let llmHeaderLogs = ApiManagementGatewayLlmLog \
| where DeploymentName != ''; \
let llmLogsWithSubscriptionId = llmHeaderLogs \
| join kind=leftouter ApiManagementGatewa...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 All 31 Labs Tested Successfully!

### Cell 182 ❌ NEEDS FIX

**Source Preview:**
```python
print('='*60)
print('MASTER LAB TESTING COMPLETE')
print('='*60)
print('\nSummary:')
print('  - 31 labs tested')
print('  - All features validated')
print('  - Ready for production use')
print('\nNext...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Extra Cells

### Cell 185 ❌ NEEDS FIX

**Source Preview:**
```python
import os, pathlib
TENANT_ID = "2b9d9f47-1fb6-400a-a438-39fe7d768649"
os.environ["AZURE_TENANT_ID"] = TENANT_ID
print(f"AZURE_TENANT_ID exported: {TENANT_ID}")
# Ensure .env has the tenant id (already...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Image & Vision Initialization (Inline Plan)

### Cell 187 ❌ NEEDS FIX

**Source Preview:**
```python
import os, json, time, requests
from typing import Optional

# Endpoint Discovery: attempt to infer native Azure OpenAI endpoint and list models.
# Sets OPENAI_ENDPOINT if successful; otherwise leaves...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 188 ❌ NEEDS FIX

**Source Preview:**
```python
import base64, math

# Image & Vision Model Initialization
# Chooses direct Azure OpenAI endpoint (if discovered) else APIM gateway route.

IMAGE_MODEL = globals().get('DALL_E_DEPLOYMENT') or os.envir...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 189 ❌ NEEDS FIX

**Source Preview:**
```python
# Test Image Generation (Minimal)
TEST_PROMPT = "A tiny sketch of a futuristic Azure data center shaped like a cloud, line art"
print(f"[test] Attempting generation with model={IMAGE_MODEL} source={SO...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 190 ❌ NEEDS FIX

**Source Preview:**
```python
# Set Azure OpenAI resource name manually if not discovered
# Replace PLACEHOLDER_RESOURCE with your actual Azure OpenAI resource (e.g., aoai-master-lab or openai-xyz123)
resource_name = os.environ.ge...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 191 ❌ NEEDS FIX

**Source Preview:**
```python

```

#### Expected Outcome
- **Type:** general
- **Summary:** Should: Task completes successfully
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should: Task completes successfully
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 192 ❌ NEEDS FIX

**Source Preview:**
```python

```

#### Expected Outcome
- **Type:** general
- **Summary:** Should: Task completes successfully
- **Success Indicators:** ✅, Success, Complete
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should: Task completes successfully
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Exercise 6.1: Function Calling with MCP Tools

### Cell 197 ❌ NEEDS FIX

**Source Preview:**
```python
# Exercise 6.1 & 6.2: Function Calling with MCP Tools (enhanced diagnostics)
# Architecture: MCP connects directly to server, OpenAI goes through APIM

import json
import asyncio
import time
from mcp ...
```

#### Expected Outcome
- **Type:** mcp_tool_call
- **Summary:** MCP tool should execute and return results
- **Success Indicators:** result, success, data
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: MCP tool should execute and return results
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 198 ❌ NEEDS FIX

**Source Preview:**
```python
# Advanced MCP Server Diagnostics Cell - FIND THE CORRECT MCP ENDPOINT

import httpx
import asyncio
import json
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSessi...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Exercise 6.2: Microsoft Agent Framework with MCP

### Cell 200 ❌ NEEDS FIX

**Source Preview:**
```python
# Exercise 4.1: Microsoft Agent Framework with MCP
# This cell uses the higher-level agent framework to achieve the same goal.
# It abstracts away the manual tool calling loop.

from agent_framework._...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Exercise 6.4: Semantic Kernel Agent with MCP

### Cell 203 ❌ NEEDS FIX

**Source Preview:**
```python
import asyncio
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Exercise 7.3: JWT Token Validation

### Cell 210 ❌ NEEDS FIX

**Source Preview:**
```python
policy_xml_file = "src/github/apim-api/auth-client-policy.xml"

with open(policy_xml_file, 'r') as file:
    policy_xml = file.read()
    utils.update_api_operation_policy(subscription_id, resource_gr...
```

#### Expected Outcome
- **Type:** general
- **Summary:** Should: All tests pass
- **Success Indicators:** ✅, Test passed, Success
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should: All tests pass
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 211 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab: JWT Validation Configuration
# Deploy JWT validation policy for OAuth authentication scenarios

import os
import subprocess
import shutil
import time
import tempfile

def get_az_cli():
    """F...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Duplicate function definition found - should use Cell 5 instead
- **Discrepancies:** Duplicate get_az_cli() function

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---

### Cell 212 ❌ NEEDS FIX

**Source Preview:**
```python
# Unauthenticated call should fail with 401 Unauthorized
import requests
utils.print_info("Calling sse endpoint WITHOUT authorization...")
response = requests.get(f"{apim_resource_gateway_url}/github/...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 213 ❌ NEEDS FIX

**Source Preview:**
```python
import requests
# Authenticated call should succeed
utils.print_info("Calling sse endpoint WITH authorization...")
output = utils.run("az account get-access-token --resource \"https://azure-api.net/au...
```

#### Expected Outcome
- **Type:** api_call
- **Summary:** API call should succeed with valid response
- **Success Indicators:** 200, success, response
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Exercise 2.3: Sales Analysis via MCP + AI ONLY

### Cell 218 ❌ NEEDS FIX

**Source Preview:**
```python
# This cell acts as a fallback if the primary MCP analysis in the previous cell fails.

if 'sales_data_info' not in locals() or not sales_data_info:
    print("⚠️ MCP analysis failed or returned no da...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 220 ❌ NEEDS FIX

**Source Preview:**
```python
# Exercise 2.4: Azure Cost Analysis via MCP
print(" Azure Cost Analysis via MCP Server + Azure OpenAI")
print("=" * 80)

try:
    # Define the specific cost file to use
    cost_file_path = Path("./sa...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 221 ❌ NEEDS FIX

**Source Preview:**
```python
# Exercise 2.5: Dynamic Column Analysis
print(" Dynamic MCP Analysis with User-Defined Columns")
print("=" * 80)

try:
    # --- Define columns for analysis ---
    # These variables can be changed to...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** MCP server ready, Tool executed, Result returned
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Lab: Consolidated Policy - All Features Combined

### Cell 224 ❌ NEEDS FIX

**Source Preview:**
```python
# Lab: Consolidated Policy Configuration
# Deploy comprehensive policy combining JWT validation, token rate limiting, logging, and error handling

import os
import subprocess
import shutil
import time...
```

#### Expected Outcome
- **Type:** function_definition
- **Summary:** Should NOT define get_az_cli() - use Cell 5 instead
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** HIGH
- **Reasoning:** Duplicate function definition found - should use Cell 5 instead
- **Discrepancies:** Duplicate get_az_cli() function

#### 💡 Recommended Fix
- **Type:** `remove_duplicate_function`
- **Priority:** HIGH
- **Confidence:** HIGH
- **Description:** Remove get_az_cli() function - use Cell 5 instead

**Fix Code:**
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

---

### Cell 225 ❌ NEEDS FIX

**Source Preview:**
```python
# Deploy Consolidated Policy to APIM
import os
from pathlib import Path

print("="*80)
print("DEPLOYING CONSOLIDATED POLICY")
print("="*80)
print()

# Policy file path
policy_file = Path("policies/con...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Rate limit applied, 429 Too Many Requests
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 226 ❌ NEEDS FIX

**Source Preview:**
```python
# Test Consolidated Policy
import requests
import json
from openai import AzureOpenAI

print("="*80)
print("TESTING CONSOLIDATED POLICY")
print("="*80)
print()

# Get configuration
apim_gateway_url = ...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Rate limit applied, 429 Too Many Requests
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---

### Cell 227 ❌ NEEDS FIX

**Source Preview:**
```python
# AzureOpenAI Compatibility Import Shim
# Some cells use: from openai import AzureOpenAI
# Provide a unified accessor that can adapt if future SDK reorganizes paths.

def get_azure_openai_client(**kwa...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Rate limit applied, 429 Too Many Requests
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 📂 Agent Framework Version Alignment

### Cell 229 ❌ NEEDS FIX

**Source Preview:**
```python
# Post-Upgrade Verification for Agents and AzureOpenAI
import importlib, json

ver_openai = None
try:
    import openai
    ver_openai = getattr(openai, '__version__', 'unknown')
except Exception as e...
```

#### Expected Outcome
- **Type:** output_display
- **Summary:** Should display information without errors
- **Success Indicators:** Agent response, Tool used, Task completed
- **Should Have Errors:** No

#### Actual Outcome
- **Type:** no_output
- **Summary:** Cell has no output (may not have been executed)
- **Has Output:** No
- **Has Error:** No

#### Comparison
- **Matches Expected:** ❌ No
- **Confidence:** MEDIUM
- **Reasoning:** No output - cell may not have been executed yet
- **Discrepancies:** Missing output

#### 💡 Recommended Fix
- **Type:** `manual_investigation`
- **Priority:** MEDIUM
- **Confidence:** LOW
- **Description:** Requires manual investigation

**Fix Code:**
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

---


## 🔧 Consolidated Fixes

This section consolidates all recommended fixes for easy application.

### High Priority Fixes (Apply First)

#### Cell 38: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

#### Cell 45: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

#### Cell 55: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

#### Cell 64: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

#### Cell 99: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

#### Cell 102: Add environment variable validation
```python
# Add at top of cell:
import os
required_vars = ['RESOURCE_GROUP', 'APIM_GATEWAY_URL']  # Adjust as needed
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing: {missing}. Run Cell 3 (Environment Loader) first")
    raise RuntimeError(f"Missing environment variables: {missing}")
```

#### Cell 104: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

#### Cell 211: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

#### Cell 224: Remove get_az_cli() function - use Cell 5 instead
```python
# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()
```

### Medium Priority Fixes

#### Cell 39: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Success - found indicators: Success
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 41: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Has output but unclear if successful
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 57: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Error occurred: SystemExit
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 59: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Has output but unclear if successful
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 69: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Success - found indicators: Success, Complete
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 71: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 72: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 73: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 75: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 77: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 79: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 81: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 83: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 86: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 88: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 89: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 92: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Error occurred (type unknown)
# Discrepancies: Error occurred when success expected
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 94: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Has output but unclear if successful
# Discrepancies: Success indicators missing
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 100: Fix endpoint URL (404 Not Found)
```python
# Check endpoint URL:
# - Verify API is deployed
# - Check path is correct
# - Ensure APIM gateway URL is correct
print(f"Endpoint: {url}")  # Add debugging
```

#### Cell 105: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 106: Requires manual investigation
```python
# Analysis:
# Expected: Azure resource deployment should succeed
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 109: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 111: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 113: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 115: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 117: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 119: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 121: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 123: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 125: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 127: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 129: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 131: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 133: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 135: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 137: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 139: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 141: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 143: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 145: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 149: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 151: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 153: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 155: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 157: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 159: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 161: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 163: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 165: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 167: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 169: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 171: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 173: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 174: Requires manual investigation
```python
# Analysis:
# Expected: Should: Task completes successfully
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 176: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 178: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 180: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 182: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 185: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 187: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 188: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 189: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 190: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 191: Requires manual investigation
```python
# Analysis:
# Expected: Should: Task completes successfully
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 192: Requires manual investigation
```python
# Analysis:
# Expected: Should: Task completes successfully
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 197: Requires manual investigation
```python
# Analysis:
# Expected: MCP tool should execute and return results
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 198: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 200: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 203: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 210: Requires manual investigation
```python
# Analysis:
# Expected: Should: All tests pass
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 212: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 213: Requires manual investigation
```python
# Analysis:
# Expected: API call should succeed with valid response
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 218: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 220: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 221: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 225: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 226: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 227: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

#### Cell 229: Requires manual investigation
```python
# Analysis:
# Expected: Should display information without errors
# Actual: Cell has no output (may not have been executed)
# Discrepancies: Missing output
# Recommendation: Review cell code and output, apply targeted fix
```

### Fixes by Type

- **add_env_var_check:** 1 cells (102)
- **fix_endpoint:** 1 cells (100)
- **manual_investigation:** 78 cells (39, 41, 57, 59, 69, 71, 72, 73, 75, 77, 79, 81, 83, 86, 88, 89, 92, 94, 105, 106, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 174, 176, 178, 180, 182, 185, 187, 188, 189, 190, 191, 192, 197, 198, 200, 203, 210, 212, 213, 218, 220, 221, 225, 226, 227, 229)
- **remove_duplicate_function:** 8 cells (38, 45, 55, 64, 99, 104, 211, 224)

---

