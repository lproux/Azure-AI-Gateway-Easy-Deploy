"""
Simple MCP Tool Calling Helper for Quick Start Labs

Provides minimal functionality to call MCP servers via JSON-RPC protocol
and integrate with Azure OpenAI for tool calling workflows.
"""

import os
import json
import requests
from typing import Dict, Any, Optional


class SimpleMCPClient:
    """Lightweight MCP client for calling tools via JSON-RPC"""

    def __init__(self):
        self.request_id = 0

        # Load MCP server URLs from environment
        self.servers = {
            'weather': os.getenv('MCP_WEATHER_URL'),
            'github': os.getenv('MCP_GITHUB_URL'),
            'docs': os.getenv('MCP_MS_LEARN_URL'),
            'product_catalog': os.getenv('MCP_PRODUCT_CATALOG_URL'),
            'place_order': os.getenv('MCP_PLACE_ORDER_URL'),
        }

    def _next_id(self) -> int:
        """Generate next request ID"""
        self.request_id += 1
        return self.request_id

    def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool via JSON-RPC

        Args:
            server_name: Name of the MCP server ('weather', 'github', 'docs', etc.)
            tool_name: Name of the tool to call
            arguments: Tool arguments as a dictionary

        Returns:
            Tool result dictionary
        """
        server_url = self.servers.get(server_name)

        if not server_url:
            raise ValueError(f"MCP server '{server_name}' not configured")

        # Build JSON-RPC request
        rpc_request = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        # Call MCP server
        try:
            response = requests.post(
                f"{server_url}/mcp/",
                json=rpc_request,
                timeout=30.0
            )
            response.raise_for_status()

            result = response.json()

            if 'error' in result:
                return {
                    "error": True,
                    "message": result['error'].get('message', 'Unknown error')
                }

            return result.get('result', {})

        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }

    def list_tools(self, server_name: str) -> list:
        """
        List available tools from an MCP server

        Args:
            server_name: Name of the MCP server

        Returns:
            List of tool definitions
        """
        server_url = self.servers.get(server_name)

        if not server_url:
            raise ValueError(f"MCP server '{server_name}' not configured")

        # Build JSON-RPC request
        rpc_request = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/list",
            "params": {}
        }

        try:
            response = requests.post(
                f"{server_url}/mcp/",
                json=rpc_request,
                timeout=10.0
            )
            response.raise_for_status()

            result = response.json()
            return result.get('result', {}).get('tools', [])

        except Exception as e:
            print(f"Error listing tools: {e}")
            return []


def test_mcp_with_llm(client, mcp_client: SimpleMCPClient, model: str = "gpt-4o", use_demo_mode: bool = False):
    """
    Test MCP tool calling with Azure OpenAI end-to-end

    Args:
        client: Azure OpenAI client instance
        mcp_client: SimpleMCPClient instance
        model: Model deployment name
        use_demo_mode: If True, use simulated MCP responses (for when servers aren't running)

    Returns:
        Final LLM response after tool execution
    """
    import time
    import uuid
    import random

    # Generate unique session ID to avoid semantic cache hits
    session_id = str(uuid.uuid4())

    # Step 1: Get weather tool definition from MCP server
    print("Step 1: Discovering MCP tools...")
    tools_list = mcp_client.list_tools('weather')

    if not tools_list:
        print("⚠️  MCP servers not responding (may be scaled to zero)")
        print("   Using demo mode to demonstrate the workflow...")
        use_demo_mode = True
        # Simulated tool definition (what would come from MCP server)
        tools_list = [{
            "name": "get_current_weather",
            "description": "Get the current weather for a city",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "country": {"type": "string", "description": "Country code (optional)"}
                },
                "required": ["city"]
            }
        }]
        print(f"✅ Using {len(tools_list)} simulated MCP tool(s) for demo")
    else:
        print(f"✅ Discovered {len(tools_list)} real MCP tool(s)")

    # Convert MCP tool format to OpenAI function format
    openai_tools = []
    for tool in tools_list[:2]:  # Use first 2 tools for simplicity
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.get('name'),
                "description": tool.get('description', ''),
                "parameters": tool.get('inputSchema', {})
            }
        })

    print(f"✅ Found {len(tools_list)} tools, using: {[t['function']['name'] for t in openai_tools]}")
    print()

    # Step 2: Ask LLM to use the tools
    print("Step 2: Asking LLM to use MCP tools...")
    print(f"   Session ID: {session_id[:8]}...")

    # Use unique session ID and varied prompt to avoid semantic cache
    cities = ["London", "Tokyo", "Paris", "Sydney", "Berlin"]
    selected_city = random.choice(cities)

    messages = [
        {"role": "system", "content": f"You are a weather assistant. Session: {session_id}. Always use the weather tool when asked about weather."},
        {"role": "user", "content": f"[Request {session_id[:8]}] What's the current weather in {selected_city}? Please use the weather tool."}
    ]

    # Try multiple models with retry logic for load balancing
    models_to_try = [model, "gpt-4o-mini"] if model != "gpt-4o-mini" else ["gpt-4o-mini"]
    max_retries = 5
    response = None
    assistant_message = None

    for current_model in models_to_try:
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=current_model,
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="required",  # Force tool calling
                    max_tokens=150
                )

                # Check for mock/cached response from APIM
                if response.choices and response.choices[0].message:
                    content = response.choices[0].message.content or ""
                    tool_calls = response.choices[0].message.tool_calls

                    # If we got tool calls, success!
                    if tool_calls:
                        assistant_message = response.choices[0].message
                        break

                    # Check for cached responses
                    if "APIM" in content or "Greetings" in content or "Hello" in content:
                        print(f"⚠️  Attempt {attempt + 1}: Got cached response, regenerating...")
                        # Regenerate session ID and prompt
                        session_id = str(uuid.uuid4())
                        selected_city = random.choice(cities)
                        messages = [
                            {"role": "system", "content": f"You are a weather assistant. Session: {session_id}. Always use the weather tool when asked about weather."},
                            {"role": "user", "content": f"[Request {session_id[:8]}] What's the current weather in {selected_city}? Please use the weather tool."}
                        ]
                        time.sleep(0.3)
                        continue

                assistant_message = response.choices[0].message
                if assistant_message.tool_calls:
                    break  # Success!

            except Exception as e:
                if "DeploymentNotFound" in str(e) and attempt < max_retries - 1:
                    print(f"⚠️  Retry {attempt + 1}/{max_retries} ({current_model})...")
                    time.sleep(0.5)
                elif attempt == max_retries - 1:
                    print(f"⚠️  {current_model} not available, trying fallback...")
                    break
                else:
                    raise

        # Check if we got valid tool calls
        if assistant_message and assistant_message.tool_calls:
            break

    if not assistant_message or not assistant_message.tool_calls:
        content = assistant_message.content if assistant_message else "No response"
        if "Greetings from APIM" in str(content):
            print("❌ Got mock response from APIM - backend pool routing issue")
        else:
            print("❌ LLM did not request any tool calls")
        return None

    print(f"✅ LLM requested {len(assistant_message.tool_calls)} tool call(s)")

    # Add assistant's response to messages
    messages.append({
        "role": "assistant",
        "content": assistant_message.content,
        "tool_calls": [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                }
            }
            for tc in assistant_message.tool_calls
        ]
    })

    # Step 3: Execute tools via MCP
    print()
    print("Step 3: Executing MCP tools...")

    for tool_call in assistant_message.tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"   Calling {tool_name} with args: {arguments}")

        if use_demo_mode:
            # Simulated MCP response for demo
            city = arguments.get('city', selected_city)
            result = {
                "city": city,
                "temperature": random.randint(10, 25),
                "condition": random.choice(["Partly cloudy", "Sunny", "Overcast", "Light rain"]),
                "humidity": random.randint(50, 80),
                "wind_speed": random.randint(5, 20),
                "note": "Simulated response (MCP servers not available)"
            }
            print(f"   Result (simulated): {str(result)[:150]}...")
        else:
            # Call actual MCP server
            result = mcp_client.call_tool('weather', tool_name, arguments)
            print(f"   Result: {str(result)[:200]}...")

        # Add tool result to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Step 4: Get final answer from LLM
    print()
    print("Step 4: Getting final answer from LLM...")

    for attempt in range(max_retries):
        try:
            final_response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=300
            )
            break
        except Exception as e:
            if "DeploymentNotFound" in str(e) and attempt < max_retries - 1:
                print(f"⚠️  Retry {attempt + 1}/{max_retries}...")
            else:
                raise

    final_answer = final_response.choices[0].message.content

    print()
    print("=" * 70)
    print("FINAL ANSWER:")
    print("=" * 70)
    print(final_answer)
    print("=" * 70)

    return final_answer


print("✅ Simple MCP helper module loaded")
print("   Usage: from quick_start.mcp_helper import SimpleMCPClient, test_mcp_with_llm")
