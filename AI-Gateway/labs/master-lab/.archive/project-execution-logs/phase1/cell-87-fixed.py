# Exercise 2.4 & 2.5: Function Calling with MCP Tools (FIXED 2025-11-17)
# Architecture: MCP connects directly to server, OpenAI goes through APIM
# FIXES:
# 1. Correct streamablehttp_client unpacking: (read, write, _) instead of returned[0], returned[1]
# 2. Simplified error handling
# 3. Removed duplicate handshake logic

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
if "1.0" not in mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS:
    mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS = list(mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS) + ["1.0"]
    print(f"[PATCH] Added MCP protocol v1.0 to supported versions: {mcp_client_session.SUPPORTED_PROTOCOL_VERSIONS}")

# Use the working Docs MCP server
DOCS_MCP_URL = 'http://docs-mcp-24774.eastus.azurecontainer.io:8000/mcp'
print(f"[CONFIG] Using MCP URL: {DOCS_MCP_URL}")

# --- Diagnostic helpers ---
def _format_exception(e: BaseException, indent=0) -> str:
    """Recursively format an exception and its causes, including ExceptionGroups."""
    prefix = "  " * indent
    lines = [f"{prefix}{type(e).__name__}: {str(e).splitlines()[0] if str(e) else 'No message'}"]

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

async def call_tool(mcp_session, function_name, function_args):
    """Call an MCP tool safely and stringify result."""
    try:
        func_response = await mcp_session.call_tool(function_name, function_args)
        return str(func_response.content)
    except Exception as exc:
        return json.dumps({'error': str(exc), 'type': type(exc).__name__})

async def run_completion_with_tools(server_url, prompt):
    """Run Azure OpenAI completion with MCP tools with extra diagnostics."""
    print("="*80)
    print(f"Connecting to MCP server: {server_url}")

    try:
        # FIXED: Correct unpacking of streamablehttp_client return value
        async with streamablehttp_client(server_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize session
                await session.initialize()

                # Get available tools
                tools_response = await session.list_tools()
                tools = tools_response.tools

                print(f"[OK] Handshake succeeded. {len(tools)} tools available.")

                # Convert MCP tools to OpenAI format
                openai_tools = [{
                    'type': 'function',
                    'function': {
                        'name': t.name,
                        'description': t.description,
                        'parameters': t.inputSchema
                    }
                } for t in tools]

                # Initialize OpenAI client (using variables from earlier cells)
                client = AzureOpenAI(
                    azure_endpoint=f'{apim_resource_gateway_url}/{inference_api_path}',
                    api_key=api_key,
                    api_version=inference_api_version,
                )

                messages = [{'role': 'user', 'content': prompt}]
                print(f'\nQuery: {prompt}')

                # First completion - get tool calls
                response = client.chat.completions.create(
                    model='gpt-4o-mini',  # Use a known deployed model
                    messages=messages,
                    tools=openai_tools
                )

                response_message = response.choices[0].message
                tool_calls = getattr(response_message, 'tool_calls', None)

                if not tool_calls:
                    print(f'[INFO] No tool calls needed. Response: {response_message.content}')
                    return

                # Add assistant message to history
                messages.append(response_message)

                # Execute tool calls
                print('\nExecuting MCP tools...')
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments or '{}')
                    print(f'  Tool: {function_name}({function_args})')

                    # Call MCP tool
                    function_response = await call_tool(session, function_name, function_args)

                    # Add tool response to messages
                    messages.append({
                        'tool_call_id': tool_call.id,
                        'role': 'tool',
                        'name': function_name,
                        'content': function_response
                    })

                # Get final answer with tool results
                print('\nGetting final answer...')
                second_response = client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=messages
                )

                print('\n[ANSWER]')
                print(second_response.choices[0].message.content)

    except Exception as exc:
        print('[ERROR] Unexpected failure during tool run.')
        print(_format_exception(exc))
        print("\n[TROUBLESHOOTING]")
        print("  • Verify MCP server is running and accessible")
        print("  • Check URL is correct (should end with /mcp)")
        print("  • Ensure network connectivity (firewall, proxy)")
        print("  • Verify protocol version compatibility")

# Example usage (Exercise 2.4 & 2.5)
async def run_agent_example():
    queries = [
        'List available document-related tools and summarize their purpose.',
        'Retrieve docs for MCP server publishing and give key steps.'
    ]

    for q in queries:
        await run_completion_with_tools(DOCS_MCP_URL, q)
        print()

# Run the example
await run_agent_example()

print("[OK] MCP Function Calling Complete!")
