# ========================================================================
# TECHNIQUE 15: Hybrid Approach - SK Orchestration + Direct HTTP
# ========================================================================
import time
import asyncio
import httpx

print("TECHNIQUE 15: Hybrid Approach (RECOMMENDED)")
print("="*70)
print("Purpose: Use SK for chat, bypass MCP plugin with direct HTTP")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
    from semantic_kernel.functions import kernel_function
    
    print("Creating Semantic Kernel...")
    
    kernel = Kernel()
    
    service = AzureChatCompletion(
        endpoint=f"{apim_gateway_url}/{inference_api_path}",
        api_key=api_key,
        api_version=inference_api_version,
        deployment_name=deployment_name
    )
    
    kernel.add_service(service)
    
    print("Defining custom tools (no MCP plugin)...")
    
    # Define tools as native Python functions
    class WeatherTools:
        @kernel_function(name="get_weather", description="Get weather for a location")
        async def get_weather(self, location: str) -> str:
            """Get weather via direct APIM call (no MCP)"""
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    # Call weather API directly through APIM
                    response = await client.get(
                        f"{apim_gateway_url}/weather/api/current",
                        params={"location": location},
                        headers={"api-key": api_key}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        return f"Weather in {location}: {data.get('description', 'N/A')}, {data.get('temperature', 'N/A')}°C"
                    else:
                        return f"Weather data unavailable for {location}"
            except Exception as e:
                return f"Error getting weather: {str(e)}"
    
    # Add plugin
    weather_plugin = kernel.add_plugin(WeatherTools(), "weather")
    
    print("Testing hybrid approach...")
    print("Query: 'What\'s the weather in Paris?'")
    
    # Use SK with custom tools
    from semantic_kernel.contents import ChatHistory
    
    history = ChatHistory()
    history.add_user_message("What's the weather in Paris? Use the get_weather function.")
    
    # Get response with function calling
    response = await asyncio.wait_for(
        service.get_chat_message_contents(
            history,
            kernel=kernel,
            arguments=kernel.arguments
        ),
        timeout=30.0
    )
    
    elapsed = time.time() - start_time
    result = "✅ SUCCESS"
    
    print(f"\n✅ Response: {response[0].content}")
    print(f"⏱️  Time: {elapsed:.2f}s")
    print("\n💡 Hybrid approach: SK for orchestration, HTTP for tools")
    
except asyncio.TimeoutError:
    elapsed = time.time() - start_time
    result = "⚠️  TIMEOUT"
    print(f"\n⚠️  Timed out after 30s")
    print(f"⏱️  Time: {elapsed:.2f}s")
    
except Exception as e:
    elapsed = time.time() - start_time
    result = f"❌ FAILED"
    print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
    print(f"⏱️  Time: {elapsed:.2f}s")
    import traceback
    traceback.print_exc()

print(f"\nRESULT: {result}")
print("="*70)