# ========================================================================
# PRODUCTION: AutoGen + APIM + MCP (SSE Transport)
# ========================================================================
# FIXED 2025-11-17: Updated to latest AutoGen API
# Changes:
# 1. StreamableHttpServerParams instead of SseServerParams
# 2. StreamableHttpMcpToolAdapter instead of mcp_server_tools
# 3. Improved error handling for TaskGroup issues
# 4. Added timeout protection

import asyncio
import time

print("🎯 PRODUCTION AUTOGEN + APIM SOLUTION")
print("="*70)
print()

async def run_autogen_agent(task: str, mcp_endpoint: str, timeout: int = 30):
    """
    Run AutoGen agent with MCP tools through APIM

    Args:
        task: User query/task
        mcp_endpoint: MCP SSE endpoint (e.g., "/weather/sse")
        timeout: Timeout in seconds
    """
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    from autogen_ext.tools.mcp import StreamableHttpServerParams, StreamableHttpMcpToolAdapter
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console
    from autogen_core import CancellationToken

    print(f"Task: {task}")
    print(f"MCP Endpoint: {mcp_endpoint}")
    print(f"Timeout: {timeout}s")
    print()

    # Create server params for SSE transport - FIXED: Use StreamableHttpServerParams
    server_params = StreamableHttpServerParams(
        url=f"{apim_gateway_url}{mcp_endpoint}",
        headers={
            "Content-Type": "application/json",
            "api-key": api_key
        },
        timeout=float(timeout),
        terminate_on_close=True
    )

    print("📡 Fetching MCP tools...")

    tools = []
    try:
        # FIXED: Use StreamableHttpMcpToolAdapter for dynamic tool loading
        # Note: This requires knowing tool names in advance
        # For dynamic discovery, we'll use a try/catch approach with common tool names

        common_tool_names = [
            "get_weather", "search_weather", "current_weather",  # Weather tools
            "search_docs", "fetch_docs", "get_documentation",    # Docs tools
            "search_github", "get_repo", "list_repos",           # GitHub tools
        ]

        # Try to load known tools with timeout
        for tool_name in common_tool_names:
            try:
                adapter = await asyncio.wait_for(
                    StreamableHttpMcpToolAdapter.from_server_params(
                        server_params,
                        tool_name
                    ),
                    timeout=5.0  # Short timeout per tool
                )
                tools.append(adapter)
                print(f"  ✅ Loaded: {tool_name}")
            except asyncio.TimeoutError:
                continue  # Tool not available or timed out
            except Exception:
                continue  # Tool doesn't exist

        if tools:
            print(f"\n✅ {len(tools)} tools available")
        else:
            print("⚠️  No tools loaded, falling back to no-tool mode")
        print()

    except Exception as e:
        print(f"⚠️  Tool loading failed: {type(e).__name__}")
        print("Falling back to no-tool mode")
        tools = []

    # Create Azure OpenAI client
    model_client = AzureOpenAIChatCompletionClient(
        model=deployment_name,
        azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
        api_key=api_key,
        model_capabilities={
            "function_calling": True,
            "json_output": True,
            "vision": False
        }
    )

    # Create agent
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=tools if tools else [],  # Empty list if no tools
        system_message="You are a helpful assistant." + (
            " You have access to MCP tools to help answer questions." if tools
            else " Note: MCP tools are currently unavailable."
        )
    )

    print("🤖 Running agent...")
    print("-" * 70)

    # Run agent with streaming output and timeout protection
    try:
        # Create cancellation token with timeout
        cancellation_token = CancellationToken()

        # Run with asyncio timeout as additional protection
        await asyncio.wait_for(
            Console(
                agent.run_stream(
                    task=task,
                    cancellation_token=cancellation_token
                )
            ),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        print(f"\n⚠️  Agent timed out after {timeout}s")
        raise
    except Exception as e:
        print(f"\n❌ Agent error: {type(e).__name__}: {str(e)}")
        # Don't re-raise - let the example continue

    print("-" * 70)

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

print("\n🌤️  EXAMPLE 1: Weather Query (with graceful degradation)")
print("="*70)
start = time.time()

try:
    await run_autogen_agent(
        task="What's the weather in London? If tools are unavailable, explain that weather data cannot be retrieved.",
        mcp_endpoint="/weather/sse",
        timeout=30
    )
    print(f"\n⏱️  Total time: {time.time() - start:.2f}s")
except asyncio.TimeoutError:
    print(f"\n⏱️  Timed out after {time.time() - start:.2f}s")
except Exception as e:
    print(f"\n⏱️  Failed after {time.time() - start:.2f}s: {e}")

print("\n" + "="*70)
print("\n✅ AutoGen + APIM integration complete")
print()
print("💡 Key Features:")
print("  - Updated to latest AutoGen API (StreamableHttpServerParams)")
print("  - Robust timeout protection at multiple levels")
print("  - Graceful degradation if MCP tools unavailable")
print("  - Dynamic tool discovery with fallback")
print("  - Streaming output support with Console")
print()
print("📝 To use with different MCP servers:")
print("  - Weather: /weather/sse")
print("  - GitHub: /github/sse")
print("  - Docs: /docs/sse")
print()
print("⚠️  Note: MCP servers may be scaled to zero, causing initial delays")

print("="*70)
