# FRAGMENT-BASED POLICY NOTEBOOK - ARCHITECTURE & IMPLEMENTATION PLAN

**Status:** PLANNING PHASE
**Date:** 2025-11-11
**Parallel to:** PLAN 2 (Current Notebook Policy Fixes)

---

## EXECUTIVE SUMMARY

This document outlines a comprehensive plan for creating a **new notebook** (`master-ai-gateway-fragment-policies.ipynb`) that implements APIM policy management using **Policy Fragments** instead of inline policies.

**Key Benefits:**
- ✅ Reusable policy components across APIs
- ✅ Feature flag-based enable/disable of policies
- ✅ Centralized policy configuration via Named Values
- ✅ Easier testing and A/B testing of policies
- ✅ Simplified policy updates (change once, apply everywhere)
- ✅ Version control friendly (small XML fragments)

---

## CURRENT STATE ANALYSIS

### Current Notebook Policies (Inline)

From `master-ai-gateway-fix-MCP.ipynb`, we have 4 main policy implementations:

| Cell | Policy Name | Purpose | Location |
|------|-------------|---------|----------|
| 38 | Token Metrics | Monitor token usage with Azure Monitor dimensions | Inbound |
| 45 | Load Balancing | Backend pool with retry logic | Inbound + Backend |
| 55 | Token Rate Limiting | Limit tokens per minute per subscription | Inbound |
| 64 | Private Connectivity | Managed identity authentication | Inbound |

**Issues with Current Approach:**
- ❌ Policies embedded directly in API (hard to reuse)
- ❌ No feature flags (can't easily enable/disable)
- ❌ Configuration values hardcoded in policy XML
- ❌ Must re-apply entire policy to make changes
- ❌ Difficult to test policy changes independently

---

## FRAGMENT-BASED ARCHITECTURE

### Policy Fragment Manager Overview

Based on the provided PowerShell script, the architecture includes:

**1. Policy Fragments** - Reusable XML snippets stored in APIM
   - `fragment-token-metrics`
   - `fragment-load-balancing`
   - `fragment-token-ratelimit`
   - `fragment-private-connectivity`
   - `fragment-caching` (bonus)
   - `fragment-circuit-breaker` (bonus)

**2. Feature Flags** - Named Values controlling fragment activation
   - `feature-token-metrics-enabled` (true/false)
   - `feature-load-balancing-enabled` (true/false)
   - `feature-token-ratelimit-enabled` (true/false)
   - `feature-private-connectivity-enabled` (true/false)
   - `feature-caching-enabled` (true/false)
   - `feature-circuit-breaker-enabled` (true/false)

**3. Configuration Values** - Named Values for policy parameters
   - `token-ratelimit-tpm` (50, 100, 500, etc.)
   - `token-ratelimit-period` (60)
   - `cache-duration-seconds` (300)
   - `circuit-error-threshold` (5)
   - `circuit-timeout-seconds` (60)
   - `lb-retry-count` (2)

**4. Master Policy** - API-level policy that includes fragments conditionally
   ```xml
   <policies>
     <inbound>
       <base />
       <choose>
         <when condition="@(context.Variables.GetValueOrDefault<string>(\"feature-token-metrics-enabled\", \"false\") == \"true\")">
           <include-fragment fragment-id="fragment-token-metrics" />
         </when>
       </choose>
       <choose>
         <when condition="@(context.Variables.GetValueOrDefault<string>(\"feature-load-balancing-enabled\", \"false\") == \"true\")">
           <include-fragment fragment-id="fragment-load-balancing" />
         </when>
       </choose>
       <!-- ...more fragments... -->
     </inbound>
     <backend>
       <base />
     </backend>
     <outbound>
       <base />
     </outbound>
     <on-error>
       <base />
     </on-error>
   </policies>
   ```

---

## NEW NOTEBOOK STRUCTURE

### Filename: `master-ai-gateway-fragment-policies.ipynb`

### Section 0: Setup & Configuration (Cells 1-10)

**Cell 1:** Markdown - Introduction
```markdown
# Azure AI Gateway - Policy Fragment Management

This notebook demonstrates advanced APIM policy management using Policy Fragments,
Feature Flags, and Named Values for dynamic, reusable policy composition.
```

**Cell 2:** Imports & Environment Setup
```python
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
```

**Cell 3:** Configuration Class
```python
class FragmentPolicyConfig:
    """Configuration for fragment-based policy management."""

    # APIM Service Details
    subscription_id: str
    resource_group: str
    apim_service: str
    api_id: str = "azure-openai-api"

    # Feature Flags
    features: Dict[str, bool] = {
        "token-metrics": True,
        "load-balancing": True,
        "token-ratelimit": False,  # Off by default for testing
        "private-connectivity": True,
        "caching": False,
        "circuit-breaker": True
    }

    # Configuration Values
    config_values: Dict[str, str] = {
        "token-ratelimit-tpm": "100",
        "cache-duration-seconds": "300",
        "circuit-error-threshold": "5",
        "lb-retry-count": "2"
    }
```

**Cell 4:** Fragment Definitions
```python
FRAGMENTS = {
    "fragment-token-metrics": {
        "description": "Azure OpenAI token metrics emission",
        "xml_template": "fragments/token-metrics.xml",
        "applies_to": ["inbound"]
    },
    "fragment-load-balancing": {
        "description": "Backend pool load balancing with retry",
        "xml_template": "fragments/load-balancing.xml",
        "applies_to": ["inbound", "backend"]
    },
    "fragment-token-ratelimit": {
        "description": "Token-based rate limiting",
        "xml_template": "fragments/token-ratelimit.xml",
        "applies_to": ["inbound"]
    },
    "fragment-private-connectivity": {
        "description": "Managed identity authentication",
        "xml_template": "fragments/private-connectivity.xml",
        "applies_to": ["inbound"]
    },
    "fragment-caching": {
        "description": "Semantic caching with Redis",
        "xml_template": "fragments/caching.xml",
        "applies_to": ["inbound", "outbound"]
    },
    "fragment-circuit-breaker": {
        "description": "Circuit breaker pattern",
        "xml_template": "fragments/circuit-breaker.xml",
        "applies_to": ["backend", "on-error"]
    }
}
```

**Cells 5-10:** Helper functions
- `deploy_fragment(fragment_id, xml_content, description)`
- `create_named_value(name, value, secret=False)`
- `toggle_feature(feature_name, enabled: bool)`
- `apply_master_policy(api_id, fragment_ids)`
- `list_fragments()`
- `test_fragment_configuration()`

---

### Section 1: Fragment Deployment (Cells 11-20)

**Cell 11:** Markdown - Fragment XML Templates

**Cell 12-17:** Create Fragment XML Files (one cell per fragment)

**Cell 12:** Token Metrics Fragment
```python
token_metrics_xml = """<fragment>
    <azure-openai-emit-token-metric namespace="{{{{named-value-token-metrics-namespace}}}}">
        <dimension name="Subscription ID" value="@(context.Subscription.Id)" />
        <dimension name="Client IP" value="@(context.Request.IpAddress)" />
        <dimension name="API ID" value="@(context.Api.Id)" />
        <dimension name="User ID" value="@(context.Request.Headers.GetValueOrDefault(&quot;x-user-id&quot;, &quot;N/A&quot;))" />
    </azure-openai-emit-token-metric>
</fragment>"""

# Save to file
Path("fragments").mkdir(exist_ok=True)
Path("fragments/token-metrics.xml").write_text(token_metrics_xml)
```

**Cell 13:** Load Balancing Fragment
```python
load_balancing_xml = """<fragment>
    <set-backend-service backend-id="{{{{named-value-backend-pool-id}}}}" />
    <!-- Retry logic in backend section -->
</fragment>"""

Path("fragments/load-balancing.xml").write_text(load_balancing_xml)
```

**Cell 14-17:** Other fragments (token-ratelimit, private-connectivity, caching, circuit-breaker)

**Cell 18:** Deploy All Fragments
```python
print('[*] Deploying all policy fragments to APIM...')

for fragment_id, fragment_info in FRAGMENTS.items():
    xml_path = fragment_info["xml_template"]
    description = fragment_info["description"]

    if Path(xml_path).exists():
        xml_content = Path(xml_path).read_text()
        success = deploy_fragment(fragment_id, xml_content, description)

        if success:
            print(f'  [OK] {fragment_id}')
        else:
            print(f'  [FAIL] {fragment_id}')
    else:
        print(f'  [SKIP] {fragment_id} - XML file not found')

print('[OK] Fragment deployment complete')
```

**Cell 19:** Verify Fragment Deployment
```python
fragments = list_fragments()
print(f'[*] Total fragments deployed: {len(fragments)}')

for fragment in fragments:
    print(f'  - {fragment["id"]}: {fragment["description"]}')
```

---

### Section 2: Feature Flags & Configuration (Cells 20-30)

**Cell 20:** Markdown - Feature Flag Explanation

**Cell 21:** Deploy Feature Flags as Named Values
```python
print('[*] Deploying feature flags as Named Values...')

for feature_name, enabled in config.features.items():
    named_value_name = f"feature-{feature_name}-enabled"
    value = "true" if enabled else "false"

    success = create_named_value(named_value_name, value, secret=False)

    status = "✅ ENABLED" if enabled else "❌ DISABLED"
    print(f'  [{status}] {feature_name}')

print('[OK] Feature flags deployed')
```

**Cell 22:** Deploy Configuration Values
```python
print('[*] Deploying configuration values as Named Values...')

for config_name, config_value in config.config_values.items():
    named_value_name = f"config-{config_name}"

    success = create_named_value(named_value_name, config_value, secret=False)
    print(f'  [OK] {config_name} = {config_value}')

print('[OK] Configuration values deployed')
```

**Cell 23:** View All Named Values
```python
# List all named values in APIM
named_values = list_named_values()

features = [nv for nv in named_values if nv["name"].startswith("feature-")]
configs = [nv for nv in named_values if nv["name"].startswith("config-")]

print('[*] Feature Flags:')
for nv in features:
    print(f'  {nv["name"]}: {nv["value"]}')

print('\n[*] Configuration Values:')
for nv in configs:
    print(f'  {nv["name"]}: {nv["value"]}')
```

---

### Section 3: Master Policy Application (Cells 31-40)

**Cell 31:** Markdown - Master Policy Template Explanation

**Cell 32:** Generate Master Policy XML
```python
def generate_master_policy(enabled_fragments: List[str]) -> str:
    """Generate master API policy with conditional fragment includes."""

    inbound_fragments = []
    backend_fragments = []
    outbound_fragments = []
    onerror_fragments = []

    for fragment_id in enabled_fragments:
        fragment_info = FRAGMENTS.get(fragment_id)
        if not fragment_info:
            continue

        applies_to = fragment_info["applies_to"]
        feature_name = fragment_id.replace("fragment-", "")

        # Create conditional include
        include_block = f'''
        <choose>
            <when condition="@({{{{named-value-feature-{feature_name}-enabled}}}} == &quot;true&quot;)">
                <include-fragment fragment-id="{fragment_id}" />
            </when>
        </choose>'''

        if "inbound" in applies_to:
            inbound_fragments.append(include_block)
        if "backend" in applies_to:
            backend_fragments.append(include_block)
        if "outbound" in applies_to:
            outbound_fragments.append(include_block)
        if "on-error" in applies_to:
            onerror_fragments.append(include_block)

    policy_xml = f"""<policies>
    <inbound>
        <base />
{''.join(inbound_fragments)}
    </inbound>
    <backend>
        <base />
{''.join(backend_fragments)}
    </backend>
    <outbound>
        <base />
{''.join(outbound_fragments)}
    </outbound>
    <on-error>
        <base />
{''.join(onerror_fragments)}
    </on-error>
</policies>"""

    return policy_xml
```

**Cell 33:** Apply Master Policy to API
```python
print('[*] Applying master policy to API...')
print(f'    API ID: {config.api_id}')

# Get list of all fragment IDs
fragment_ids = list(FRAGMENTS.keys())

# Generate master policy
master_policy_xml = generate_master_policy(fragment_ids)

# Apply to API
success = apply_master_policy(config.api_id, master_policy_xml)

if success:
    print('[OK] Master policy applied successfully')
    print('[INFO] Fragments will be included conditionally based on feature flags')
else:
    print('[FAIL] Failed to apply master policy')
```

**Cell 34:** View Current API Policy
```python
# Get current policy for the API
current_policy = get_api_policy(config.api_id)

print('[*] Current API Policy:')
print('='*80)
print(current_policy)
print('='*80)
```

---

### Section 4: Dynamic Feature Toggle (Cells 41-50)

**Cell 41:** Markdown - Live Feature Toggle Demo

**Cell 42:** Toggle Token Metrics Feature
```python
print('[*] Toggling token-metrics feature...')

# Get current status
current_status = get_feature_status("token-metrics")
print(f'    Current: {current_status}')

# Toggle
new_status = not current_status
toggle_feature("token-metrics", new_status)

print(f'    New: {new_status}')
print('[OK] Feature toggled')
print('[INFO] Change will take effect on next API call (~30-60 seconds)')
```

**Cell 43:** Toggle Multiple Features at Once
```python
feature_changes = {
    "token-ratelimit": True,   # Enable for testing
    "caching": False,          # Disable to test without caching
    "circuit-breaker": True    # Enable for resilience
}

print('[*] Applying bulk feature changes...')

for feature_name, enabled in feature_changes.items():
    toggle_feature(feature_name, enabled)
    status = "ENABLED" if enabled else "DISABLED"
    print(f'  [{status}] {feature_name}')

print('[OK] All features updated')
```

**Cell 44:** Interactive Feature Toggle Menu
```python
def show_feature_menu():
    """Interactive menu for toggling features."""

    while True:
        print('\n' + '='*80)
        print('FEATURE FLAG MANAGEMENT')
        print('='*80)

        # List current features
        for i, (feature_name, enabled) in enumerate(config.features.items(), 1):
            status = "✅ ENABLED" if enabled else "❌ DISABLED"
            print(f'{i}. {feature_name:30s} {status}')

        print('\n0. Exit')

        choice = input('\nSelect feature to toggle (0 to exit): ')

        if choice == '0':
            break

        try:
            idx = int(choice) - 1
            feature_name = list(config.features.keys())[idx]
            current = config.features[feature_name]
            new_status = not current

            toggle_feature(feature_name, new_status)
            config.features[feature_name] = new_status

            print(f'[OK] {feature_name} is now {"ENABLED" if new_status else "DISABLED"}')
        except:
            print('[ERROR] Invalid choice')

# Run interactive menu (comment out if running non-interactively)
# show_feature_menu()
```

---

### Section 5: Testing & Validation (Cells 51-60)

**Cell 51:** Markdown - Testing Strategy

**Cell 52:** Test Individual Fragments
```python
print('[*] Testing individual fragments...')

test_results = []

for fragment_id in FRAGMENTS.keys():
    feature_name = fragment_id.replace("fragment-", "")

    # Enable only this feature
    for f in config.features.keys():
        toggle_feature(f, f == feature_name)

    # Wait for propagation
    import time
    time.sleep(5)

    # Make test API call
    try:
        response = test_openai_api_call()
        test_results.append({
            "fragment": fragment_id,
            "status": "PASS" if response.status_code == 200 else "FAIL",
            "latency_ms": response.elapsed.total_seconds() * 1000
        })
    except Exception as e:
        test_results.append({
            "fragment": fragment_id,
            "status": "ERROR",
            "error": str(e)
        })

# Display results
import pandas as pd
df = pd.DataFrame(test_results)
print(df)
```

**Cell 53:** Test Fragment Combinations
```python
# Test common fragment combinations
test_combinations = [
    ["token-metrics", "load-balancing"],
    ["token-ratelimit", "circuit-breaker"],
    ["all"]  # All enabled
]

for combination in test_combinations:
    print(f'\n[*] Testing combination: {", ".join(combination)}')

    # Enable combination
    for feature in config.features.keys():
        should_enable = feature in combination or "all" in combination
        toggle_feature(feature, should_enable)

    # Test
    response = test_openai_api_call()
    print(f'    Status: {response.status_code}')
    print(f'    Latency: {response.elapsed.total_seconds() * 1000:.2f}ms')
```

**Cell 54:** A/B Testing Framework
```python
def ab_test_fragments(fragment_a: str, fragment_b: str, num_requests: int = 10):
    """Compare performance of two fragments."""

    results_a = []
    results_b = []

    # Test Fragment A
    toggle_feature(fragment_a.replace("fragment-", ""), True)
    toggle_feature(fragment_b.replace("fragment-", ""), False)
    time.sleep(5)

    for _ in range(num_requests):
        response = test_openai_api_call()
        results_a.append(response.elapsed.total_seconds() * 1000)

    # Test Fragment B
    toggle_feature(fragment_a.replace("fragment-", ""), False)
    toggle_feature(fragment_b.replace("fragment-", ""), True)
    time.sleep(5)

    for _ in range(num_requests):
        response = test_openai_api_call()
        results_b.append(response.elapsed.total_seconds() * 1000)

    # Compare
    import statistics
    print(f'[*] A/B Test Results:')
    print(f'    {fragment_a}: avg={statistics.mean(results_a):.2f}ms, p95={statistics.quantiles(results_a, n=20)[18]:.2f}ms')
    print(f'    {fragment_b}: avg={statistics.mean(results_b):.2f}ms, p95={statistics.quantiles(results_b, n=20)[18]:.2f}ms')

# Example: Compare load balancing with/without circuit breaker
ab_test_fragments("fragment-load-balancing", "fragment-circuit-breaker", num_requests=20)
```

---

### Section 6: Monitoring & Analytics (Cells 61-70)

**Cell 61:** Markdown - Monitoring Dashboard

**Cell 62:** Query Azure Monitor for Token Metrics
```python
# Query token metrics from Azure Monitor
from azure.monitor.query import LogsQueryClient, MetricsQueryClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
metrics_client = MetricsQueryClient(credential)

# Query token consumption metrics
print('[*] Querying token metrics from Azure Monitor...')

# Get APIM resource ID
apim_resource_id = f'/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service}'

# Query last 1 hour
from datetime import datetime, timedelta
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=1)

metrics = metrics_client.query_resource(
    apim_resource_id,
    metric_names=["TokenTransaction"],
    timespan=(start_time, end_time)
)

# Display results
for metric in metrics.metrics:
    print(f'\n[*] Metric: {metric.name}')
    for timeseries in metric.timeseries:
        for data_point in timeseries.data:
            print(f'    {data_point.time_stamp}: {data_point.total}')
```

**Cell 63:** Visualize Fragment Usage
```python
import matplotlib.pyplot as plt

# Plot token metrics over time
fig, ax = plt.subplots(figsize=(12, 6))

# Plot data
for timeseries in metrics.metrics[0].timeseries:
    timestamps = [dp.time_stamp for dp in timeseries.data]
    values = [dp.total for dp in timeseries.data]
    ax.plot(timestamps, values, label=timeseries.metadata.get('Dimension', 'Total'))

ax.set_xlabel('Time')
ax.set_ylabel('Token Count')
ax.set_title('Token Consumption by Fragment')
ax.legend()
plt.show()
```

**Cell 64:** Generate Fragment Usage Report
```python
def generate_fragment_report():
    """Generate comprehensive report on fragment usage."""

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "features": {},
        "fragments": {},
        "configuration": {}
    }

    # Get feature status
    for feature_name in config.features.keys():
        report["features"][feature_name] = get_feature_status(feature_name)

    # Get fragment details
    fragments = list_fragments()
    for fragment in fragments:
        report["fragments"][fragment["id"]] = {
            "description": fragment.get("description", ""),
            "last_modified": fragment.get("lastModified", "")
        }

    # Get configuration
    for config_name in config.config_values.keys():
        named_value_name = f"config-{config_name}"
        report["configuration"][config_name] = get_named_value(named_value_name)

    # Save report
    report_path = f'fragment-report-{datetime.utcnow().strftime("%Y%m%d-%H%M%S")}.json'
    Path(report_path).write_text(json.dumps(report, indent=2))

    print(f'[OK] Report saved to {report_path}')
    return report

report = generate_fragment_report()
print(json.dumps(report, indent=2))
```

---

### Section 7: CI/CD Integration (Cells 71-80)

**Cell 71:** Markdown - CI/CD Pipeline Integration

**Cell 72:** Export Fragment Configuration
```python
def export_fragment_config(output_file: str = "fragment-config.json"):
    """Export all fragment configuration for CI/CD."""

    config_export = {
        "version": "1.0",
        "apim": {
            "subscription_id": config.subscription_id,
            "resource_group": config.resource_group,
            "service_name": config.apim_service,
            "api_id": config.api_id
        },
        "fragments": {},
        "features": config.features,
        "config_values": config.config_values
    }

    # Export fragment XML
    for fragment_id, fragment_info in FRAGMENTS.items():
        xml_path = fragment_info["xml_template"]
        if Path(xml_path).exists():
            config_export["fragments"][fragment_id] = {
                "description": fragment_info["description"],
                "xml_content": Path(xml_path).read_text(),
                "applies_to": fragment_info["applies_to"]
            }

    # Save
    Path(output_file).write_text(json.dumps(config_export, indent=2))
    print(f'[OK] Configuration exported to {output_file}')

export_fragment_config()
```

**Cell 73:** Import Fragment Configuration
```python
def import_fragment_config(config_file: str = "fragment-config.json"):
    """Import and apply fragment configuration from file."""

    if not Path(config_file).exists():
        print(f'[ERROR] Config file not found: {config_file}')
        return False

    config_data = json.loads(Path(config_file).read_text())

    print('[*] Importing fragment configuration...')

    # Deploy fragments
    for fragment_id, fragment_data in config_data["fragments"].items():
        deploy_fragment(
            fragment_id,
            fragment_data["xml_content"],
            fragment_data["description"]
        )
        print(f'  [OK] {fragment_id}')

    # Set feature flags
    for feature_name, enabled in config_data["features"].items():
        toggle_feature(feature_name, enabled)
        print(f'  [OK] feature-{feature_name}-enabled = {enabled}')

    # Set configuration values
    for config_name, config_value in config_data["config_values"].items():
        create_named_value(f"config-{config_name}", config_value)
        print(f'  [OK] config-{config_name} = {config_value}')

    print('[OK] Configuration imported successfully')
    return True

# import_fragment_config("fragment-config.json")
```

**Cell 74:** Generate Azure Pipeline YAML
```python
pipeline_yaml = """
# Azure DevOps Pipeline for Fragment Policy Deployment

trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: apim-policy-fragments

stages:
- stage: Deploy
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
          python deploy-fragments.py

    - task: AzureCLI@2
      displayName: 'Run Fragment Tests'
      inputs:
        azureSubscription: '$(azureSubscription)'
        scriptType: 'bash'
        scriptLocation: 'inlineScript'
        inlineScript: |
          # Run tests
          python test-fragments.py

          # Publish results
          pytest --junitxml=test-results.xml

    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/test-results.xml'
"""

Path("azure-pipelines.yml").write_text(pipeline_yaml)
print('[OK] Pipeline YAML generated: azure-pipelines.yml')
```

---

## IMPLEMENTATION ROADMAP

### Phase 1: Core Infrastructure (Week 1)
- ✅ Create notebook structure (cells 1-20)
- ✅ Implement helper functions
- ✅ Create fragment XML templates
- ✅ Deploy basic fragments (token-metrics, load-balancing)
- ✅ Test individual fragments

### Phase 2: Feature Flags & Configuration (Week 1)
- ✅ Implement Named Values for feature flags
- ✅ Implement Named Values for configuration
- ✅ Create master policy generator
- ✅ Test conditional fragment inclusion

### Phase 3: Advanced Features (Week 2)
- ✅ Implement interactive toggle menu
- ✅ Create A/B testing framework
- ✅ Add monitoring & analytics integration
- ✅ Build fragment usage dashboard

### Phase 4: CI/CD Integration (Week 2)
- ✅ Export/import configuration
- ✅ Generate Azure Pipeline YAML
- ✅ Create deployment scripts
- ✅ Document deployment process

### Phase 5: Testing & Validation (Week 3)
- ✅ Unit tests for all functions
- ✅ Integration tests for fragment combinations
- ✅ Performance tests (A/B testing)
- ✅ Load testing with fragments

### Phase 6: Documentation & Training (Week 3)
- ✅ Complete user guide
- ✅ API reference documentation
- ✅ Video tutorials
- ✅ Best practices guide

---

## FRAGMENT SPECIFICATIONS

### Fragment 1: Token Metrics
**ID:** `fragment-token-metrics`
**File:** `fragments/token-metrics.xml`
**Applies To:** Inbound
**Feature Flag:** `feature-token-metrics-enabled`
**Configuration:**
- `config-token-metrics-namespace` (default: "openai")

**XML Template:**
```xml
<fragment>
    <azure-openai-emit-token-metric namespace="{{named-value-config-token-metrics-namespace}}">
        <dimension name="Subscription ID" value="@(context.Subscription.Id)" />
        <dimension name="Client IP" value="@(context.Request.IpAddress)" />
        <dimension name="API ID" value="@(context.Api.Id)" />
        <dimension name="User ID" value="@(context.Request.Headers.GetValueOrDefault(&quot;x-user-id&quot;, &quot;N/A&quot;))" />
    </azure-openai-emit-token-metric>
</fragment>
```

### Fragment 2: Load Balancing
**ID:** `fragment-load-balancing`
**File:** `fragments/load-balancing.xml`
**Applies To:** Inbound, Backend
**Feature Flag:** `feature-load-balancing-enabled`
**Configuration:**
- `config-lb-backend-pool-id` (default: "openai-backend-pool")
- `config-lb-retry-count` (default: "2")

**XML Template:**
```xml
<fragment>
    <!-- Inbound section -->
    <set-backend-service backend-id="{{named-value-config-lb-backend-pool-id}}" />

    <!-- Backend section (when applied to backend) -->
    <retry count="{{named-value-config-lb-retry-count}}" interval="0" first-fast-retry="true"
           condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
        <forward-request buffer-request-body="true" />
    </retry>
</fragment>
```

### Fragment 3: Token Rate Limiting
**ID:** `fragment-token-ratelimit`
**File:** `fragments/token-ratelimit.xml`
**Applies To:** Inbound
**Feature Flag:** `feature-token-ratelimit-enabled`
**Configuration:**
- `config-token-ratelimit-tpm` (default: "100")

**XML Template:**
```xml
<fragment>
    <azure-openai-token-limit
        tokens-per-minute="{{named-value-config-token-ratelimit-tpm}}"
        counter-key="@(context.Subscription.Id)"
        estimate-prompt-tokens="true"
        tokens-consumed-header-name="consumed-tokens"
        remaining-tokens-header-name="remaining-tokens" />
</fragment>
```

### Fragment 4: Private Connectivity
**ID:** `fragment-private-connectivity`
**File:** `fragments/private-connectivity.xml`
**Applies To:** Inbound
**Feature Flag:** `feature-private-connectivity-enabled`
**Configuration:**
- `config-backend-id` (default: "openai-backend")

**XML Template:**
```xml
<fragment>
    <authentication-managed-identity
        resource="https://cognitiveservices.azure.com"
        output-token-variable-name="managed-id-access-token"
        ignore-error="false" />
    <set-header name="Authorization" exists-action="override">
        <value>@("Bearer " + (string)context.Variables["managed-id-access-token"])</value>
    </set-header>
    <set-backend-service backend-id="{{named-value-config-backend-id}}" />
</fragment>
```

### Fragment 5: Semantic Caching (Bonus)
**ID:** `fragment-caching`
**File:** `fragments/caching.xml`
**Applies To:** Inbound, Outbound
**Feature Flag:** `feature-caching-enabled`
**Configuration:**
- `config-cache-duration-seconds` (default: "300")
- `config-redis-cache-name` (default: "redis-cache")

**XML Template:**
```xml
<fragment>
    <!-- Inbound: Check cache -->
    <cache-lookup vary-by-developer="false" vary-by-developer-groups="false"
                  caching-type="external" downstream-caching-type="none">
        <vary-by-header>Content-Type</vary-by-header>
        <vary-by-query-parameter>*</vary-by-query-parameter>
    </cache-lookup>

    <!-- Outbound: Store in cache -->
    <cache-store duration="{{named-value-config-cache-duration-seconds}}"
                 caching-type="external" />
</fragment>
```

### Fragment 6: Circuit Breaker (Bonus)
**ID:** `fragment-circuit-breaker`
**File:** `fragments/circuit-breaker.xml`
**Applies To:** Backend, On-Error
**Feature Flag:** `feature-circuit-breaker-enabled`
**Configuration:**
- `config-circuit-error-threshold` (default: "5")
- `config-circuit-timeout-seconds` (default: "60")

**XML Template:**
```xml
<fragment>
    <!-- Circuit breaker pattern -->
    <choose>
        <when condition="@(context.Variables.GetValueOrDefault<int>(&quot;circuit-failures&quot;, 0) > {{named-value-config-circuit-error-threshold}})">
            <return-response>
                <set-status code="503" reason="Circuit Breaker Open" />
                <set-body>Circuit breaker is open. Service temporarily unavailable.</set-body>
            </return-response>
        </when>
    </choose>
</fragment>
```

---

## COMPARISON: INLINE vs FRAGMENTS

| Aspect | Inline Policies (Current) | Policy Fragments (New) |
|--------|---------------------------|------------------------|
| **Reusability** | ❌ Copy-paste across APIs | ✅ Define once, use many times |
| **Maintainability** | ❌ Update each API separately | ✅ Update fragment once |
| **Feature Flags** | ❌ Must modify policy XML | ✅ Toggle via Named Values |
| **Configuration** | ❌ Hardcoded in XML | ✅ Dynamic via Named Values |
| **Testing** | ❌ Must redeploy entire policy | ✅ Test fragments independently |
| **A/B Testing** | ❌ Complex, error-prone | ✅ Simple feature flag toggle |
| **Version Control** | ❌ Large XML diffs | ✅ Small fragment diffs |
| **CI/CD** | ❌ Deploy entire policy | ✅ Deploy only changed fragments |
| **Rollback** | ❌ Restore entire policy | ✅ Toggle feature flag |
| **Monitoring** | ❌ Monolithic metrics | ✅ Per-fragment metrics |

---

## ACCEPTANCE CRITERIA

### Functional Requirements
- ✅ All 6 fragments deployable to APIM
- ✅ Feature flags control fragment activation
- ✅ Configuration values configurable via Named Values
- ✅ Master policy includes fragments conditionally
- ✅ Interactive toggle menu works
- ✅ A/B testing framework functional

### Non-Functional Requirements
- ✅ Notebook runs end-to-end without errors
- ✅ All markdown cells explain concepts clearly
- ✅ Code follows Python best practices
- ✅ Fragment XML validates against APIM schema
- ✅ Performance overhead < 10ms per fragment

### Documentation Requirements
- ✅ Each cell has clear comments
- ✅ Markdown sections explain concepts
- ✅ Fragment specifications complete
- ✅ CI/CD integration documented
- ✅ Testing strategy documented

---

## NEXT STEPS

1. **User Review & Approval**
   - Review this architecture plan
   - Provide feedback on structure
   - Approve to begin implementation

2. **Create Notebook File**
   - Create `master-ai-gateway-fragment-policies.ipynb`
   - Implement cells 1-20 (core infrastructure)
   - Test basic fragment deployment

3. **Parallel Development**
   - Continue PLAN 2 fixes on current notebook
   - Develop fragment-based notebook in parallel
   - Keep both notebooks synchronized

4. **Integration & Testing**
   - Test fragment notebook end-to-end
   - Compare performance vs inline policies
   - Validate CI/CD integration

---

**STATUS:** ✅ PLAN COMPLETE - AWAITING USER APPROVAL

This comprehensive plan provides a complete roadmap for building a production-ready, fragment-based policy management notebook that addresses all the limitations of the current inline policy approach.

---

*Generated by Claude Code*
*Anthropic AI Assistant*
