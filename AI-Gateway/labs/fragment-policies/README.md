# Azure AI Gateway - Fragment-Based Policy Management

Complete implementation of APIM policy management using **Policy Fragments**, **Feature Flags**, and **Named Values** for dynamic, reusable, and testable policy composition.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Fragment Specifications](#fragment-specifications)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Contributing](#contributing)

## Overview

This lab demonstrates advanced Azure API Management (APIM) policy management using a fragment-based architecture. Instead of monolithic inline policies, policies are broken down into reusable fragments that can be:

- **Enabled/disabled dynamically** via feature flags (Named Values)
- **Configured centrally** via configuration values (Named Values)
- **Tested independently** for validation and quality assurance
- **Deployed selectively** for A/B testing and gradual rollouts
- **Version controlled** as small, focused XML files

### Key Benefits

| Benefit | Inline Policies | Fragment Policies |
|---------|----------------|-------------------|
| **Reusability** | ❌ Copy-paste across APIs | ✅ Define once, use everywhere |
| **Maintainability** | ❌ Update each API separately | ✅ Update fragment once |
| **Feature Flags** | ❌ Modify policy XML | ✅ Toggle via Named Values |
| **Configuration** | ❌ Hardcoded in XML | ✅ Dynamic via Named Values |
| **Testing** | ❌ Redeploy entire policy | ✅ Test fragments independently |
| **Rollback** | ❌ Restore entire policy | ✅ Toggle feature flag |
| **Version Control** | ❌ Large XML diffs | ✅ Small fragment diffs |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     API Request                              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              APIM Gateway - Master Policy                    │
│                (conditional fragment includes)               │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              Feature Flags (Named Values)                    │
│   • feature-token-metrics-enabled = true                     │
│   • feature-load-balancing-enabled = true                    │
│   • feature-token-ratelimit-enabled = false                  │
│   • feature-private-connectivity-enabled = false             │
│   • feature-caching-enabled = false                          │
│   • feature-circuit-breaker-enabled = true                   │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
        ┌──────────────┴──────────────┬──────────────┐
        ↓                             ↓              ↓
┌───────────────┐          ┌──────────────┐  ┌──────────────┐
│  Fragment 1   │          │  Fragment 2  │  │  Fragment N  │
│ (if enabled)  │          │ (if enabled) │  │ (if enabled) │
└───────────────┘          └──────────────┘  └──────────────┘
```

### Master Policy Structure

```xml
<policies>
  <inbound>
    <base />
    <choose>
      <when condition="@({{named-value-feature-token-metrics-enabled}} == 'true')">
        <include-fragment fragment-id="fragment-token-metrics" />
      </when>
    </choose>
    <!-- More conditional fragment includes... -->
  </inbound>
  <backend>
    <base />
    <!-- Backend fragments... -->
  </backend>
  <outbound>
    <base />
    <!-- Outbound fragments... -->
  </outbound>
  <on-error>
    <base />
    <!-- Error handling fragments... -->
  </on-error>
</policies>
```

## Features

### 1. Policy Fragments

Six production-ready policy fragments:

| Fragment | Description | Applies To | Default State |
|----------|-------------|------------|---------------|
| **token-metrics** | Emit token consumption to Application Insights | inbound | ✅ Enabled |
| **load-balancing** | Backend pool with priority/weight-based routing | inbound, backend | ✅ Enabled |
| **token-ratelimit** | Token-per-minute (TPM) limits per subscription | inbound | ❌ Disabled |
| **private-connectivity** | Managed identity auth for private endpoints | inbound | ❌ Disabled |
| **caching** | Semantic caching with Azure Redis | inbound, outbound | ❌ Disabled |
| **circuit-breaker** | Fault tolerance and resilience pattern | inbound, on-error | ✅ Enabled |

### 2. Feature Flags

Dynamic enable/disable of policies without redeployment:

```python
# Enable token rate limiting
toggle_feature("token-ratelimit", enabled=True)

# Disable caching
toggle_feature("caching", enabled=False)
```

### 3. Centralized Configuration

All policy parameters managed via Named Values:

```json
{
  "config-token-ratelimit-tpm": "100",
  "config-cache-duration-seconds": "300",
  "config-circuit-error-threshold": "5"
}
```

### 4. Comprehensive Testing

Full pytest test suite:
- Fragment XML validation
- Feature flag configuration tests
- Master policy generation tests
- Integration tests (requires APIM)

## Project Structure

```
fragment-policies/
├── master-ai-gateway-fragment-policies.ipynb  # Main notebook (80+ cells)
├── README.md                                   # This file
│
├── fragments/                                  # Policy fragment XML files
│   ├── token-metrics.xml                       # Token consumption metrics
│   ├── load-balancing.xml                      # Backend pool load balancing
│   ├── token-ratelimit.xml                     # Token rate limiting
│   ├── private-connectivity.xml                # Managed identity auth
│   ├── caching.xml                             # Semantic caching
│   └── circuit-breaker.xml                     # Circuit breaker pattern
│
├── config/                                     # Configuration files
│   ├── fragment-config.json                    # Fragment definitions
│   └── apim-config.json                        # APIM service configuration
│
└── tests/                                      # Pytest test suite
    ├── __init__.py
    ├── conftest.py                             # Pytest configuration
    ├── test_fragments.py                       # Fragment validation tests
    ├── test_feature_flags.py                   # Feature flag tests
    └── test_master_policy.py                   # Master policy tests
```

## Prerequisites

### Required

- **Python 3.12+**
- **VS Code** with Jupyter extension
- **Azure CLI** (authenticated)
- **Azure Subscription** with Contributor + RBAC Administrator permissions
- **Existing APIM Service** (Basicv2 or higher recommended)

### Python Packages

```bash
pip install azure-mgmt-apimanagement azure-identity azure-monitor-query
pip install requests pandas matplotlib pytest
```

### Azure Resources

- Azure API Management service
- Azure AI Services (Azure OpenAI or AI Foundry)
- Application Insights (for metrics)
- Azure Redis (optional, for caching)
- Log Analytics Workspace (for monitoring)

## Quick Start

### 1. Clone and Setup

```bash
cd /path/to/AI-Gateway/labs/fragment-policies
pip install -r ../../requirements.txt
```

### 2. Configure APIM Service

Edit the notebook (Cell 19) or set environment variables:

```python
config.apim_service = "YOUR-APIM-SERVICE-NAME"
config.resource_group = "YOUR-RESOURCE-GROUP"
config.subscription_id = "YOUR-SUBSCRIPTION-ID"
```

### 3. Run the Notebook

Open `master-ai-gateway-fragment-policies.ipynb` in VS Code and:

1. **Run All** to execute sequentially
2. Or execute cells **step by step** for learning

### 4. Deploy Fragments

```python
# Cell 19: Deploy all fragments to APIM
# Fragments are deployed in dependency order
```

### 5. Configure Feature Flags

```python
# Cell 21: Deploy feature flags as Named Values
# Set default enabled/disabled states
```

### 6. Apply Master Policy

```python
# Cell 33: Generate and apply master policy to API
# Policy includes conditional fragment references
```

## Fragment Specifications

### Fragment 1: Token Metrics

**File:** `fragments/token-metrics.xml`
**Feature Flag:** `feature-token-metrics-enabled`
**Configuration:**
- `config-token-metrics-namespace` (default: "openai")

**Purpose:** Emit Azure OpenAI token consumption metrics to Application Insights with custom dimensions for tracking.

**XML:**
```xml
<fragment>
    <azure-openai-emit-token-metric namespace="{{named-value-config-token-metrics-namespace}}">
        <dimension name="Subscription ID" value="@(context.Subscription?.Id ?? 'unknown')" />
        <dimension name="Client IP" value="@(context.Request.IpAddress)" />
        <dimension name="API ID" value="@(context.Api.Id)" />
        <dimension name="User ID" value="@(context.Request.Headers.GetValueOrDefault('x-user-id', 'anonymous'))" />
    </azure-openai-emit-token-metric>
</fragment>
```

### Fragment 2: Load Balancing

**File:** `fragments/load-balancing.xml`
**Feature Flag:** `feature-load-balancing-enabled`
**Configuration:**
- `config-lb-backend-pool-id` (default: "openai-backend-pool")
- `config-lb-retry-count` (default: "2")

**Purpose:** Route requests to backend pool with priority-based failover and automatic retry on 429/503 errors.

### Fragment 3: Token Rate Limiting

**File:** `fragments/token-ratelimit.xml`
**Feature Flag:** `feature-token-ratelimit-enabled`
**Configuration:**
- `config-token-ratelimit-tpm` (default: "100")

**Purpose:** Enforce token-per-minute (TPM) limits on Azure OpenAI requests to prevent quota exhaustion.

### Fragment 4: Private Connectivity

**File:** `fragments/private-connectivity.xml`
**Feature Flag:** `feature-private-connectivity-enabled`
**Configuration:**
- `config-private-backend-id` (default: "openai-private-backend")

**Purpose:** Authenticate to Azure OpenAI using Managed Identity and route traffic through private endpoints.

### Fragment 5: Semantic Caching

**File:** `fragments/caching.xml`
**Feature Flag:** `feature-caching-enabled`
**Configuration:**
- `config-cache-duration-seconds` (default: "300")
- `config-cache-score-threshold` (default: "0.8")
- `config-cache-embeddings-backend` (default: "openai-embeddings-backend")

**Purpose:** Implement semantic caching using Azure Redis to reduce latency and backend costs.

**Note:** Requires both inbound and outbound sections.

### Fragment 6: Circuit Breaker

**File:** `fragments/circuit-breaker.xml`
**Feature Flag:** `feature-circuit-breaker-enabled`
**Configuration:**
- `config-circuit-error-threshold` (default: "5")
- `config-circuit-timeout-seconds` (default: "60")
- `config-circuit-window-seconds` (default: "120")

**Purpose:** Implement circuit breaker pattern to prevent cascading failures when backends are experiencing issues.

## Usage Examples

### Enable a Feature

```python
# Enable token rate limiting
toggle_feature("token-ratelimit", enabled=True)

# Verify status
print(config.features["token-ratelimit"])  # True
```

### Disable a Feature

```python
# Disable semantic caching
toggle_feature("caching", enabled=False)
```

### Update Configuration

```python
# Increase token rate limit to 500 TPM
create_named_value("config-token-ratelimit-tpm", "500")

# Reduce cache duration to 2 minutes
create_named_value("config-cache-duration-seconds", "120")
```

### Bulk Feature Toggle

```python
feature_changes = {
    "token-metrics": True,
    "load-balancing": True,
    "token-ratelimit": True,
    "circuit-breaker": True,
    "caching": False,
    "private-connectivity": False
}

for feature_name, enabled in feature_changes.items():
    toggle_feature(feature_name, enabled)
```

### List Deployed Fragments

```python
fragments = list_fragments()
for fragment in fragments:
    print(f"{fragment['name']}: {fragment['description']}")
```

### Export Configuration

```python
# Export all configuration to JSON
config_export = {
    "fragments": FRAGMENTS,
    "features": config.features,
    "config_values": config.config_values
}

Path("exported-config.json").write_text(json.dumps(config_export, indent=2))
```

## Testing

### Run All Tests

```bash
cd tests/
pytest -v
```

### Run Specific Test File

```bash
# Test fragments only
pytest test_fragments.py -v

# Test feature flags only
pytest test_feature_flags.py -v

# Test master policy only
pytest test_master_policy.py -v
```

### Run Integration Tests

Integration tests require APIM service access:

```bash
# Set environment variables
export APIM_SERVICE_NAME="your-apim-service"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_RESOURCE_GROUP="your-resource-group"

# Run integration tests
pytest -v -m integration
```

### Test Coverage

```bash
pytest --cov=. --cov-report=html
```

### Test Results

Expected test coverage:
- **Fragment XML validation:** 15+ tests
- **Feature flag configuration:** 12+ tests
- **Master policy generation:** 10+ tests
- **Integration tests:** 3+ tests (requires APIM)

## CI/CD Integration

### Azure DevOps Pipeline

Create `.azure-pipelines.yml`:

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: fragment-policy-config

stages:
- stage: Test
  jobs:
  - job: RunTests
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.12'

    - script: |
        pip install -r requirements.txt
        cd labs/fragment-policies/tests
        pytest -v --junitxml=test-results.xml
      displayName: 'Run Tests'

    - task: PublishTestResults@2
      inputs:
        testResultsFiles: '**/test-results.xml'
        testRunTitle: 'Fragment Policy Tests'

- stage: Deploy
  dependsOn: Test
  condition: succeeded()
  jobs:
  - job: DeployFragments
    steps:
    - task: AzureCLI@2
      displayName: 'Deploy Policy Fragments'
      inputs:
        azureSubscription: '$(azureSubscription)'
        scriptType: 'bash'
        scriptLocation: 'inlineScript'
        inlineScript: |
          # Install Python dependencies
          pip install azure-mgmt-apimanagement azure-identity

          # Run deployment script
          python deploy-fragments.py \
            --service-name $(APIM_SERVICE_NAME) \
            --resource-group $(RESOURCE_GROUP) \
            --config config/fragment-config.json
```

### GitHub Actions

Create `.github/workflows/deploy-fragments.yml`:

```yaml
name: Deploy Policy Fragments

on:
  push:
    branches: [ main ]
    paths:
      - 'labs/fragment-policies/**'
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        cd labs/fragment-policies/tests
        pytest -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Deploy Fragments
      run: |
        cd labs/fragment-policies
        python deploy-fragments.py
```

### Deployment Script

Create `deploy-fragments.py`:

```python
#!/usr/bin/env python3
"""
Deploy policy fragments to Azure APIM.
Usage: python deploy-fragments.py --service-name <apim> --resource-group <rg>
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys

def deploy_fragment(service_name, resource_group, fragment_id, xml_path, description):
    """Deploy a single fragment."""
    cmd = [
        "az", "apim", "api", "policy-fragment", "create",
        "--resource-group", resource_group,
        "--service-name", service_name,
        "--policy-fragment-id", fragment_id,
        "--description", description,
        "--value-path", str(xml_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Deploy policy fragments")
    parser.add_argument("--service-name", required=True, help="APIM service name")
    parser.add_argument("--resource-group", required=True, help="Resource group")
    parser.add_argument("--config", default="config/fragment-config.json", help="Config file")

    args = parser.parse_args()

    # Load configuration
    config = json.loads(Path(args.config).read_text())

    # Deploy fragments in order
    for fragment_id in config["deployment_order"]:
        fragment_info = config["fragments"][fragment_id]
        xml_path = Path("fragments") / Path(fragment_info["file"]).name

        print(f"Deploying {fragment_id}...")
        success = deploy_fragment(
            args.service_name,
            args.resource_group,
            fragment_id,
            xml_path,
            fragment_info["description"]
        )

        if success:
            print(f"  ✅ {fragment_id} deployed")
        else:
            print(f"  ❌ {fragment_id} failed")
            sys.exit(1)

    print("\n✅ All fragments deployed successfully")

if __name__ == "__main__":
    main()
```

## Troubleshooting

### Common Issues

#### 1. Fragment Deployment Fails

**Symptom:** `az apim api policy-fragment create` returns error

**Solutions:**
- Verify APIM service name and resource group
- Check Azure CLI authentication: `az account show`
- Ensure you have Contributor permissions on APIM service
- Validate fragment XML syntax

#### 2. Named Value Not Found

**Symptom:** Policy references `{{named-value-xxx}}` but value doesn't exist

**Solutions:**
- Run Cell 21 to deploy feature flags
- Run Cell 22 to deploy configuration values
- Verify Named Value exists: `az apim nv show --service-name <apim> --resource-group <rg> --named-value-id <name>`

#### 3. Feature Toggle Not Working

**Symptom:** Changing feature flag doesn't affect policy behavior

**Solutions:**
- Wait 30-60 seconds for APIM cache to refresh
- Clear APIM cache manually in Azure Portal
- Verify Named Value was updated: `az apim nv show`
- Check master policy includes conditional fragment references

#### 4. Circuit Breaker Always Open

**Symptom:** Circuit breaker returns 503 even when backends are healthy

**Solutions:**
- Clear circuit breaker cache values
- Reduce `config-circuit-error-threshold`
- Increase `config-circuit-timeout-seconds`
- Check backend health in APIM

#### 5. Caching Not Working

**Symptom:** Semantic cache always misses

**Solutions:**
- Verify Redis cache is deployed and accessible
- Check `config-cache-score-threshold` (lower = more permissive)
- Ensure embeddings backend is configured
- Verify cache-lookup is in inbound, cache-store in outbound

### Debug Mode

Enable detailed logging in Azure CLI:

```bash
# Set debug mode
export AZURE_CLI_DEBUG=1

# Run commands with verbose output
az apim api policy-fragment list --debug
```

### APIM Tracing

Use APIM trace tool to debug policy execution:

1. Enable tracing in Azure Portal (APIM → APIs → Test → Trace)
2. Make test request
3. View trace results to see which fragments executed

## Best Practices

### 1. Feature Flag Naming

- Use consistent prefix: `feature-{fragment-name}-enabled`
- Always include `-enabled` suffix for clarity
- Match fragment naming: `fragment-token-metrics` → `feature-token-metrics-enabled`

### 2. Fragment Design

- **Single Responsibility**: Each fragment should do one thing well
- **Self-Contained**: Fragments should not depend on execution order
- **Idempotent**: Fragments should produce same result regardless of how many times applied
- **Documented**: Include XML comments explaining purpose and behavior

### 3. Configuration Management

- Use Named Values for all configurable parameters
- Provide sensible defaults in `fragment-config.json`
- Document units (seconds, bytes, count, etc.)
- Validate ranges (e.g., cache score: 0.0-1.0)

### 4. Deployment Strategy

- **Test in Dev First**: Deploy to dev/test environment before production
- **Gradual Rollout**: Enable features for subset of users first
- **Monitor Metrics**: Watch Application Insights during rollout
- **Rollback Plan**: Keep feature flags for quick disable if issues occur

### 5. Testing Strategy

- Run unit tests before deployment
- Test fragment combinations, not just individual fragments
- Use A/B testing for performance comparison
- Monitor error rates and latency

### 6. Version Control

- Commit fragment XML files individually
- Tag releases with semantic versioning
- Document breaking changes in commit messages
- Maintain CHANGELOG.md

## Contributing

### Development Workflow

1. **Fork Repository**
2. **Create Feature Branch**: `git checkout -b feature/new-fragment`
3. **Make Changes**
4. **Write Tests**: Add tests to `tests/`
5. **Run Tests**: `pytest -v`
6. **Commit**: `git commit -m "Add new fragment: XYZ"`
7. **Push**: `git push origin feature/new-fragment`
8. **Create Pull Request**

### Adding a New Fragment

1. **Create XML File**: `fragments/my-new-fragment.xml`
2. **Update Configuration**: Add to `config/fragment-config.json`
3. **Write Tests**: Add to `tests/test_fragments.py`
4. **Document**: Update README.md with fragment specification
5. **Test**: Run full test suite
6. **Deploy**: Update notebook with new fragment

### Code Style

- **Python**: Follow PEP 8
- **XML**: Indent with 4 spaces
- **JSON**: Indent with 2 spaces
- **Comments**: Explain "why", not "what"

## License

This project is part of the Azure AI Gateway labs and follows the same license as the parent repository.

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Azure APIM Policy Reference](https://learn.microsoft.com/azure/api-management/api-management-policies)
- **Community**: [Azure APIM Forums](https://learn.microsoft.com/answers/topics/azure-api-management.html)

---


*Anthropic AI Assistant*
*Last Updated: 2025-11-11*
