# ========================================================================
# TECHNIQUE 2: Semantic Kernel Without MCP (Baseline)
# ========================================================================
import time

print("TECHNIQUE 2: Semantic Kernel Without MCP")
print("="*70)
print("Purpose: Verify SK works with Azure OpenAI")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
    from semantic_kernel.contents import ChatHistory
    
    print("Creating Kernel...")
    kernel = Kernel()
    
    print("Adding Azure OpenAI service...")
    service = AzureChatCompletion(
        endpoint=f"{apim_gateway_url}/{inference_api_path}",
        api_key=api_key,
        api_version=inference_api_version,
        deployment_name=deployment_name
    )
    
    kernel.add_service(service)
    
    print("Testing with simple prompt...")
    
    # Create chat history
    history = ChatHistory()
    history.add_user_message("What is 2+2? Answer with just the number.")
    
    # Get response
    response = await service.get_chat_message_contents(history, kernel=kernel)
    
    elapsed = time.time() - start_time
    result = "✅ SUCCESS"
    
    print(f"\n✅ Response: {response[0].content}")
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