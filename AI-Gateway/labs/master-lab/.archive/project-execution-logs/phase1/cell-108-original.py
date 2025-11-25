import asyncio
import httpx
import sys
from datetime import datetime

print("=" * 80)
print("SEMANTIC KERNEL DIAGNOSTIC REPORT")
print(f"Generated: {datetime.now().isoformat()}")
print("=" * 80)

# Test 1: Python Environment
print("\n[1/7] Python Environment")
print("-" * 80)
print(f"Python version: {sys.version}")
print(f"asyncio: {asyncio.__version__ if hasattr(asyncio, '__version__') else 'built-in'}")

# Test 2: Package Versions
print("\n[2/7] Package Versions")
print("-" * 80)
packages_to_check = [
    'semantic_kernel',
    'openai',
    'httpx',
    'nest_asyncio',
    'mcp'
]

for package in packages_to_check:
    try:
        module = __import__(package)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package}: {version}")
    except ImportError:
        print(f"❌ {package}: NOT INSTALLED")

# Test 3: Azure OpenAI Direct (bypass APIM)
print("\n[3/7] Azure OpenAI Direct Access (bypassing APIM)")
print("-" * 80)
try:
    from openai import AzureOpenAI
    
    # Extract the actual Azure OpenAI endpoint from APIM gateway URL if available
    # For this test, we'll use APIM as the gateway
    test_client = AzureOpenAI(
        azure_endpoint=apim_gateway_url,
        api_key=apim_api_key,
        api_version="2024-08-01-preview"
    )
    
    print(f"Endpoint: {apim_gateway_url}")
    print(f"API Key: ****{apim_api_key[-4:] if len(apim_api_key) > 4 else '****'}")
    print("Attempting simple completion...")
    
    response = test_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Reply with just 'OK'"}],
        max_tokens=5,
        timeout=10.0
    )
    
    result = response.choices[0].message.content
    print(f"✅ Azure OpenAI works: '{result}'")
    print(f"   Tokens used: {response.usage.total_tokens if response.usage else 'N/A'}")
    
except Exception as e:
    print(f"❌ Azure OpenAI failed: {type(e).__name__}: {str(e)[:100]}")

# Test 4: APIM Gateway Connectivity
print("\n[4/7] APIM Gateway Connectivity")
print("-" * 80)
try:
    async def test_apim():
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test resource gateway
            try:
                response = await client.get(
                    f"{apim_resource_gateway_url}/health",
                    headers={"api-key": apim_api_key}
                )
                print(f"✅ APIM Resource Gateway: {response.status_code}")
            except Exception as e:
                print(f"⚠️  APIM Resource Gateway: {str(e)[:60]}")
            
            # Test main gateway
            try:
                response = await client.get(
                    f"{apim_gateway_url}/health",
                    headers={"api-key": apim_api_key}
                )
                print(f"✅ APIM Main Gateway: {response.status_code}")
            except Exception as e:
                print(f"⚠️  APIM Main Gateway: {str(e)[:60]}")
    
    await test_apim()
    
except Exception as e:
    print(f"❌ APIM test failed: {str(e)[:100]}")

# Test 5: MCP Server Availability
print("\n[5/7] MCP Server Availability")
print("-" * 80)

mcp_servers = {
    "weather": f"{apim_resource_gateway_url}/weather",
    "docs": f"{apim_resource_gateway_url}/docs"
}

async def test_mcp_servers():
    async with httpx.AsyncClient(timeout=10.0) as client:
        for name, base_url in mcp_servers.items():
            try:
                # Try SSE endpoint
                response = await client.get(
                    f"{base_url}/sse",
                    headers={"api-key": apim_api_key}
                )
                print(f"✅ {name:10} SSE: {response.status_code}")
            except httpx.TimeoutException:
                print(f"⏱️  {name:10} SSE: Timeout (may be scaled to zero)")
            except Exception as e:
                print(f"❌ {name:10} SSE: {str(e)[:50]}")

try:
    await test_mcp_servers()
except Exception as e:
    print(f"❌ MCP server test failed: {str(e)[:100]}")

# Test 6: Semantic Kernel Configuration
print("\n[6/7] Semantic Kernel Configuration Test")
print("-" * 80)
try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
    
    kernel = Kernel()
    service_id = "diagnostic_test"
    
    # Add Azure OpenAI service
    service = AzureChatCompletion(
        service_id=service_id,
        endpoint=apim_gateway_url,
        api_key=apim_api_key,
        deployment_name="gpt-4o-mini",
        api_version="2024-08-01-preview"
    )
    kernel.add_service(service)
    
    print(f"✅ Kernel created successfully")
    print(f"   Service ID: {service_id}")
    print(f"   Endpoint: {apim_gateway_url}")
    print("   Attempting simple prompt with 30s timeout...")
    
    async def test_sk_prompt():
        result = await kernel.invoke_prompt(
            prompt_template="Reply with just 'SK OK'",
            settings={"service_id": service_id, "max_tokens": 5}
        )
        return str(result)
    
    try:
        result = await asyncio.wait_for(test_sk_prompt(), timeout=30.0)
        print(f"✅ Semantic Kernel prompt works: '{result}'")
    except TimeoutError:
        print(f"❌ Semantic Kernel TIMED OUT after 30s")
        print("   This indicates SK is hanging on basic prompts")
        print("   Likely causes:")
        print("     - SK version incompatibility")
        print("     - Incorrect endpoint configuration")
        print("     - APIM policy blocking requests")
    
except ImportError as e:
    print(f"❌ Semantic Kernel not installed: {str(e)}")
except Exception as e:
    print(f"❌ Semantic Kernel test failed: {type(e).__name__}: {str(e)[:100]}")
    import traceback
    traceback.print_exc()

# Test 7: Network and Async Configuration
print("\n[7/7] Async Configuration")
print("-" * 80)
try:
    import nest_asyncio
    print(f"✅ nest_asyncio installed")
    print(f"   Applied: {nest_asyncio._patched if hasattr(nest_asyncio, '_patched') else 'unknown'}")
except ImportError:
    print(f"❌ nest_asyncio not installed (may cause issues in Jupyter)")

# Summary
print("\n" + "=" * 80)
print("DIAGNOSTIC SUMMARY")
print("=" * 80)
print("\nIf Semantic Kernel is hanging:")
print("  1. ✅ All green checks → Problem is likely SK version or configuration")
print("  2. ❌ Azure OpenAI failed → Fix APIM endpoint or API key first")
print("  3. ❌ MCP servers timeout → Servers may be scaled to zero, wait 60s and retry")
print("  4. ⏱️  SK prompt timeout → Check SK version compatibility with Azure OpenAI")
print("\nRecommended actions:")
print("  - If only SK times out: Try different SK version or configuration")
print("  - If MCP times out: Wake servers with direct HTTP calls")
print("  - If Azure OpenAI fails: Verify APIM policies and deployment")
print("=" * 80)
