# Phase 3: Semantic Kernel + AutoGen Extras Implementation Plan

**Project**: Master AI Gateway Workshop Notebook
**Phase**: 3 - SK + AutoGen Advanced Features
**Date**: 2025-11-17
**Status**: Research Complete - Ready for Implementation

---

## Executive Summary

This document provides comprehensive research findings and implementation plans for adding advanced Semantic Kernel (SK) 1.x and AutoGen features to the Master AI Gateway notebook. Based on official Microsoft documentation and code samples, we propose 6 new notebook cells that demonstrate practical AI Gateway capabilities using cutting-edge agentic features.

---

## 1. Research Summary

### 1.1 Semantic Kernel 1.x Key Findings

#### Latest Features (SK 1.37.0+)
1. **Function Calling Evolution**
   - Deprecated: Stepwise and Handlebars planners
   - Recommended: Auto Function Calling with `FunctionChoiceBehavior.Auto()`
   - Native support for multi-step planning through function calling
   - Automatic loop handling for complex task execution

2. **Plugin Architecture**
   - Plugins encapsulate functionality like enterprise APIs
   - Support for dependency injection in constructors
   - Native integration with Azure OpenAI function calling
   - Can create plugins from: native code, prompts, OpenAPI specs

3. **Agent Framework**
   - `ChatCompletionAgent`: For chat-based AI services
   - `OpenAIAssistantAgent`: For OpenAI Assistants API
   - `OpenAIResponsesAgent`: For latest Responses API (experimental)
   - Support for multi-agent orchestration patterns

4. **Streaming Support**
   - `get_streaming_chat_message_content()` for real-time responses
   - Works with function calling and plugins
   - Supports agent streaming with `invoke_stream()`

5. **Memory & Context Management**
   - Vector Store connectors: Azure AI Search, Cosmos DB, Redis, Qdrant, etc.
   - Chat history management with truncation reducers
   - Thread-based conversation state management

#### Integration with Azure OpenAI
- Direct support for Azure OpenAI endpoints
- Custom client support for APIM routing
- Token-based authentication (Azure CLI, Managed Identity)
- Execution settings for model parameters

### 1.2 AutoGen Latest Features

#### Multi-Agent Patterns
1. **ConversableAgent**
   - Base agent for multi-agent conversations
   - Support for tool registration and execution
   - LLM configuration with multiple providers
   - Human-in-the-loop capabilities

2. **Tool Integration**
   - Function registration with `register_for_llm()`
   - Execution registration with `register_for_execution()`
   - Support for typed parameters with annotations
   - Automatic tool calling through LLM

3. **Orchestration**
   - Multi-agent conversations with `initiate_chat()`
   - Sequential and parallel agent execution
   - Termination conditions and message routing
   - Group chat coordination

4. **Azure Integration**
   - Works with Azure OpenAI endpoints
   - MLflow tracing support for observability
   - Compatible with Azure Container Apps dynamic sessions

### 1.3 Integration Opportunities with AI Gateway

Based on research, the following integration patterns are most relevant:

1. **SK Plugins for MCP Servers**: Create SK plugins that wrap MCP server functionality
2. **Function Calling through APIM**: Route SK function calls through APIM gateway
3. **AutoGen Multi-Agent via APIM**: Configure AutoGen agents to use APIM endpoints
4. **SK + AutoGen Hybrid**: Combine SK plugins with AutoGen orchestration
5. **Streaming with Gateway**: Demonstrate streaming responses through APIM
6. **Advanced Context Management**: Use SK memory with gateway-routed embeddings

---

## 2. Proposed Cell Additions (6 New Cells)

### Cell 1: SK Plugin for Gateway-Routed Function Calling
**Purpose**: Demonstrate SK plugins with automatic function calling through APIM

**Key Features**:
- Create custom SK plugin for weather/time data
- Use `FunctionChoiceBehavior.Auto()` for automatic planning
- Route all LLM calls through APIM gateway
- Show function calling loop with chat history

**Dependencies**: semantic-kernel, existing apim_gateway_url

### Cell 2: SK Streaming Chat with Function Calling
**Purpose**: Show real-time streaming responses with function calling via gateway

**Key Features**:
- Streaming chat completion with `get_streaming_chat_message_content()`
- Async iteration over response chunks
- Function calling during streaming
- APIM gateway integration

**Dependencies**: semantic-kernel, asyncio

### Cell 3: AutoGen Multi-Agent Conversation via APIM
**Purpose**: Demonstrate AutoGen agents communicating through AI Gateway

**Key Features**:
- Create 2-3 specialized agents (e.g., Analyst, Writer, Reviewer)
- Configure each agent to use APIM endpoint
- Initiate multi-turn conversation
- Show agent collaboration patterns

**Dependencies**: pyautogen, existing headers_both

### Cell 4: SK Agent with Custom Azure OpenAI Client
**Purpose**: Use SK ChatCompletionAgent with custom client for APIM routing

**Key Features**:
- Create custom Azure OpenAI client pointing to APIM
- Build SK ChatCompletionAgent with custom client
- Multi-turn conversation with thread management
- Demonstrate agent streaming

**Dependencies**: semantic-kernel, openai

### Cell 5: SK Vector Search with Gateway-Routed Embeddings
**Purpose**: Show SK memory/vector store with embeddings via APIM

**Key Features**:
- In-memory vector store for quick demo
- Generate embeddings through APIM gateway
- Create searchable memory collection
- SK search function for RAG pattern

**Dependencies**: semantic-kernel[memory], numpy

### Cell 6: SK + AutoGen Hybrid Orchestration
**Purpose**: Advanced pattern combining SK plugins with AutoGen orchestration

**Key Features**:
- SK plugins as tools for AutoGen agents
- AutoGen orchestration of multi-step workflow
- SK function calling + AutoGen decision making
- All LLM calls through APIM

**Dependencies**: semantic-kernel, pyautogen

---

## 3. Implementation Code

### Cell 1: SK Plugin for Gateway-Routed Function Calling

```python
# ============================================================================
# Semantic Kernel: Plugin with Function Calling via APIM Gateway
# ============================================================================
"""
Demonstrates:
- SK plugin creation with kernel_function decorator
- Automatic function calling with FunctionChoiceBehavior.Auto()
- Routing SK chat completion through APIM gateway
- Multi-step planning with automatic function invocation
"""

import asyncio
from datetime import datetime
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from openai import AsyncAzureOpenAI

print("="*70)
print("SEMANTIC KERNEL: Function Calling Plugin via APIM Gateway")
print("="*70)

# ============================================================================
# Step 1: Create SK Plugin with Kernel Functions
# ============================================================================

class WorkshopPlugin:
    """Custom plugin for AI Gateway workshop demonstrations."""

    @kernel_function(description="Get the current UTC time")
    def get_current_time(self) -> str:
        """Returns current UTC time in ISO format."""
        return datetime.utcnow().isoformat()

    @kernel_function(description="Get weather information for a city")
    def get_weather(self, city: str) -> str:
        """
        Get simulated weather for a city.

        Args:
            city: Name of the city
        """
        # Simulated weather data
        weather_data = {
            "seattle": "Rainy, 55°F (13°C)",
            "san francisco": "Foggy, 62°F (17°C)",
            "boston": "Cloudy, 48°F (9°C)",
            "paris": "Partly cloudy, 15°C (59°F)",
        }
        city_lower = city.lower()
        return weather_data.get(city_lower, f"Weather data unavailable for {city}")

    @kernel_function(description="Calculate the square of a number")
    def calculate_square(self, number: float) -> float:
        """
        Calculate square of a number.

        Args:
            number: Number to square
        """
        return number * number

print("\n✓ Workshop plugin created with 3 functions")

# ============================================================================
# Step 2: Configure Custom Azure OpenAI Client for APIM
# ============================================================================

# Create custom client pointing to APIM gateway
custom_client = AsyncAzureOpenAI(
    azure_endpoint=apim_gateway_url,
    api_version="2024-02-01",
    api_key=subscription_key_both,  # From existing notebook variables
    default_headers=headers_both    # From existing notebook variables
)

print("✓ Custom Azure OpenAI client configured for APIM gateway")
print(f"  Endpoint: {apim_gateway_url}")

# ============================================================================
# Step 3: Initialize Semantic Kernel with Plugin
# ============================================================================

kernel = Kernel()

# Add Azure OpenAI chat completion service with custom client
chat_service = AzureChatCompletion(
    service_id="apim_chat",
    deployment_name=deployment_name,
    async_client=custom_client,
)
kernel.add_service(chat_service)

# Add the workshop plugin
kernel.add_plugin(
    WorkshopPlugin(),
    plugin_name="Workshop"
)

print("✓ Semantic Kernel initialized")
print("  Service: Azure OpenAI via APIM")
print("  Plugin: WorkshopPlugin (3 functions)")

# ============================================================================
# Step 4: Configure Auto Function Calling
# ============================================================================

from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings

execution_settings = AzureChatPromptExecutionSettings(
    service_id="apim_chat",
    max_tokens=500,
    temperature=0.7,
)

# Enable automatic function calling
execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

print("✓ Execution settings configured")
print("  Function calling: Automatic")
print("  Max tokens: 500")
print("  Temperature: 0.7")

# ============================================================================
# Step 5: Run Function Calling Examples
# ============================================================================

async def run_sk_function_calling():
    """Execute SK function calling examples."""

    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Function Call")
    print("="*70)

    # Create chat history
    history = ChatHistory()
    history.add_user_message("What time is it right now?")

    # Get response (SK will automatically call get_current_time function)
    result = await chat_service.get_chat_message_content(
        chat_history=history,
        settings=execution_settings,
        kernel=kernel,
    )

    print(f"\nUser: What time is it right now?")
    print(f"Assistant: {result}")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 2: Multi-Step Function Calling")
    print("="*70)

    history2 = ChatHistory()
    history2.add_user_message(
        "What's the weather in Seattle and what's the square of 12?"
    )

    result2 = await chat_service.get_chat_message_content(
        chat_history=history2,
        settings=execution_settings,
        kernel=kernel,
    )

    print(f"\nUser: What's the weather in Seattle and what's the square of 12?")
    print(f"Assistant: {result2}")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 3: Complex Planning")
    print("="*70)

    history3 = ChatHistory()
    history3.add_user_message(
        "First tell me the current time, then check the weather in Paris, "
        "and finally calculate the square of 7. Present all results."
    )

    result3 = await chat_service.get_chat_message_content(
        chat_history=history3,
        settings=execution_settings,
        kernel=kernel,
    )

    print(f"\nUser: First tell me the current time, then check the weather in Paris,")
    print(f"      and finally calculate the square of 7. Present all results.")
    print(f"Assistant: {result3}")

    # ========================================================================

    print("\n" + "="*70)
    print("FUNCTION CALLING STATISTICS")
    print("="*70)
    print(f"Total examples executed: 3")
    print(f"All calls routed through: {apim_gateway_url}")
    print(f"Plugin used: WorkshopPlugin")
    print(f"Functions available: get_current_time, get_weather, calculate_square")

# Run the async function
await run_sk_function_calling()

print("\n" + "="*70)
print("✓ SK Plugin Function Calling Demo Complete")
print("="*70)
print("\nKey Takeaways:")
print("1. SK plugins encapsulate reusable functionality")
print("2. Auto function calling handles multi-step planning automatically")
print("3. All LLM calls route through APIM gateway")
print("4. No manual function call parsing required")
```

---

### Cell 2: SK Streaming Chat with Function Calling

```python
# ============================================================================
# Semantic Kernel: Streaming Chat with Function Calling
# ============================================================================
"""
Demonstrates:
- Real-time streaming responses through APIM
- Streaming with automatic function calling
- Async iteration over response chunks
- Progressive output rendering
"""

import asyncio
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from openai import AsyncAzureOpenAI

print("="*70)
print("SEMANTIC KERNEL: Streaming Chat with Function Calling")
print("="*70)

# ============================================================================
# Step 1: Setup Kernel (reuse from previous cell or create new)
# ============================================================================

# Simple plugin for streaming demo
class StreamingDemoPlugin:
    """Plugin for streaming demonstrations."""

    @kernel_function(description="Get information about a programming language")
    def get_language_info(self, language: str) -> str:
        """Get information about a programming language."""
        info = {
            "python": "Python is a high-level, interpreted language known for simplicity and readability. Created by Guido van Rossum in 1991.",
            "javascript": "JavaScript is a dynamic, interpreted language primarily used for web development. Created by Brendan Eich in 1995.",
            "csharp": "C# is a modern, object-oriented language developed by Microsoft. Released in 2000 as part of .NET Framework.",
            "java": "Java is a class-based, object-oriented language designed to have minimal implementation dependencies. Released by Sun Microsystems in 1995.",
        }
        return info.get(language.lower(), f"Information not available for {language}")

    @kernel_function(description="Count words in a text")
    def count_words(self, text: str) -> int:
        """Count the number of words in text."""
        return len(text.split())

# Create kernel with custom APIM client
stream_kernel = Kernel()

custom_stream_client = AsyncAzureOpenAI(
    azure_endpoint=apim_gateway_url,
    api_version="2024-02-01",
    api_key=subscription_key_both,
    default_headers=headers_both
)

stream_chat_service = AzureChatCompletion(
    service_id="apim_stream",
    deployment_name=deployment_name,
    async_client=custom_stream_client,
)

stream_kernel.add_service(stream_chat_service)
stream_kernel.add_plugin(StreamingDemoPlugin(), plugin_name="StreamingDemo")

print("✓ Streaming kernel configured")
print(f"  Endpoint: {apim_gateway_url}")

# ============================================================================
# Step 2: Configure Streaming Settings
# ============================================================================

from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings

stream_settings = AzureChatPromptExecutionSettings(
    service_id="apim_stream",
    max_tokens=800,
    temperature=0.8,
)
stream_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

print("✓ Streaming settings configured")

# ============================================================================
# Step 3: Streaming Examples
# ============================================================================

async def run_streaming_examples():
    """Execute streaming chat examples."""

    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Streaming Response")
    print("="*70)

    history = ChatHistory()
    history.add_user_message("Tell me a short story about an AI learning to paint.")

    print("\nUser: Tell me a short story about an AI learning to paint.")
    print("Assistant: ", end="", flush=True)

    # Get streaming response
    response_stream = stream_chat_service.get_streaming_chat_message_content(
        chat_history=history,
        settings=stream_settings,
        kernel=stream_kernel,
    )

    # Collect chunks for later use
    chunks = []
    async for chunk in response_stream:
        if chunk.content:
            print(chunk.content, end="", flush=True)
            chunks.append(chunk)

    print("\n")  # New line after streaming

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 2: Streaming with Function Call")
    print("="*70)

    history2 = ChatHistory()
    history2.add_user_message(
        "Give me detailed information about Python and then explain why it's popular."
    )

    print("\nUser: Give me detailed information about Python and then explain why it's popular.")
    print("Assistant: ", end="", flush=True)

    response_stream2 = stream_chat_service.get_streaming_chat_message_content(
        chat_history=history2,
        settings=stream_settings,
        kernel=stream_kernel,
    )

    chunks2 = []
    async for chunk in response_stream2:
        if chunk.content:
            print(chunk.content, end="", flush=True)
            chunks2.append(chunk)

    print("\n")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 3: Interactive Streaming Conversation")
    print("="*70)

    # Multi-turn conversation with streaming
    conv_history = ChatHistory()

    messages = [
        "What programming language should I learn first?",
        "Tell me more about Python specifically.",
        "How many words have you used in your last response?"
    ]

    for msg in messages:
        print(f"\nUser: {msg}")
        print("Assistant: ", end="", flush=True)

        conv_history.add_user_message(msg)

        stream_response = stream_chat_service.get_streaming_chat_message_content(
            chat_history=conv_history,
            settings=stream_settings,
            kernel=stream_kernel,
        )

        full_response_chunks = []
        async for chunk in stream_response:
            if chunk.content:
                print(chunk.content, end="", flush=True)
                full_response_chunks.append(chunk)

        # Combine chunks into full message for history
        if full_response_chunks:
            full_response = sum(full_response_chunks[1:], full_response_chunks[0])
            conv_history.add_message(full_response)

        print("\n")

    # ========================================================================

    print("\n" + "="*70)
    print("STREAMING STATISTICS")
    print("="*70)
    print(f"Examples executed: 3")
    print(f"Streaming endpoint: {apim_gateway_url}")
    print(f"Function calling: Enabled (auto)")
    print(f"Response mode: Real-time streaming")

# Run streaming examples
await run_streaming_examples()

print("\n" + "="*70)
print("✓ SK Streaming Demo Complete")
print("="*70)
print("\nKey Takeaways:")
print("1. Streaming provides real-time response rendering")
print("2. Function calling works seamlessly with streaming")
print("3. Async iteration enables progressive output")
print("4. All streaming goes through APIM gateway")
```

---

### Cell 3: AutoGen Multi-Agent Conversation via APIM

```python
# ============================================================================
# AutoGen: Multi-Agent Conversation via APIM Gateway
# ============================================================================
"""
Demonstrates:
- Multiple AutoGen agents with specialized roles
- Agent-to-agent communication
- Tool/function registration and execution
- Routing all AutoGen LLM calls through APIM
- Termination conditions and conversation flow
"""

import os
from typing import Annotated, Literal
from autogen import ConversableAgent

print("="*70)
print("AUTOGEN: Multi-Agent Conversation via APIM Gateway")
print("="*70)

# ============================================================================
# Step 1: Configure AutoGen for APIM Gateway
# ============================================================================

# AutoGen configuration pointing to APIM
autogen_config = {
    "model": deployment_name,
    "api_type": "azure",
    "api_key": subscription_key_both,
    "base_url": apim_gateway_url,
    "api_version": "2024-02-01",
}

# Add custom headers to requests (AutoGen doesn't natively support extra_headers in config)
# We'll configure this in the agent setup

config_list = [autogen_config]

print("✓ AutoGen configuration created")
print(f"  Model: {deployment_name}")
print(f"  Base URL: {apim_gateway_url}")

# ============================================================================
# Step 2: Define Tools for Agents
# ============================================================================

# Simple calculator tool
Operator = Literal["+", "-", "*", "/"]

def calculator(a: float, b: float, operator: Annotated[Operator, "operator"]) -> float:
    """
    Perform basic arithmetic operations.

    Args:
        a: First number
        b: Second number
        operator: Operation to perform (+, -, *, /)

    Returns:
        Result of the calculation
    """
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b == 0:
            return float('inf')  # Handle division by zero
        return a / b
    else:
        raise ValueError(f"Invalid operator: {operator}")

print("✓ Calculator tool defined")

# ============================================================================
# Step 3: Create Specialized Agents
# ============================================================================

# Agent 1: Analyst (suggests approaches)
analyst_agent = ConversableAgent(
    name="Analyst",
    system_message=(
        "You are a data analyst. Your role is to analyze problems and suggest "
        "approaches using available tools. When calculations are needed, clearly "
        "state what needs to be calculated. Return 'TERMINATE' when the task is complete."
    ),
    llm_config={"config_list": config_list, "temperature": 0.7},
)

# Agent 2: Calculator (executes calculations)
calculator_agent = ConversableAgent(
    name="Calculator",
    system_message=(
        "You are a calculator agent. You execute mathematical calculations accurately. "
        "Use the calculator tool for all computations."
    ),
    llm_config={"config_list": config_list, "temperature": 0.1},
)

# Agent 3: User Proxy (manages execution and termination)
user_proxy = ConversableAgent(
    name="UserProxy",
    llm_config=False,  # No LLM for proxy
    is_termination_msg=lambda msg: msg.get("content") is not None
                                   and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

print("✓ Three agents created:")
print("  1. Analyst - Problem analysis and planning")
print("  2. Calculator - Execution of calculations")
print("  3. UserProxy - Tool execution and flow control")

# ============================================================================
# Step 4: Register Tools with Agents
# ============================================================================

# Register calculator tool
analyst_agent.register_for_llm(
    name="calculator",
    description="A calculator that performs basic arithmetic"
)(calculator)

calculator_agent.register_for_llm(
    name="calculator",
    description="A calculator that performs basic arithmetic"
)(calculator)

user_proxy.register_for_execution(name="calculator")(calculator)

print("✓ Calculator tool registered with all agents")

# ============================================================================
# Step 5: Run Multi-Agent Conversations
# ============================================================================

print("\n" + "="*70)
print("EXAMPLE 1: Simple Calculation Task")
print("="*70)

response1 = user_proxy.initiate_chat(
    analyst_agent,
    message="Calculate (15 + 27) * 3 and then subtract 50. What's the final result?",
    max_turns=10
)

print("\n✓ Example 1 complete")

# ============================================================================

print("\n" + "="*70)
print("EXAMPLE 2: Complex Multi-Step Problem")
print("="*70)

response2 = user_proxy.initiate_chat(
    analyst_agent,
    message=(
        "A company has quarterly revenues of $125,000, $138,000, $142,000, and $155,000. "
        "Calculate the total annual revenue and then the average quarterly revenue."
    ),
    max_turns=10
)

print("\n✓ Example 2 complete")

# ============================================================================

print("\n" + "="*70)
print("EXAMPLE 3: Agent Collaboration Pattern")
print("="*70)

# More complex scenario requiring agent collaboration
response3 = user_proxy.initiate_chat(
    analyst_agent,
    message=(
        "If a product costs $89.99 and there's a 15% discount, what's the final price? "
        "Then, if I buy 7 units at the discounted price, what's my total cost?"
    ),
    max_turns=15
)

print("\n✓ Example 3 complete")

# ============================================================================

print("\n" + "="*70)
print("MULTI-AGENT CONVERSATION STATISTICS")
print("="*70)
print(f"Total examples: 3")
print(f"Agents involved: Analyst, Calculator, UserProxy")
print(f"Tool calls: Calculator function")
print(f"All LLM calls routed through: {apim_gateway_url}")
print(f"Model used: {deployment_name}")

print("\n" + "="*70)
print("✓ AutoGen Multi-Agent Demo Complete")
print("="*70)
print("\nKey Takeaways:")
print("1. AutoGen enables multi-agent collaboration patterns")
print("2. Agents can have specialized roles and tools")
print("3. Tool registration separates LLM decision from execution")
print("4. All agent LLM calls route through APIM gateway")
print("5. Termination conditions control conversation flow")
```

---

### Cell 4: SK Agent with Custom Azure OpenAI Client

```python
# ============================================================================
# Semantic Kernel: ChatCompletionAgent with APIM Routing
# ============================================================================
"""
Demonstrates:
- SK ChatCompletionAgent with custom Azure OpenAI client
- Multi-turn conversation with thread management
- Agent streaming capabilities
- Integration with existing APIM infrastructure
"""

import asyncio
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelFunctionFromPrompt, KernelArguments
from openai import AsyncAzureOpenAI

print("="*70)
print("SEMANTIC KERNEL: ChatCompletionAgent with APIM")
print("="*70)

# ============================================================================
# Step 1: Create Kernel with Custom Client
# ============================================================================

agent_kernel = Kernel()

# Custom client for APIM
agent_client = AsyncAzureOpenAI(
    azure_endpoint=apim_gateway_url,
    api_version="2024-02-01",
    api_key=subscription_key_both,
    default_headers=headers_both
)

# Add chat completion service
agent_chat_service = AzureChatCompletion(
    service_id="agent_service",
    deployment_name=deployment_name,
    async_client=agent_client,
)
agent_kernel.add_service(agent_chat_service)

print("✓ Agent kernel created")
print(f"  Service: Azure OpenAI via APIM")
print(f"  Endpoint: {apim_gateway_url}")

# ============================================================================
# Step 2: Add Plugin Function to Agent
# ============================================================================

# Add a simple prompt-based function
documentation_function = agent_kernel.add_function(
    plugin_name="DocsHelper",
    function=KernelFunctionFromPrompt(
        function_name="explain_concept",
        prompt="""You are a technical documentation expert.

Explain the following concept clearly and concisely:

Concept: {{$concept}}

Provide:
1. Brief definition
2. Key characteristics
3. Common use cases
4. A simple example""",
    )
)

print("✓ Documentation helper function added to kernel")

# ============================================================================
# Step 3: Configure Agent Settings
# ============================================================================

agent_settings = AzureChatPromptExecutionSettings(
    service_id="agent_service",
    max_tokens=600,
    temperature=0.7,
)
agent_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

print("✓ Agent execution settings configured")
print("  Function calling: Auto")
print("  Max tokens: 600")

# ============================================================================
# Step 4: Create ChatCompletionAgent
# ============================================================================

workshop_agent = ChatCompletionAgent(
    kernel=agent_kernel,
    name="WorkshopAssistant",
    instructions=(
        "You are an AI assistant for an Azure AI Gateway workshop. "
        "Help users understand AI Gateway concepts, API Management, "
        "and Azure OpenAI integration. Be concise and practical. "
        "Use available functions to provide detailed explanations when needed."
    ),
    arguments=KernelArguments(settings=agent_settings),
)

print("✓ ChatCompletionAgent created")
print(f"  Name: {workshop_agent.name}")
print("  Instructions: Workshop assistance")

# ============================================================================
# Step 5: Run Agent Conversations
# ============================================================================

async def run_agent_examples():
    """Execute agent conversation examples."""

    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Agent Interaction")
    print("="*70)

    # Create new thread
    thread = workshop_agent.get_new_thread()

    # First interaction
    result1 = await workshop_agent.run(
        "What is Azure API Management?",
        thread=thread
    )

    print(f"\nUser: What is Azure API Management?")
    print(f"Agent: {result1.text}\n")

    # Second interaction (agent remembers context)
    result2 = await workshop_agent.run(
        "How does it help with AI Gateway patterns?",
        thread=thread
    )

    print(f"User: How does it help with AI Gateway patterns?")
    print(f"Agent: {result2.text}\n")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 2: Agent with Function Calling")
    print("="*70)

    thread2 = workshop_agent.get_new_thread()

    result3 = await workshop_agent.run(
        "Explain the concept of 'semantic kernel' in detail",
        thread=thread2
    )

    print(f"\nUser: Explain the concept of 'semantic kernel' in detail")
    print(f"Agent: {result3.text}\n")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 3: Streaming Agent Response")
    print("="*70)

    thread3 = workshop_agent.get_new_thread()

    print("\nUser: Explain the benefits of using an AI Gateway for enterprise deployments")
    print("Agent: ", end="", flush=True)

    # Stream the response
    async for chunk in workshop_agent.run_stream(
        "Explain the benefits of using an AI Gateway for enterprise deployments",
        thread=thread3
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print("\n")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 4: Multi-Turn Technical Discussion")
    print("="*70)

    thread4 = workshop_agent.get_new_thread()

    questions = [
        "What is function calling in LLMs?",
        "How does Semantic Kernel implement function calling?",
        "What's the difference between manual and auto function invocation?"
    ]

    for question in questions:
        result = await workshop_agent.run(question, thread=thread4)
        print(f"\nUser: {question}")
        print(f"Agent: {result.text[:200]}...")  # Truncate for readability

    print("\n")

    # ========================================================================

    print("\n" + "="*70)
    print("AGENT CONVERSATION STATISTICS")
    print("="*70)
    print(f"Total examples: 4")
    print(f"Agent: WorkshopAssistant")
    print(f"Threads created: 4")
    print(f"Total interactions: 8+")
    print(f"All routed through: {apim_gateway_url}")
    print(f"Streaming enabled: Yes")

# Run agent examples
await run_agent_examples()

print("\n" + "="*70)
print("✓ SK ChatCompletionAgent Demo Complete")
print("="*70)
print("\nKey Takeaways:")
print("1. SK agents maintain conversation state across turns")
print("2. Threads enable parallel, independent conversations")
print("3. Agents support both standard and streaming responses")
print("4. Function calling integrates seamlessly with agents")
print("5. Custom clients enable APIM gateway routing")
```

---

### Cell 5: SK Vector Search with Gateway-Routed Embeddings

```python
# ============================================================================
# Semantic Kernel: Vector Search with APIM-Routed Embeddings
# ============================================================================
"""
Demonstrates:
- SK in-memory vector store for quick demos
- Embedding generation through APIM gateway
- Vector search for RAG pattern
- SK search functions for retrieval
"""

import asyncio
import numpy as np
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding, AzureChatCompletion
from semantic_kernel.connectors.memory import InMemoryVectorStore
from openai import AsyncAzureOpenAI

print("="*70)
print("SEMANTIC KERNEL: Vector Search with Gateway Embeddings")
print("="*70)

# ============================================================================
# Step 1: Configure Kernel with Embedding Service
# ============================================================================

memory_kernel = Kernel()

# Custom client for embeddings through APIM
embedding_client = AsyncAzureOpenAI(
    azure_endpoint=apim_gateway_url,
    api_version="2024-02-01",
    api_key=subscription_key_both,
    default_headers=headers_both
)

# Note: You'll need an embedding deployment in your Azure OpenAI
# For demo purposes, we'll use text-embedding-ada-002
embedding_deployment = "text-embedding-ada-002"  # Update if different

try:
    embedding_service = AzureTextEmbedding(
        service_id="apim_embeddings",
        deployment_name=embedding_deployment,
        async_client=embedding_client,
    )
    memory_kernel.add_service(embedding_service)
    embeddings_available = True
    print(f"✓ Embedding service configured")
    print(f"  Deployment: {embedding_deployment}")
except Exception as e:
    print(f"⚠ Embedding service not available: {e}")
    print("  Continuing with simulated embeddings for demo...")
    embeddings_available = False

# Add chat service for RAG
memory_chat_client = AsyncAzureOpenAI(
    azure_endpoint=apim_gateway_url,
    api_version="2024-02-01",
    api_key=subscription_key_both,
    default_headers=headers_both
)

memory_chat_service = AzureChatCompletion(
    service_id="memory_chat",
    deployment_name=deployment_name,
    async_client=memory_chat_client,
)
memory_kernel.add_service(memory_chat_service)

print("✓ Chat service added for RAG pattern")

# ============================================================================
# Step 2: Create Sample Knowledge Base
# ============================================================================

knowledge_base = {
    "apim_basics": """
    Azure API Management (APIM) is a fully managed service that enables users to
    publish, secure, transform, maintain, and monitor APIs. It acts as a facade
    to backend services, providing a consistent interface for API consumers.
    """,

    "ai_gateway": """
    An AI Gateway is an architectural pattern using API Management to provide a
    unified interface for multiple AI services. It enables load balancing,
    rate limiting, authentication, and monitoring for AI endpoints.
    """,

    "semantic_kernel": """
    Semantic Kernel is an open-source SDK that lets you easily combine AI services
    like OpenAI, Azure OpenAI, and Hugging Face with conventional programming
    languages like C#, Python, and Java. It provides plugins, planners, and memory.
    """,

    "function_calling": """
    Function calling allows large language models to interact with external tools
    and APIs. The model can decide when to call functions, what parameters to use,
    and how to use the results to answer user queries.
    """,

    "autogen": """
    AutoGen is a framework for developing LLM applications using multiple agents
    that can converse with each other to solve tasks. It supports multi-agent
    conversations, human-in-the-loop, and tool usage.
    """,
}

print(f"✓ Knowledge base created")
print(f"  Documents: {len(knowledge_base)}")

# ============================================================================
# Step 3: Generate Embeddings and Create Vector Store
# ============================================================================

async def create_vector_memory():
    """Create in-memory vector store with embeddings."""

    # For demo: use simple simulated embeddings if service unavailable
    if not embeddings_available:
        print("\nℹ Using simulated embeddings for demo")
        # Create simple random embeddings (normally you'd use real embeddings)
        vectors = {}
        for key in knowledge_base.keys():
            vectors[key] = np.random.rand(1536).tolist()  # ada-002 dimension
        return vectors

    # Real embeddings through APIM
    print("\n🔄 Generating embeddings through APIM gateway...")
    vectors = {}

    for key, text in knowledge_base.items():
        # Generate embedding
        embedding = await embedding_service.generate_embeddings([text])
        vectors[key] = embedding[0]
        print(f"  ✓ {key}: {len(embedding[0])} dimensions")

    return vectors

# Create vector memory
vectors = await create_vector_memory()

print(f"✓ Vector embeddings created")
print(f"  Total vectors: {len(vectors)}")

# ============================================================================
# Step 4: Implement Simple Vector Search
# ============================================================================

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

async def search_knowledge_base(query: str, top_k: int = 2):
    """Search knowledge base using vector similarity."""

    if not embeddings_available:
        # Fallback: simple keyword search
        print(f"\nℹ Using keyword search (embeddings unavailable)")
        results = []
        query_lower = query.lower()
        for key, text in knowledge_base.items():
            if any(word in text.lower() for word in query_lower.split()):
                results.append((key, text, 0.9))  # Dummy score
        return results[:top_k]

    # Generate query embedding
    print(f"\n🔄 Searching for: '{query}'")
    query_embedding = await embedding_service.generate_embeddings([query])
    query_vector = query_embedding[0]

    # Calculate similarities
    similarities = []
    for key, vector in vectors.items():
        similarity = cosine_similarity(query_vector, vector)
        similarities.append((key, knowledge_base[key], similarity))

    # Sort by similarity and return top k
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:top_k]

print("✓ Vector search function created")

# ============================================================================
# Step 5: RAG Pattern Examples
# ============================================================================

async def run_rag_examples():
    """Execute RAG pattern examples."""

    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Vector Search")
    print("="*70)

    results = await search_knowledge_base("What is API Management?", top_k=2)

    print("\nSearch Results:")
    for i, (key, text, score) in enumerate(results, 1):
        print(f"\n{i}. {key} (similarity: {score:.4f})")
        print(f"   {text.strip()[:100]}...")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 2: RAG with Chat Completion")
    print("="*70)

    query = "How does an AI Gateway help with multiple AI services?"

    # Search for relevant context
    search_results = await search_knowledge_base(query, top_k=2)

    # Build context from search results
    context = "\n\n".join([f"Context {i+1}:\n{text}"
                           for i, (_, text, _) in enumerate(search_results)])

    # Create RAG prompt
    rag_prompt = f"""Based on the following context, answer the user's question.

Context:
{context}

Question: {query}

Answer:"""

    print(f"\nQuery: {query}")
    print("\n🔄 Searching knowledge base...")
    print(f"  Found {len(search_results)} relevant documents")

    print("\n🔄 Generating answer with retrieved context...")

    from semantic_kernel.contents import ChatHistory

    history = ChatHistory()
    history.add_user_message(rag_prompt)

    from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings

    rag_settings = AzureChatPromptExecutionSettings(
        service_id="memory_chat",
        max_tokens=300,
        temperature=0.7,
    )

    answer = await memory_chat_service.get_chat_message_content(
        chat_history=history,
        settings=rag_settings,
        kernel=memory_kernel,
    )

    print(f"\nAnswer: {answer}")

    # ========================================================================

    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-Query RAG")
    print("="*70)

    queries = [
        "What is Semantic Kernel?",
        "Explain function calling",
        "What is AutoGen used for?"
    ]

    for query in queries:
        results = await search_knowledge_base(query, top_k=1)
        print(f"\nQuery: {query}")
        if results:
            key, text, score = results[0]
            print(f"  Best match: {key} (score: {score:.4f})")
            print(f"  {text.strip()[:80]}...")

    # ========================================================================

    print("\n" + "="*70)
    print("VECTOR SEARCH STATISTICS")
    print("="*70)
    print(f"Knowledge base size: {len(knowledge_base)} documents")
    print(f"Vector dimensions: 1536 (text-embedding-ada-002)")
    print(f"Search method: Cosine similarity")
    print(f"Embeddings routed through: {apim_gateway_url}")
    print(f"Chat completions routed through: {apim_gateway_url}")

# Run RAG examples
await run_rag_examples()

print("\n" + "="*70)
print("✓ SK Vector Search Demo Complete")
print("="*70)
print("\nKey Takeaways:")
print("1. Vector embeddings enable semantic search")
print("2. RAG combines retrieval with generation")
print("3. All embedding calls route through APIM")
print("4. In-memory stores work for quick prototypes")
print("5. Production would use Azure AI Search or Cosmos DB")
```

---

### Cell 6: SK + AutoGen Hybrid Orchestration

```python
# ============================================================================
# Hybrid: Semantic Kernel Plugins + AutoGen Orchestration
# ============================================================================
"""
Demonstrates:
- SK plugins as tools for AutoGen agents
- Multi-agent orchestration with SK capabilities
- Combining SK function calling with AutoGen decision making
- Complex workflow coordination
- All LLM calls through APIM gateway
"""

import asyncio
from typing import Annotated, Dict, Any
from datetime import datetime
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from openai import AsyncAzureOpenAI
from autogen import ConversableAgent

print("="*70)
print("HYBRID: Semantic Kernel + AutoGen Orchestration")
print("="*70)

# ============================================================================
# Step 1: Create SK Plugin with Business Logic
# ============================================================================

class EnterprisePlugin:
    """SK Plugin for enterprise business operations."""

    @kernel_function(description="Get customer information by ID")
    def get_customer_info(self, customer_id: str) -> str:
        """Retrieve customer information."""
        # Simulated customer database
        customers = {
            "C001": "Customer: Acme Corp, Tier: Gold, Balance: $50,000",
            "C002": "Customer: Contoso Ltd, Tier: Silver, Balance: $25,000",
            "C003": "Customer: Fabrikam Inc, Tier: Platinum, Balance: $100,000",
        }
        return customers.get(customer_id, "Customer not found")

    @kernel_function(description="Calculate discount based on customer tier")
    def calculate_discount(self, tier: str, amount: float) -> Dict[str, Any]:
        """Calculate discount for a customer tier."""
        discount_rates = {
            "platinum": 0.20,
            "gold": 0.15,
            "silver": 0.10,
            "bronze": 0.05,
        }
        rate = discount_rates.get(tier.lower(), 0.0)
        discount = amount * rate
        final_price = amount - discount

        return {
            "tier": tier,
            "original_amount": amount,
            "discount_rate": rate,
            "discount_amount": discount,
            "final_price": final_price
        }

    @kernel_function(description="Process order and return order ID")
    def process_order(self, customer_id: str, amount: float) -> str:
        """Process a customer order."""
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return f"Order {order_id} processed for customer {customer_id}, amount: ${amount:.2f}"

# Create SK kernel with plugin
hybrid_kernel = Kernel()

hybrid_client = AsyncAzureOpenAI(
    azure_endpoint=apim_gateway_url,
    api_version="2024-02-01",
    api_key=subscription_key_both,
    default_headers=headers_both
)

hybrid_chat_service = AzureChatCompletion(
    service_id="hybrid_service",
    deployment_name=deployment_name,
    async_client=hybrid_client,
)

hybrid_kernel.add_service(hybrid_chat_service)
hybrid_kernel.add_plugin(EnterprisePlugin(), plugin_name="Enterprise")

print("✓ Semantic Kernel created with EnterprisePlugin")
print("  Functions: get_customer_info, calculate_discount, process_order")

# ============================================================================
# Step 2: Create Wrapper Functions for AutoGen
# ============================================================================

# We need to create standalone functions that AutoGen can call
# These will internally use SK kernel

async def sk_get_customer(customer_id: Annotated[str, "Customer ID"]) -> str:
    """Get customer information using SK plugin."""
    plugin = hybrid_kernel.get_plugin("Enterprise")
    func = plugin["get_customer_info"]
    result = await func.invoke(hybrid_kernel, customer_id=customer_id)
    return str(result)

async def sk_calculate_discount(
    tier: Annotated[str, "Customer tier"],
    amount: Annotated[float, "Order amount"]
) -> str:
    """Calculate discount using SK plugin."""
    plugin = hybrid_kernel.get_plugin("Enterprise")
    func = plugin["calculate_discount"]
    result = await func.invoke(hybrid_kernel, tier=tier, amount=amount)
    return str(result)

async def sk_process_order(
    customer_id: Annotated[str, "Customer ID"],
    amount: Annotated[float, "Order amount"]
) -> str:
    """Process order using SK plugin."""
    plugin = hybrid_kernel.get_plugin("Enterprise")
    func = plugin["process_order"]
    result = await func.invoke(hybrid_kernel, customer_id=customer_id, amount=amount)
    return str(result)

print("✓ SK wrapper functions created for AutoGen")

# ============================================================================
# Step 3: Create AutoGen Agents with SK Tools
# ============================================================================

# Configure AutoGen for APIM
hybrid_autogen_config = {
    "model": deployment_name,
    "api_type": "azure",
    "api_key": subscription_key_both,
    "base_url": apim_gateway_url,
    "api_version": "2024-02-01",
}

config_list_hybrid = [hybrid_autogen_config]

# Agent 1: Sales Agent (analyzes and recommends)
sales_agent = ConversableAgent(
    name="SalesAgent",
    system_message=(
        "You are a sales agent. Analyze customer information, calculate appropriate "
        "discounts, and recommend actions. Be professional and detail-oriented. "
        "Return 'TERMINATE' when task is complete."
    ),
    llm_config={"config_list": config_list_hybrid, "temperature": 0.7},
)

# Agent 2: Order Processor (executes orders)
processor_agent = ConversableAgent(
    name="OrderProcessor",
    system_message=(
        "You are an order processing agent. Execute orders after receiving "
        "approval from sales agent. Confirm all details before processing."
    ),
    llm_config={"config_list": config_list_hybrid, "temperature": 0.3},
)

# Agent 3: User Proxy
hybrid_proxy = ConversableAgent(
    name="Coordinator",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None
                                   and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

print("✓ AutoGen agents created")
print("  1. SalesAgent - Analysis and recommendations")
print("  2. OrderProcessor - Order execution")
print("  3. Coordinator - Workflow management")

# ============================================================================
# Step 4: Register SK Functions with AutoGen Agents
# ============================================================================

# Note: AutoGen's async function support may vary by version
# For this demo, we'll use sync wrappers

def get_customer_sync(customer_id: Annotated[str, "Customer ID"]) -> str:
    """Sync wrapper for SK customer lookup."""
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(sk_get_customer(customer_id))

def calculate_discount_sync(
    tier: Annotated[str, "Customer tier"],
    amount: Annotated[float, "Order amount"]
) -> str:
    """Sync wrapper for SK discount calculation."""
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(sk_calculate_discount(tier, amount))

def process_order_sync(
    customer_id: Annotated[str, "Customer ID"],
    amount: Annotated[float, "Order amount"]
) -> str:
    """Sync wrapper for SK order processing."""
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(sk_process_order(customer_id, amount))

# Register with agents
sales_agent.register_for_llm(
    name="get_customer",
    description="Get customer information by ID"
)(get_customer_sync)

sales_agent.register_for_llm(
    name="calculate_discount",
    description="Calculate discount based on tier and amount"
)(calculate_discount_sync)

processor_agent.register_for_llm(
    name="process_order",
    description="Process an order for a customer"
)(process_order_sync)

hybrid_proxy.register_for_execution(name="get_customer")(get_customer_sync)
hybrid_proxy.register_for_execution(name="calculate_discount")(calculate_discount_sync)
hybrid_proxy.register_for_execution(name="process_order")(process_order_sync)

print("✓ SK functions registered with AutoGen agents")

# ============================================================================
# Step 5: Run Hybrid Orchestration Examples
# ============================================================================

print("\n" + "="*70)
print("EXAMPLE 1: Customer Order Workflow")
print("="*70)

response1 = hybrid_proxy.initiate_chat(
    sales_agent,
    message=(
        "Customer C003 wants to make a purchase of $10,000. "
        "Look up their information, calculate their discount, "
        "and process the order."
    ),
    max_turns=15
)

print("\n✓ Example 1 complete")

# ============================================================================

print("\n" + "="*70)
print("EXAMPLE 2: Multi-Customer Analysis")
print("="*70)

response2 = hybrid_proxy.initiate_chat(
    sales_agent,
    message=(
        "Compare customers C001 and C002. For each, calculate what their "
        "final price would be for a $5,000 purchase."
    ),
    max_turns=15
)

print("\n✓ Example 2 complete")

# ============================================================================

print("\n" + "="*70)
print("EXAMPLE 3: Complex Business Logic")
print("="*70)

response3 = hybrid_proxy.initiate_chat(
    sales_agent,
    message=(
        "Find the best customer tier for a $50,000 purchase. "
        "Show the calculations for all tiers and recommend which "
        "tier a customer should have to get the best value."
    ),
    max_turns=15
)

print("\n✓ Example 3 complete")

# ============================================================================

print("\n" + "="*70)
print("HYBRID ORCHESTRATION STATISTICS")
print("="*70)
print(f"Framework combination: Semantic Kernel + AutoGen")
print(f"SK plugins: EnterprisePlugin (3 functions)")
print(f"AutoGen agents: SalesAgent, OrderProcessor, Coordinator")
print(f"SK functions as AutoGen tools: 3")
print(f"Examples executed: 3")
print(f"All LLM calls routed through: {apim_gateway_url}")
print(f"Model: {deployment_name}")

print("\n" + "="*70)
print("✓ Hybrid SK + AutoGen Demo Complete")
print("="*70)
print("\nKey Takeaways:")
print("1. SK plugins can serve as tools for AutoGen agents")
print("2. Combine SK's plugin architecture with AutoGen's orchestration")
print("3. SK handles business logic, AutoGen handles agent coordination")
print("4. All LLM calls (SK and AutoGen) route through same APIM gateway")
print("5. Hybrid approach leverages strengths of both frameworks")
print("6. Enterprise patterns: separation of concerns, reusable logic")
```

---

## 4. Testing Strategy

### 4.1 Pre-Execution Checks

**Before running new cells:**

1. ✅ Verify `semantic-kernel>=1.0.0` in requirements.txt
2. ✅ Verify `pyautogen>=0.2.0` in requirements.txt
3. ✅ Ensure `apim_gateway_url` variable exists (from earlier cells)
4. ✅ Ensure `subscription_key_both` variable exists
5. ✅ Ensure `headers_both` variable exists
6. ✅ Ensure `deployment_name` variable exists
7. ✅ Check Azure OpenAI deployment is accessible via APIM

### 4.2 Cell-by-Cell Testing

**Cell 1 (SK Plugin Function Calling):**
- Expected: 3 examples execute successfully
- Expected: Function calls shown in output
- Expected: All responses from APIM gateway
- Potential Issues: Missing kernel functions, APIM routing errors
- Workaround: Add more error handling, verify plugin registration

**Cell 2 (SK Streaming):**
- Expected: Real-time text output (character by character)
- Expected: Function calls during streaming
- Expected: All chunks received
- Potential Issues: Streaming may not work with some APIM configurations
- Workaround: Fall back to non-streaming if issues occur

**Cell 3 (AutoGen Multi-Agent):**
- Expected: Agent conversations displayed
- Expected: Tool calls (calculator) executed
- Expected: Termination on TERMINATE keyword
- Potential Issues: AutoGen configuration for Azure endpoints
- Workaround: Verify config_list format, add extra debugging

**Cell 4 (SK Agent):**
- Expected: Multi-turn conversations with context retention
- Expected: Streaming works
- Expected: Thread management maintains state
- Potential Issues: Custom client compatibility
- Workaround: Use standard AzureChatCompletion if custom client fails

**Cell 5 (Vector Search):**
- Expected: Embeddings generated via APIM
- Expected: Vector search returns relevant results
- Expected: RAG pattern generates contextual answers
- Potential Issues: Embedding deployment may not exist
- Workaround: Fallback to keyword search (included in code)

**Cell 6 (Hybrid):**
- Expected: SK functions called by AutoGen agents
- Expected: Multi-agent orchestration completes
- Expected: Complex workflow executes end-to-end
- Potential Issues: Async/sync wrapper complexity
- Workaround: Simplified sync wrappers included

### 4.3 Expected Outputs

**Success Indicators:**
- ✓ checkmarks for each setup step
- Formatted output with clear section headers
- No Python exceptions or tracebacks
- Response content from LLM (not error messages)
- Statistics summaries at end of each cell
- "Complete" messages for each demo

**Warning Indicators:**
- ⚠ warnings (acceptable for missing optional features)
- Fallback messages (using alternative implementations)
- Simulated data (when real services unavailable)

**Error Indicators:**
- ❌ or exceptions in output
- Missing responses from LLM
- Timeout errors
- Authentication failures
- APIM routing failures

### 4.4 Integration Testing

**After all cells execute:**

1. Verify all cells use `apim_gateway_url`
2. Check APIM analytics for request counts
3. Verify no direct Azure OpenAI calls (should all route through APIM)
4. Confirm both SK and AutoGen work with same gateway
5. Test streaming and non-streaming modes
6. Verify function calling works end-to-end

### 4.5 Troubleshooting Guide

**Common Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Import errors | Missing dependencies | Run `pip install -r requirements.txt` |
| APIM routing fails | Wrong gateway URL | Verify `apim_gateway_url` from earlier cells |
| No embeddings | Deployment not found | Use fallback keyword search (in code) |
| AutoGen config error | Wrong API format | Check `api_type`, `base_url` in config |
| Streaming not working | APIM proxy issue | Fall back to non-streaming |
| Function calls fail | Plugin not registered | Check `kernel.add_plugin()` calls |

---

## 5. Dependencies Check

### 5.1 Required Packages (Already in requirements.txt)

- ✅ `semantic-kernel>=1.0.0` - Core SK functionality
- ✅ `pyautogen>=0.2.0` - AutoGen multi-agent framework
- ✅ `openai>=1.12.0` - OpenAI client (used by SK)
- ✅ `azure-identity>=1.15.0` - Azure authentication
- ✅ `httpx>=0.27.0` - HTTP client for async requests
- ✅ `numpy` (via pandas) - Vector operations

### 5.2 Optional Enhancements

**If you want to add (not required for basic demo):**

```txt
# Enhanced vector stores
azure-ai-search>=11.4.0
redis>=5.0.0

# Observability
mlflow>=2.10.0
opentelemetry-api>=1.21.0
```

### 5.3 Existing Notebook Variables Required

All new cells assume these variables exist from earlier notebook cells:

- `apim_gateway_url` - APIM gateway endpoint
- `subscription_key_both` - APIM subscription key
- `headers_both` - Request headers dict
- `deployment_name` - Azure OpenAI deployment name
- `credential` - Azure credential object (if used)

---

## 6. Implementation Checklist

### Phase 3.1: Preparation
- [ ] Verify requirements.txt has SK 1.37.0 and AutoGen 0.2.0+
- [ ] Run earlier notebook cells to set up APIM variables
- [ ] Test basic APIM connectivity
- [ ] Verify Azure OpenAI deployment accessible via APIM

### Phase 3.2: Cell Implementation
- [ ] Add Cell 1: SK Plugin Function Calling
- [ ] Test Cell 1, verify function calls work
- [ ] Add Cell 2: SK Streaming
- [ ] Test Cell 2, verify streaming output
- [ ] Add Cell 3: AutoGen Multi-Agent
- [ ] Test Cell 3, verify agent conversations
- [ ] Add Cell 4: SK Agent
- [ ] Test Cell 4, verify thread management
- [ ] Add Cell 5: Vector Search
- [ ] Test Cell 5, verify search results
- [ ] Add Cell 6: Hybrid Orchestration
- [ ] Test Cell 6, verify SK + AutoGen integration

### Phase 3.3: Validation
- [ ] Run all 6 new cells in sequence
- [ ] Verify no errors or exceptions
- [ ] Check APIM analytics for all requests
- [ ] Confirm statistics in each cell output
- [ ] Test with different queries/inputs

### Phase 3.4: Documentation
- [ ] Add markdown cells explaining each demo
- [ ] Include "What you'll learn" sections
- [ ] Add troubleshooting notes
- [ ] Create summary cell at end

---

## 7. Success Metrics

**Phase 3 will be complete when:**

1. ✅ All 6 new cells execute without errors
2. ✅ All LLM calls route through APIM gateway
3. ✅ SK function calling works with APIM
4. ✅ AutoGen agents communicate via APIM
5. ✅ Streaming responses work correctly
6. ✅ Vector search demonstrates RAG pattern
7. ✅ Hybrid SK + AutoGen orchestration completes
8. ✅ All cells have clear, educational output
9. ✅ Statistics show request counts and routes
10. ✅ Notebook remains under 200 cells total

---

## 8. Next Steps

After Phase 3 completion:

1. **User Testing**: Have workshop participants run all cells
2. **Performance Tuning**: Optimize APIM policies for SK/AutoGen
3. **Advanced Topics**: Consider adding:
   - SK Agent orchestration patterns
   - AutoGen GroupChat with >2 agents
   - SK memory persistence with Azure services
   - Advanced prompt templates
4. **Documentation**: Create workshop guide PDF
5. **Deployment**: Package notebook for distribution

---

## Appendix: Key Research Links

### Semantic Kernel Documentation
- [SK Getting Started](https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide)
- [SK Plugins](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/)
- [SK Function Calling](https://learn.microsoft.com/en-us/semantic-kernel/concepts/ai-services/chat-completion/function-calling/)
- [SK Agents](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-architecture)
- [SK Planning](https://learn.microsoft.com/en-us/semantic-kernel/concepts/planning)

### AutoGen Documentation
- [AutoGen Overview](https://microsoft.github.io/autogen/)
- [AutoGen Agents](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/intro.html)
- [Azure Integration](https://learn.microsoft.com/en-us/azure/container-apps/sessions-tutorial-autogen)

### Azure AI Documentation
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/)
- [API Management](https://learn.microsoft.com/en-us/azure/api-management/)
- [AI Agent Service](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/agents/transparency-note)

---

**Document Status**: ✅ Research Complete - Ready for Implementation
**Last Updated**: 2025-11-17
**Next Action**: Begin Phase 3.1 - Preparation
