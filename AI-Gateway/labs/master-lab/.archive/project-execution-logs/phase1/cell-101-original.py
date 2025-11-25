# ========================================================================
# PRODUCTION: AutoGen + APIM + MCP (SSE Transport)
# ========================================================================
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
    from autogen_ext.tools.mcp import SseServerParams, mcp_server_tools
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console
    from autogen_core import CancellationToken
    
    print(f"Task: {task}")
    print(f"MCP Endpoint: {mcp_endpoint}")
    print(f"Timeout: {timeout}s")
    print()
    
    # Create server params for SSE transport
    server_params = SseServerParams(
        url=f"{apim_gateway_url}{mcp_endpoint}",
        headers={
            "Content-Type": "application/json",
            "api-key": api_key
        },
        timeout=timeout
    )
    
    print("📡 Fetching MCP tools...")
    
    try:
        # Get tools with timeout
        tools = await asyncio.wait_for(
            mcp_server_tools(server_params),
            timeout=timeout
        )
        
        print(f"✅ Tools available: {[t.name for t in tools]}")
        print()
        
    except asyncio.TimeoutError:
        print(f"⚠️  Tool fetching timed out after {timeout}s")
        print("Falling back to no-tool mode")
        tools = []
    
    # Create Azure OpenAI client
    model_client = AzureOpenAIChatCompletionClient(
        model=deployment_name,
        azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
        api_key=api_key,
        default_headers={"api-key": api_key}
    )
    
    # Create agent
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=tools,
        system_message="You are a helpful assistant with access to MCP tools."
    )
    
    print("🤖 Running agent...")
    print("-" * 70)
    
    # Run agent with streaming output
    try:
        await Console(
            agent.run_stream(task=task)
        )
    except Exception as e:
        print(f"\n❌ Agent error: {type(e).__name__}: {str(e)}")
        raise
    
    print("-" * 70)

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

print("\n🌤️  EXAMPLE 1: Weather Query")
print("="*70)
start = time.time()

try:
    await run_autogen_agent(
        task="What's the weather in London, Paris, and Tokyo?",
        mcp_endpoint="/weather/sse",
        timeout=30
    )
    print(f"\n⏱️  Total time: {time.time() - start:.2f}s")
except Exception as e:
    print(f"Example 1 failed: {e}")

print("\n" + "="*70)
print("\n✅ AutoGen + APIM integration complete")
print()
print("💡 Key Benefits:")
print("  - SSE transport with built-in timeout")
print("  - Works through APIM gateway")
print("  - Graceful degradation if tools unavailable")
print("  - Streaming output support")
print()
print("📝 To use with different MCP servers:")
print("  - Weather: /weather/sse")
print("  - GitHub: /github/sse")
print("  - Docs: /docs/sse")
print("  - OnCall: /oncall/sse")

print("="*70)