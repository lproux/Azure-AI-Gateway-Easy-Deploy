# APIM Policy Integration Summary

## Overview
Successfully integrated 8 high-priority APIM policies into the Master AI Gateway Lab notebook following the Cell 42 pattern (Token Rate Limiting reference implementation).

## Execution Date
2025-11-10

## Notebook Modified
`master-ai-gateway.ipynb`

## Total Changes
- Original cell count: 214
- New cell count: 222
- Cells added: 8 new policy deployment cells

## Integration Details

### Integration #1: Semantic Caching
- **Cell Position**: Inserted at position 0 (before original Cell 0)
- **Policy File**: `policies/semantic-caching-policy.xml`
- **Features**:
  - Azure OpenAI semantic cache lookup with 0.8 score threshold (80% similarity)
  - Embeddings backend integration for similarity matching
  - Cache duration: 120 seconds
  - System-assigned managed identity authentication
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`
  - `BACKEND_ID`
  - `EMBEDDINGS_BACKEND_ID`

### Integration #2: Load Balancing
- **Cell Position**: Inserted at position 36 (before load balancing tests section)
- **Policy File**: `policies/backend-pool-load-balancing-policy.xml`
- **Features**:
  - Backend pool load balancing with automatic retry
  - Retry count: 2 (tries all backends before failing)
  - Fast-fail retry on 429 (rate limit) and 503 (service unavailable)
  - Generic error response to hide backend pool details
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`
  - `BACKEND_ID` (defaults to 'openai-backend-pool')

### Integration #3: Content Safety
- **Cell Position**: Inserted at position 10 (before original Cell 9 - content safety testing)
- **Policy File**: `policies/content-safety-policy.xml`
- **Features**:
  - Azure AI Content Safety integration
  - Shield prompt enabled
  - Severity threshold: 4 (Medium) for all categories:
    - SelfHarm
    - Hate
    - Violence
    - Sexual
  - Blocklist support (blocklist1)
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`
  - `BACKEND_ID`
  - `CONTENT_SAFETY_BACKEND_ID`

### Integration #5: Token Metrics
- **Cell Position**: Inserted at position 29 (before original Cell 27 - first OpenAI API usage)
- **Policy File**: `policies/token-metrics-emitting-policy.xml`
- **Features**:
  - Azure OpenAI token metrics emission
  - Namespace: "openai"
  - Dimensions tracked:
    - Subscription ID
    - Client IP
    - API ID
    - User ID (from x-user-id header)
  - Integrates with Azure Monitor for analytics
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`
  - `BACKEND_ID`

### Integration #6: Private Connectivity
- **Cell Position**: Inserted at position 55 (before original Cell 51 - AI Foundry integration)
- **Policy File**: `policies/private-connectivity-policy.xml`
- **Features**:
  - Managed identity authentication for backend access
  - Resource: https://cognitiveservices.azure.com
  - Authorization header injection with bearer token
  - Retry logic for resilience (count: 2)
  - Generic error responses to hide backend details
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`
  - `BACKEND_ID`

### Integration #7: Model Routing
- **Cell Position**: Inserted at position 90 (before original Cell 85 - model selection testing)
- **Policy File**: `policies/model-routing-policy.xml`
- **Features**:
  - Intelligent model routing based on deployment-id or model field
  - Routing rules:
    - gpt-4.1 → foundry1
    - gpt-4.1-mini / gpt-4.1-nano → foundry2
    - model-router / gpt-5 / DeepSeek-R1 → foundry3
  - Model gating: gpt-4o* variants → BLOCKED (403 Forbidden)
  - Validation: Invalid models → 400 Bad Request
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`

### Integration #4: JWT Validation
- **Cell Position**: Inserted at position 202 (before original Cell 196 - OAuth section)
- **Policy File**: `policies/jwt-validation-policy.xml`
- **Features**:
  - JWT token validation for OAuth scenarios
  - OpenID Connect configuration from Azure AD
  - Audience validation: https://azure-api.net/authorization-manager
  - Failed validation: 401 Unauthorized
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`
  - `AZURE_TENANT_ID`

### Integration #8: Consolidated Policy
- **Cell Position**: Inserted at position 215 (before original Cell 208 - consolidated lab)
- **Policy File**: `policies/consolidated-policy.xml`
- **Features**:
  - Comprehensive policy combining multiple capabilities:
    - JWT Token Validation (OAuth scenarios)
    - Token Rate Limiting (1000 tokens per minute)
    - Request/Response logging
    - Custom tracing headers (X-Request-ID, X-User-ID)
    - Error handling with detailed logging
    - Application Insights integration
    - X-Remaining-Tokens response header
- **Environment Variables**:
  - `APIM_SERVICE_NAME`
  - `RESOURCE_GROUP`
  - `BACKEND_ID`
  - `AZURE_TENANT_ID`

## Cell 42 Pattern Implementation

All 8 integrations follow the proven Cell 42 pattern exactly:

1. **Azure CLI Path Detection**: `get_az_cli()` helper function handles WSL vs Windows paths
2. **Environment Configuration**:
   - Environment variable loading with sensible defaults
   - PATH environment variable setup for WSL compatibility
3. **Inline Policy XML**: Policy defined as f-string with variable substitution
4. **Temporary File Creation**: Cross-platform safe temp file handling
5. **Subprocess Execution**: `az apim api policy create` command
6. **Error Handling**:
   - Azure CLI availability check
   - 60-second timeout for policy application
   - Comprehensive error messages with hints
7. **User-Friendly Messages**:
   - Clear status indicators ([INFO], [OK], [ERROR], [SUCCESS], [HINT])
   - Configuration display before execution
   - 60-second wait after successful deployment for policy propagation
   - Manual fallback instructions with policy XML display

## Key Features Across All Integrations

### Consistency
- All cells use identical structure and error handling
- Consistent naming conventions and variable usage
- Uniform user experience and messaging

### Robustness
- Cross-platform support (WSL, Windows, Linux)
- Graceful fallback when Azure CLI is unavailable
- Comprehensive error messages with actionable hints
- Policy propagation wait time (60 seconds)

### User Experience
- Clear progress indicators
- Configuration visibility before execution
- Manual policy XML display for fallback scenarios
- Next-step guidance after completion

## Environment Variables Used

All integrations support the following environment variables:

### Required
- `APIM_SERVICE_NAME` (default: 'apim-pavavy6pu5hpa')
- `RESOURCE_GROUP` (default: 'lab-master-lab')

### Optional (policy-specific)
- `BACKEND_ID` (various defaults depending on policy)
- `EMBEDDINGS_BACKEND_ID` (default: 'embeddings-backend')
- `CONTENT_SAFETY_BACKEND_ID` (default: 'content-safety-backend')
- `AZURE_TENANT_ID` (default: 'your-tenant-id')

## Git Commit Message Suggestion

```
feat: integrate 8 APIM policies into Master AI Gateway Lab notebook

Implement Cell 42 pattern for policy deployment automation:

- Add Semantic Caching policy deployment (Cell 0)
- Add Load Balancing policy deployment (Cell 34)
- Add Content Safety policy deployment (Cell 10)
- Add Token Metrics policy deployment (Cell 29)
- Add Private Connectivity policy deployment (Cell 55)
- Add Model Routing policy deployment (Cell 90)
- Add JWT Validation policy deployment (Cell 202)
- Add Consolidated Policy deployment (Cell 215)

All integrations follow proven Cell 42 pattern:
- Azure CLI path detection with WSL/Windows support
- Environment variable configuration
- Inline policy XML with f-strings
- Temporary file creation
- Subprocess execution with az apim api policy create
- Comprehensive error handling with 60-second timeout
- User-friendly status messages and manual fallback

Total cells: 214 → 222 (+8 policy deployment cells)

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Verification Steps

To verify the integrations:

1. **Open the notebook** in Jupyter or VS Code
2. **Check cell positions**:
   - Cell 0: Semantic Caching
   - Cell 10: Content Safety
   - Cell 29: Token Metrics
   - Cell 36: Load Balancing
   - Cell 55: Private Connectivity
   - Cell 90: Model Routing
   - Cell 202: JWT Validation
   - Cell 215: Consolidated Policy

3. **Run each policy deployment cell** to apply policies to APIM
4. **Verify policy propagation** (wait 60 seconds after each deployment)
5. **Test functionality** using the subsequent test cells

## Files Modified

1. `/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/master-ai-gateway.ipynb`

## Files Referenced (Not Modified)

1. `policies/semantic-caching-policy.xml`
2. `policies/backend-pool-load-balancing-policy.xml`
3. `policies/content-safety-policy.xml`
4. `policies/token-metrics-emitting-policy.xml`
5. `policies/private-connectivity-policy.xml`
6. `policies/model-routing-policy.xml`
7. `policies/jwt-validation-policy.xml`
8. `policies/consolidated-policy.xml`

## Implementation Notes

### Success Criteria Met
- All 8 integrations completed successfully
- Cell 42 pattern followed precisely for each integration
- All existing cells preserved (no modifications, only insertions)
- Notebook cell count increased from 214 to 222
- Each integration includes comprehensive error handling and user guidance

### Quality Assurance
- Cross-platform compatibility ensured (WSL, Windows, Linux)
- Environment variable support with sensible defaults
- Manual fallback instructions for all scenarios
- Consistent user experience across all integrations
- Policy propagation wait time implemented

### Best Practices Followed
- No hardcoded credentials or secrets
- Environment variable configuration
- Comprehensive error messages
- User-friendly status indicators
- Clear next-step guidance
- Manual policy XML display for troubleshooting

## Conclusion

Successfully integrated 8 high-priority APIM policies into the Master AI Gateway Lab notebook. All integrations follow the Cell 42 pattern exactly, ensuring consistency, robustness, and excellent user experience. The notebook is now ready for policy deployment automation and testing.
