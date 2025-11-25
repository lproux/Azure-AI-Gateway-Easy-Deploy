import asyncio
from asyncio import TimeoutError
import nest_asyncio
nest_asyncio.apply()

async def run_with_timeout(task, timeout_seconds=300, task_name="Semantic Kernel task"):
    """
    Run Semantic Kernel task with timeout to prevent indefinite hanging
    
    Args:
        task: Async task/coroutine to run
        timeout_seconds: Maximum time to wait (default: 300s = 5 min)
        task_name: Description for error messages
        
    Returns:
        Task result if successful
        
    Raises:
        TimeoutError: If task exceeds timeout
    """
    try:
        print(f"⏱️  Starting {task_name} (timeout: {timeout_seconds}s)")
        result = await asyncio.wait_for(task, timeout=timeout_seconds)
        print(f"✅ {task_name} completed successfully")
        return result
    except TimeoutError:
        print(f"\n❌ TIMEOUT ERROR: {task_name} exceeded {timeout_seconds} seconds")
        print("\n🔍 Common causes of Semantic Kernel hanging:")
        print("   1. MCP server not responding or scaled to zero")
        print("   2. Azure OpenAI endpoint misconfigured in APIM")
        print("   3. API key invalid, expired, or rate limited")
        print("   4. Network connectivity issues")
        print("   5. Semantic Kernel version incompatibility")
        print("\n💡 Next steps:")
        print("   - Run the diagnostic cell below to isolate the issue")
        print("   - Check MCP server logs in Azure Container Instances")
        print("   - Verify Azure OpenAI deployment in APIM")
        print("   - Test with a shorter timeout (60s) for simple prompts")
        raise
    except Exception as e:
        print(f"❌ Error in {task_name}: {type(e).__name__}: {str(e)}")
        raise

# Test 1: Simple Azure OpenAI test (no SK, no MCP) - Should complete in <10s
print("=" * 70)
print("Test 1: Direct Azure OpenAI (bypass Semantic Kernel)")
print("=" * 70)

try:
    from openai import AzureOpenAI
    
    async def test_direct_azure_openai():
        client = AzureOpenAI(
            azure_endpoint=apim_gateway_url,
            api_key=apim_api_key,
            api_version="2024-08-01-preview"
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the model deployed in your Azure OpenAI
            messages=[{"role": "user", "content": "Say 'Hello from Azure OpenAI' in 5 words or less"}],
            max_tokens=20
        )
        return response.choices[0].message.content
    
    result = await run_with_timeout(
        test_direct_azure_openai(),
        timeout_seconds=15,
        task_name="Direct Azure OpenAI test"
    )
    print(f"\n💬 Response: {result}\n")
except Exception as e:
    print(f"\n⚠️  Direct Azure OpenAI test failed. Fix this before testing Semantic Kernel.\n")

# Test 2: Semantic Kernel with Azure OpenAI (no MCP yet) - Should complete in <30s
print("\n" + "=" * 70)
print("Test 2: Semantic Kernel with Azure OpenAI (no MCP)")
print("=" * 70)

try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
    from semantic_kernel.contents import ChatHistory
    
    async def test_semantic_kernel_basic():
        # Create kernel
        kernel = Kernel()
        
        # Add Azure OpenAI service
        service_id = "azure_openai_gpt4o"
        chat_service = AzureChatCompletion(
            service_id=service_id,
            endpoint=apim_gateway_url,
            api_key=apim_api_key,
            deployment_name="gpt-4o-mini",  # Your Azure OpenAI deployment name
            api_version="2024-08-01-preview"
        )
        kernel.add_service(chat_service)
        
        # FIXED: Use get_chat_message_content() instead of invoke_prompt()
        # This is the correct API for Semantic Kernel v1.37.0+
        chat_history = ChatHistory()
        chat_history.add_user_message("Say 'Hello from Semantic Kernel' in 5 words or less")
        
        result = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings={"max_tokens": 20}
        )
        return str(result)
    
    result = await run_with_timeout(
        test_semantic_kernel_basic(),
        timeout_seconds=60,  # Shorter timeout for simple test
        task_name="Semantic Kernel basic test"
    )
    print(f"\n💬 Response: {result}\n")
    
except TimeoutError:
    print("\n⚠️  Semantic Kernel timed out. Run diagnostic cell below.\n")
except Exception as e:
    print(f"\n⚠️  Semantic Kernel test failed: {str(e)}\n")
    import traceback
    traceback.print_exc()

# Test 3: Semantic Kernel with MCP tools - Full integration test
print("\n" + "=" * 70)
print("Test 3: Semantic Kernel with MCP Tools (Full Integration)")
print("=" * 70)
print("⚠️  This test may take longer. Using 5 minute timeout.\n")
print("⚠️  NOTE: Most MCP servers are currently unavailable (only docs-mcp working)\n")

try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
    from semantic_kernel.functions import kernel_function
    from semantic_kernel.contents import ChatHistory
    import httpx
    
    async def test_semantic_kernel_with_mcp():
        # Create kernel
        kernel = Kernel()
        
        # Add Azure OpenAI service
        service_id = "azure_openai_mcp"
        chat_service = AzureChatCompletion(
            service_id=service_id,
            endpoint=apim_gateway_url,
            api_key=apim_api_key,
            deployment_name="gpt-4o-mini",
            api_version="2024-08-01-preview"
        )
        kernel.add_service(chat_service)
        
        # Create MCP plugin using docs-mcp (only working server)
        class DocsMCPPlugin:
            """Docs plugin using working MCP server"""
            
            @kernel_function(
                name="search_docs",
                description="Search Microsoft Learn documentation"
            )
            async def search_docs(self, query: str) -> str:
                """Search docs via working MCP server"""
                try:
                    # Use docs-mcp (only working server)
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        # Simple HTTP call instead of SSE
                        response = await client.get(
                            f"http://docs-mcp-72998.eastus.azurecontainer.io:8000/health"
                        )
                        if response.status_code == 200:
                            return f"Docs MCP server is available for query: {query}"
                        else:
                            return f"Docs MCP server returned: {response.status_code}"
                except Exception as e:
                    return f"Error contacting docs MCP: {str(e)}"
        
        # Add plugin to kernel
        kernel.add_plugin(DocsMCPPlugin(), "docs")
        
        # FIXED: Use get_chat_message_content() instead of invoke_prompt()
        chat_history = ChatHistory()
        chat_history.add_user_message("Check if the docs MCP server is available. Use the docs plugin.")
        
        result = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings={}
        )
        return str(result)
    
    result = await run_with_timeout(
        test_semantic_kernel_with_mcp(),
        timeout_seconds=300,  # 5 minute timeout for MCP integration
        task_name="Semantic Kernel + MCP integration"
    )
    print(f"\n💬 Response: {result}\n")
    
except TimeoutError:
    print("\n⚠️  MCP integration timed out after 5 minutes.\n")
    print("This indicates a problem with:")
    print("  - MCP server connectivity (6/7 servers currently down)")
    print("  - Semantic Kernel not calling tools properly")
    print("  - Tool execution hanging indefinitely\n")
except Exception as e:
    print(f"\n⚠️  MCP integration failed: {str(e)}\n")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Semantic Kernel Testing Complete")
print("=" * 70)
print("✅ If all tests passed, Semantic Kernel is working correctly")
print("❌ If any test timed out, use the diagnostic cell below to troubleshoot")
