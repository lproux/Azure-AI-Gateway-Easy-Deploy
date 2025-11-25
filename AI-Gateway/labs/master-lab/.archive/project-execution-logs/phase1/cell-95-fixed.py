# ========================================================================
# TECHNIQUE 2: Semantic Kernel Without MCP (Baseline)
# ========================================================================
# FIXED 2025-11-17: Updated to latest Semantic Kernel API
# Changes:
# 1. Removed kernel=kernel parameter from get_chat_message_contents()
# 2. Added proper execution settings object

import time

print("TECHNIQUE 2: Semantic Kernel Without MCP")
print("="*70)
print("Purpose: Verify SK works with Azure OpenAI")
print()

start_time = time.time()
result = "NOT RUN"

try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
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

    # Create execution settings
    settings = AzureChatPromptExecutionSettings(max_tokens=10)

    # Get response - FIXED: removed kernel=kernel, added settings parameter
    response = await service.get_chat_message_content(
        chat_history=history,
        settings=settings
    )

    elapsed = time.time() - start_time
    result = "✅ SUCCESS"

    print(f"\n✅ Response: {response.content}")
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
