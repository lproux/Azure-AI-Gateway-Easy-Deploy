# Exercise 2.4 & 2.5: Function Calling with MCP Tools (enhanced diagnostics)
# Architecture: MCP connects directly to server, OpenAI goes through APIM

import json
import asyncio
import time
from mcp import ClientSession, McpError
from mcp.client.streamable_http import streamablehttp_client
from mcp.client import session as mcp_client_session
from openai import AzureOpenAI
import nest_asyncio
nest_asyncio.apply()

# CRITICAL FIX: Server uses MCP protocol v1.0; patch client to accept it
# The server responded with "Unsupported protocol version from the server: 1.0"
# This means the client's SUPPORTED_PROTOCOL_VERSIONS doesn't include "1.0"
if "1.0" not in mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS:
    mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS = list(mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS) + ["1.0"]
    print(f"[PATCH] Added MCP protocol v1.0 to supported versions: {mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS}")

# Use the working Docs MCP server - diagnostics found /mcp works with v1.0 protocol
# Force the /mcp path regardless of what mcp.docs.server_url contains
DOCS_MCP_URL = 'http://docs-mcp-24774.eastus.azurecontainer.io:8000/mcp'
print(f"[CONFIG] Using MCP URL: {DOCS_MCP_URL}")

# --- Diagnostic helpers ---
def _format_exception(e: BaseException, indent=0) -> str:
    """Recursively format an exception and its causes, including ExceptionGroups."""
    prefix = "  " * indent
    lines = [f"{prefix}{type(e).__name__}: {str(e).splitlines()[0]}"]

    if isinstance(e, ExceptionGroup):
        lines.append(f"{prefix}  +-- Sub-exceptions ({len(e.exceptions)}):")
        for i, sub_exc in enumerate(e.exceptions):
            lines.append(f"{prefix}      |")
            lines.append(f"{prefix}      +-- Exception {i+1}/{len(e.exceptions)}:")
            lines.append(_format_exception(sub_exc, indent + 4))

    cause = getattr(e, '__cause__', None)
    if cause:
        lines.append(f"{prefix}  +-- Caused by:")
        lines.append(_format_exception(cause, indent + 2))

    context = getattr(e, '__context__', None)
    if context and context is not cause:
        lines.append(f"{prefix}  +-- During handling, another exception occurred:")
        lines.append(_format_exception(context, indent + 2))

    return "\n".join(lines)

async def _diagnostic_handshake(url: str, retries=3, backoff_factor=0.5):
    """Attempt minimal handshake with retries; return tuple (ok, tools_or_error)."""
    last_exception = None
    for attempt in range(retries):
        try:
            async with streamablehttp_client(url) as returned:
                if isinstance(returned, (list, tuple)) and len(returned) >= 2:
                    sender, receiver = returned[0], returned[1]
                else:
                    raise RuntimeError(f"Unexpected streamablehttp_client return shape: {returned}")

                async with ClientSession(sender, receiver) as session:
                    await session.initialize()
                    listed = await session.list_tools()
                    return True, listed.tools
        except Exception as e:
            last_exception = e
            print(f"[Handshake Attempt {attempt+1}/{retries} FAIL]")
            print(_format_exception(e)) # Use the new recursive formatter

            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"\n  Retrying in {sleep_time:.2f}s...")
                await asyncio.sleep(sleep_time)
            else:
                return False, e # Final attempt failed
    return False, last_exception if last_exception else RuntimeError("Handshake failed after all retries.")

async def call_tool(mcp_session, function_name, function_args):
# ... existing code ...
    """Call an MCP tool safely and stringify result."""
    try:
        func_response = await mcp_session.call_tool(function_name, function_args)
        return str(func_response.content)
    except Exception as exc:
        return json.dumps({'error': str(exc), 'type': type(exc).__name__})

async def run_completion_with_tools(server_url, prompt):
# ... existing code ...
    """Run Azure OpenAI completion with MCP tools with extra diagnostics."""
    print(f"Connecting to MCP server: {server_url}")
    ok, tools_or_error = await _diagnostic_handshake(server_url)
    if not ok:
        print("\n[FAIL] Handshake failed after all retries.")
        print("\n--- Final Exception Trace ---")
        print(_format_exception(tools_or_error))
        print("\nSuggestion: The 'Session terminated' error often means the server closed the connection unexpectedly. This can be due to:\n1. Network issue (firewall, proxy).\n2. Server-side crash or restart.\n3. APIM policy terminating long-lived connections (if behind APIM).\n4. Incorrect URL (pointing to a REST endpoint, not an MCP streaming endpoint).")
        return

    tools = tools_or_error
# ... existing code ...
    print(f"[OK] Handshake succeeded. {len(tools)} tools available.")

    try:
        async with streamablehttp_client(server_url) as returned:
            sender, receiver = returned[0], returned[1]
            async with ClientSession(sender, receiver) as session:
                await session.initialize()
                response = await session.list_tools()
                tools = response.tools

                openai_tools = [{'type': 'function', 'function': {'name': t.name, 'description': t.description, 'parameters': t.inputSchema}} for t in tools]

                client = AzureOpenAI(
                    azure_endpoint=f'{apim_resource_gateway_url}/{inference_api_path}',
                    api_key=api_key,
                    api_version=inference_api_version,
                )

                messages = [{'role': 'user', 'content': prompt}]
                print(f'\nQuery: {prompt}')

                response = client.chat.completions.create(model=models_config[0]['name'], messages=messages, tools=openai_tools)
                response_message = response.choices[0].message
                tool_calls = getattr(response_message, 'tool_calls', None)

                if not tool_calls:
                    print(f'[INFO] No tool calls needed. Response: {response_message.content}')
                    return

                messages.append(response_message)
                print('\nExecuting MCP tools...')
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments or '{}')
                    print(f'  Tool: {function_name}')
                    function_response = await call_tool(session, function_name, function_args)
                    messages.append({'tool_call_id': tool_call.id, 'role': 'tool', 'name': function_name, 'content': function_response})

                print('\nGetting final answer...')
                second_response = client.chat.completions.create(model=models_config[0]['name'], messages=messages)
                print('\n[ANSWER]')
                print(second_response.choices[0].message.content)

    except Exception as exc:
        print('[ERROR] Unexpected failure during tool run.')
        print(_format_exception(exc))
        return

# Example usage (Exercise 6.2)
async def run_agent_example():
# ... existing code ...
    queries = [
        'List available document-related tools and summarize their purpose.',
        'Retrieve docs for MCP server publishing and give key steps.'
    ]
    for q in queries:
        print('='*80)
        await run_completion_with_tools(DOCS_MCP_URL, q)
        print()

await run_agent_example()