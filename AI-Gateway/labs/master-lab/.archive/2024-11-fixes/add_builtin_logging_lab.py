#!/usr/bin/env python3
"""
Add Built-in LLM Logging Lab (Lab 12) to master-ai-gateway-fix-MCP-clean.ipynb

Uses existing resources:
- Log Analytics Workspace: workspace-pavavy6pu5hpa
- Application Insights: insights-pavavy6pu5hpa
- APIM Logger: azuremonitor

NO new infrastructure deployment needed!
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📊 ADDING BUILT-IN LLM LOGGING LAB (LAB 12)")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

current_cell_count = len(notebook['cells'])
print(f"\n[*] Current notebook has {current_cell_count} cells")

# Cell 123: Markdown Introduction
cell_123_markdown = """## Lab 12: Built-in LLM Logging

![Built-in Logging](https://learn.microsoft.com/azure/api-management/media/monitor-api-management/llm-logging-architecture.png)

### Overview

Azure API Management automatically logs LLM interactions to Azure Monitor:
- **Token usage** (prompt, completion, total)
- **Prompts** (user messages sent to the model)
- **Completions** (model responses)
- **Metadata** (model, timestamp, correlation ID)

This lab demonstrates how to:
1. Enable LLM logging diagnostics on your inference API
2. Make test API calls to generate log data
3. Query logs with KQL to analyze token usage

**Resources Used** (already deployed):
- Log Analytics Workspace: `workspace-pavavy6pu5hpa`
- APIM Logger: `azuremonitor`

**Reference**: [Monitor API Management LLM Logging](https://learn.microsoft.com/azure/api-management/monitor-api-management#modify-api-logging-settings)
"""

# Cell 124: Enable LLM Logging Configuration
cell_124_code = '''# Lab 12, Step 1: Enable LLM Logging on Inference API

import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print(f"[config] Loaded: {env_file.absolute()}")

apim_service_id = os.environ.get('APIM_SERVICE_ID')

print("=" * 80)
print("🔧 CONFIGURING LLM LOGGING DIAGNOSTICS")
print("=" * 80)

# Get the azuremonitor logger ID
logger_uri = f"https://management.azure.com{apim_service_id}/loggers/azuremonitor?api-version=2024-06-01-preview"
result = subprocess.run(['az', 'rest', '--method', 'get', '--uri', logger_uri],
                       capture_output=True, text=True)

if result.returncode == 0:
    logger_data = json.loads(result.stdout)
    logger_id = logger_data['id']
    print(f"\\n✅ Found APIM logger: {logger_id}")
else:
    print(f"\\n❌ Failed to get logger: {result.stderr}")
    raise Exception("Logger not found")

# Configure API diagnostics with LLM logging enabled
diagnostics_uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/diagnostics/azuremonitor?api-version=2024-06-01-preview"

diagnostics_config = {
    "properties": {
        "alwaysLog": "allErrors",
        "verbosity": "verbose",
        "logClientIp": True,
        "loggerId": logger_id,
        "sampling": {
            "samplingType": "fixed",
            "percentage": 100
        },
        "frontend": {
            "request": {"headers": [], "body": {"bytes": 0}},
            "response": {"headers": [], "body": {"bytes": 0}}
        },
        "backend": {
            "request": {"headers": [], "body": {"bytes": 0}},
            "response": {"headers": [], "body": {"bytes": 0}}
        },
        "largeLanguageModel": {
            "logs": "enabled",
            "requests": {
                "messages": "all",
                "maxSizeInBytes": 262144
            },
            "responses": {
                "messages": "all",
                "maxSizeInBytes": 262144
            }
        }
    }
}

body_file = '/tmp/llm-diagnostics-config.json'
with open(body_file, 'w', encoding='utf-8') as f:
    json.dump(diagnostics_config, f, indent=2)

print("\\n[*] Enabling LLM logging diagnostics...")

cmd = ['az', 'rest', '--method', 'put', '--uri', diagnostics_uri, '--body', f'@{body_file}']
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\\n✅ LLM logging diagnostics enabled!")
    print("\\n📋 Configuration:")
    print("   - Logger: azuremonitor → Log Analytics Workspace")
    print("   - LLM Logs: enabled")
    print("   - Prompts: captured (all messages, max 256KB)")
    print("   - Completions: captured (all messages, max 256KB)")
    print("   - Token usage: automatically logged")
    print("\\n💡 Logs will appear in Log Analytics within 1-2 minutes")
else:
    print(f"\\n❌ Error configuring diagnostics:")
    print(result.stderr)
    raise Exception("Failed to enable LLM logging")

print("=" * 80)
'''

# Cell 125: Make Test API Calls
cell_125_code = '''# Lab 12, Step 2: Generate Test Data with API Calls

import os
import time
from openai import AzureOpenAI
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')
apim_api_key = os.environ.get('APIM_API_KEY')
inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')

print("=" * 80)
print("🧪 GENERATING TEST DATA FOR LLM LOGGING")
print("=" * 80)

# Initialize OpenAI client
client = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key=apim_api_key,
    api_version="2024-08-01-preview"
)

# Test messages with different token counts
test_cases = [
    {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Hello! How are you?"}],
        "description": "Short greeting"
    },
    {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Explain quantum computing in 3 sentences."}],
        "description": "Medium complexity query"
    },
    {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
        ],
        "description": "Code generation request"
    },
    {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Count from 1 to 20 with commas."}],
        "description": "Token-heavy response"
    }
]

print(f"\\n[*] Making {len(test_cases)} test API calls...\\n")

for i, test in enumerate(test_cases, 1):
    print(f"Test {i}/{len(test_cases)}: {test['description']}")

    try:
        response = client.chat.completions.create(
            model=test['model'],
            messages=test['messages'],
            max_tokens=150
        )

        content = response.choices[0].message.content
        tokens = response.usage.total_tokens

        print(f"  ✅ Response: {content[:60]}{'...' if len(content) > 60 else ''}")
        print(f"  📊 Tokens: {response.usage.prompt_tokens} prompt + {response.usage.completion_tokens} completion = {tokens} total")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print()
    time.sleep(0.5)  # Brief delay between calls

print("\\n⏳ Waiting 90 seconds for logs to propagate to Log Analytics...")
print("   ", end='', flush=True)

for i in range(90, 0, -1):
    print(f"\\r   {i:2d}s remaining...", end='', flush=True)
    time.sleep(1)

print("\\r   ✅ Logs should now be available in Log Analytics!     ")
print("\\n[OK] Ready to query LLM logs!")
print("=" * 80)
'''

# Cell 126: Query Token Usage by Model
cell_126_code = '''# Lab 12, Step 3: Query Token Usage by Model

import os
import json
import subprocess
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

# Get Log Analytics Workspace Customer ID
workspace_customer_id = "f3b7ec6c-4bcc-4d13-9cbc-296be53f9eca"  # workspace-pavavy6pu5hpa

print("=" * 80)
print("📊 QUERY 1: TOKEN USAGE BY MODEL")
print("=" * 80)

# KQL query: Token usage aggregated by model
kql_query = """ApiManagementGatewayLlmLog
| where TimeGenerated > ago(1h)
| where DeploymentName != ''
| summarize
    TotalCalls = count(),
    TotalTokens = sum(TotalTokens),
    PromptTokens = sum(PromptTokens),
    CompletionTokens = sum(CompletionTokens),
    AvgTokensPerCall = avg(TotalTokens)
  by DeploymentName
| order by TotalTokens desc"""

print(f"\\n[*] Querying Log Analytics workspace: {workspace_customer_id}")
print(f"\\n[*] KQL Query:")
print("-" * 80)
print(kql_query)
print("-" * 80)

cmd = [
    'az', 'monitor', 'log-analytics', 'query',
    '-w', workspace_customer_id,
    '--analytics-query', kql_query,
    '--output', 'json'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    try:
        query_result = json.loads(result.stdout)

        if query_result and len(query_result) > 0:
            df = pd.DataFrame(query_result)
            print("\\n✅ Query Results:\\n")
            print(df.to_string(index=False))

            print("\\n📈 Summary:")
            total_calls = df['TotalCalls'].sum()
            total_tokens = df['TotalTokens'].sum()
            print(f"   - Total API calls logged: {total_calls}")
            print(f"   - Total tokens consumed: {total_tokens:,}")
        else:
            print("\\n⚠️  No LLM logs found in the last hour")
            print("   💡 Tip: Run the previous cell to generate test data")
    except Exception as e:
        print(f"\\n❌ Error parsing results: {e}")
        print(result.stdout)
else:
    print(f"\\n❌ Query failed:")
    print(result.stderr)

print("=" * 80)
'''

# Cell 127: Query Token Usage by Subscription
cell_127_code = '''# Lab 12, Step 4: Query Token Usage by Subscription

import os
import json
import subprocess
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

workspace_customer_id = "f3b7ec6c-4bcc-4d13-9cbc-296be53f9eca"

print("=" * 80)
print("📊 QUERY 2: TOKEN USAGE BY SUBSCRIPTION")
print("=" * 80)

# KQL query: Join LlmLog with GatewayLogs to get subscription info
kql_query = """let llmLogs = ApiManagementGatewayLlmLog
| where TimeGenerated > ago(1h)
| where DeploymentName != '';
llmLogs
| join kind=leftouter ApiManagementGatewayLogs on CorrelationId
| project
    SubscriptionId = ApimSubscriptionId,
    DeploymentName,
    TotalTokens,
    PromptTokens,
    CompletionTokens
| summarize
    TotalCalls = count(),
    SumTotalTokens = sum(TotalTokens),
    SumPromptTokens = sum(PromptTokens),
    SumCompletionTokens = sum(CompletionTokens)
  by SubscriptionId, DeploymentName
| order by SumTotalTokens desc"""

print(f"\\n[*] Querying Log Analytics workspace: {workspace_customer_id}")
print(f"\\n[*] KQL Query:")
print("-" * 80)
print(kql_query)
print("-" * 80)

cmd = [
    'az', 'monitor', 'log-analytics', 'query',
    '-w', workspace_customer_id,
    '--analytics-query', kql_query,
    '--output', 'json'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    try:
        query_result = json.loads(result.stdout)

        if query_result and len(query_result) > 0:
            df = pd.DataFrame(query_result)

            # Mask subscription ID for display (show last 8 chars)
            if 'SubscriptionId' in df.columns:
                df['SubscriptionId'] = df['SubscriptionId'].apply(
                    lambda x: f"****{x[-8:]}" if pd.notna(x) and len(str(x)) > 8 else x
                )

            print("\\n✅ Query Results:\\n")
            print(df.to_string(index=False))

            print("\\n📈 Summary by Subscription:")
            subscription_totals = df.groupby('SubscriptionId')['SumTotalTokens'].sum()
            for sub_id, total in subscription_totals.items():
                print(f"   - {sub_id}: {total:,} tokens")

        else:
            print("\\n⚠️  No subscription data found")
            print("   💡 This query requires ApimSubscriptionId in the logs")
    except Exception as e:
        print(f"\\n❌ Error parsing results: {e}")
        print(result.stdout)
else:
    print(f"\\n❌ Query failed:")
    print(result.stderr)

print("=" * 80)
'''

# Cell 128: View Prompts and Completions
cell_128_code = '''# Lab 12, Step 5: View Prompts and Completions

import os
import json
import subprocess
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

workspace_customer_id = "f3b7ec6c-4bcc-4d13-9cbc-296be53f9eca"

print("=" * 80)
print("📊 QUERY 3: VIEW PROMPTS AND COMPLETIONS")
print("=" * 80)

# KQL query: View actual prompts and responses
kql_query = """ApiManagementGatewayLlmLog
| where TimeGenerated > ago(1h)
| where DeploymentName != ''
| project
    TimeGenerated,
    DeploymentName,
    UserPrompt,
    Response,
    TotalTokens,
    PromptTokens,
    CompletionTokens
| order by TimeGenerated desc
| take 10"""

print(f"\\n[*] Querying Log Analytics workspace: {workspace_customer_id}")
print(f"\\n[*] KQL Query:")
print("-" * 80)
print(kql_query)
print("-" * 80)

cmd = [
    'az', 'monitor', 'log-analytics', 'query',
    '-w', workspace_customer_id,
    '--analytics-query', kql_query,
    '--output', 'json'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    try:
        query_result = json.loads(result.stdout)

        if query_result and len(query_result) > 0:
            print(f"\\n✅ Found {len(query_result)} recent LLM interactions:\\n")

            for i, log in enumerate(query_result, 1):
                print(f"{'=' * 80}")
                print(f"Interaction {i} - {log.get('TimeGenerated', 'N/A')}")
                print(f"{'=' * 80}")
                print(f"Model: {log.get('DeploymentName', 'N/A')}")
                print(f"Tokens: {log.get('PromptTokens', 0)} prompt + {log.get('CompletionTokens', 0)} completion = {log.get('TotalTokens', 0)} total")
                print(f"\\n📥 User Prompt:")
                print(f"   {log.get('UserPrompt', 'N/A')}")
                print(f"\\n📤 Model Response:")
                response = log.get('Response', 'N/A')
                # Truncate long responses for display
                if len(response) > 200:
                    print(f"   {response[:200]}...")
                else:
                    print(f"   {response}")
                print()

        else:
            print("\\n⚠️  No LLM interactions found in the last hour")
            print("   💡 Run Step 2 to generate test data")
    except Exception as e:
        print(f"\\n❌ Error parsing results: {e}")
        print(result.stdout)
else:
    print(f"\\n❌ Query failed:")
    print(result.stderr)

print("=" * 80)
print("\\n🎯 Next Steps:")
print("   - Analyze token usage patterns across models")
print("   - Track costs by subscription")
print("   - Monitor prompt/response content for quality")
print("   - Set up alerts for high token usage")
print("=" * 80)
'''

# Create new cells
new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": cell_123_markdown
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_124_code
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_125_code
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_126_code
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_127_code
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_128_code
    }
]

# Add cells to notebook
print(f"\n[*] Adding {len(new_cells)} cells at the end...")
notebook['cells'].extend(new_cells)

new_cell_count = len(notebook['cells'])
print(f"[*] Notebook now has {new_cell_count} cells (was {current_cell_count})")

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-add-builtin-logging')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ BUILT-IN LOGGING LAB ADDED!")
print("=" * 80)

print("\n📋 New Cells Added:")
print("   Cell 123: Lab 12 Introduction (Markdown)")
print("   Cell 124: Enable LLM Logging Diagnostics")
print("   Cell 125: Generate Test Data (4 API calls)")
print("   Cell 126: Query Token Usage by Model")
print("   Cell 127: Query Token Usage by Subscription")
print("   Cell 128: View Prompts and Completions")

print("\n💡 Resources Used (EXISTING - No deployment needed):")
print("   ✅ Log Analytics Workspace: workspace-pavavy6pu5hpa")
print("   ✅ Application Insights: insights-pavavy6pu5hpa")
print("   ✅ APIM Logger: azuremonitor")

print("\n🎯 How to Use:")
print("   1. Reload notebook in VS Code/Jupyter")
print("   2. Run Cell 124 to enable LLM logging (one-time setup)")
print("   3. Run Cell 125 to make test API calls (generates log data)")
print("   4. Run Cells 126-128 to query and analyze the logs")
print("   5. Explore KQL queries for custom analysis")

print("\n📊 What You'll See:")
print("   - Token usage broken down by model")
print("   - Token consumption by subscription")
print("   - Actual prompts and model responses")
print("   - Cost analysis capabilities")

print("\n⏱️  Note:")
print("   - Logs appear in Log Analytics within 1-2 minutes")
print("   - Cell 125 includes 90-second wait for propagation")
print("   - All queries use 1-hour time window (ago(1h))")

print("\n" + "=" * 80)
