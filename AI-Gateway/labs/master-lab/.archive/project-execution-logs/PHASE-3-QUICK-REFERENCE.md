# Phase 3: Quick Reference Guide

**For**: Workshop participants and presenters
**Date**: 2025-11-17
**Notebook**: master-ai-gateway-fix-MCP.ipynb

---

## Phase 3 Cell Overview

### Cell 158: Introduction
**Type**: Markdown
**Content**: Phase 3 overview and prerequisites

---

### Cells 159-160: SK Plugin Function Calling

**What it demonstrates**:
- Creating SK plugins with @kernel_function decorator
- Automatic function calling with FunctionChoiceBehavior.Auto()
- Multi-step planning and execution

**Key code**:
```python
@kernel_function(description="Get the current UTC time")
def get_current_time(self) -> str:
    return datetime.utcnow().isoformat()

execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
```

**Expected output**:
- 3 examples execute successfully
- Function calls are automatic (no manual parsing)
- All responses from APIM gateway
- Statistics summary at end

**Time to execute**: ~30-45 seconds

---

### Cells 161-162: SK Streaming Chat

**What it demonstrates**:
- Real-time streaming responses
- Async iteration over chunks
- Function calling during streaming

**Key code**:
```python
response_stream = stream_chat_service.get_streaming_chat_message_content(
    chat_history=history,
    settings=stream_settings,
    kernel=stream_kernel,
)

async for chunk in response_stream:
    print(chunk.content, end="", flush=True)
```

**Expected output**:
- Text appears character-by-character (or word-by-word)
- 3 examples with progressive output
- Statistics summary

**Time to execute**: ~45-60 seconds

---

### Cells 163-164: AutoGen Multi-Agent

**What it demonstrates**:
- Multiple specialized agents (Analyst, Calculator, UserProxy)
- Agent-to-agent communication
- Tool registration and execution

**Key code**:
```python
analyst_agent = ConversableAgent(
    name="Analyst",
    system_message="You are a data analyst...",
    llm_config={"config_list": config_list}
)

user_proxy.initiate_chat(analyst_agent, message="Calculate...", max_turns=10)
```

**Expected output**:
- Agent conversations displayed
- Tool calls (calculator) executed
- 3 multi-agent examples
- Termination on "TERMINATE"

**Time to execute**: ~60-90 seconds

---

### Cells 165-166: SK Agent with Thread Management

**What it demonstrates**:
- ChatCompletionAgent with custom client
- Thread-based conversation state
- Multi-turn conversations with context retention

**Key code**:
```python
workshop_agent = ChatCompletionAgent(
    kernel=agent_kernel,
    name="WorkshopAssistant",
    instructions="You are an AI assistant..."
)

thread = workshop_agent.get_new_thread()
result = await workshop_agent.run("What is Azure API Management?", thread=thread)
```

**Expected output**:
- 4 examples with different conversation patterns
- Context maintained across turns
- Streaming example shows progressive output
- Statistics summary

**Time to execute**: ~60-90 seconds

---

### Cells 167-168: Vector Search and RAG

**What it demonstrates**:
- Vector embeddings through APIM
- In-memory vector store
- RAG (Retrieval Augmented Generation) pattern

**Key code**:
```python
embedding = await embedding_service.generate_embeddings([text])
vectors[key] = embedding[0]

results = await search_knowledge_base("What is API Management?", top_k=2)
```

**Expected output**:
- Embeddings generated (or fallback to keyword search)
- Vector search returns relevant results
- RAG pattern generates contextual answers
- 3 examples shown

**Time to execute**: ~45-60 seconds

**Note**: May show warning "Embedding service not available" - this is acceptable and will use fallback

---

### Cells 169-170: SK + AutoGen Hybrid

**What it demonstrates**:
- SK plugins as tools for AutoGen agents
- EnterprisePlugin with business logic
- Multi-agent orchestration with SK functions

**Key code**:
```python
class EnterprisePlugin:
    @kernel_function(description="Get customer information by ID")
    def get_customer_info(self, customer_id: str) -> str:
        # Business logic...

sales_agent.register_for_llm(name="get_customer")(get_customer_sync)
```

**Expected output**:
- 3 complex business workflow examples
- SK functions called by AutoGen agents
- Multi-agent collaboration
- Statistics summary

**Time to execute**: ~60-90 seconds

---

## Quick Troubleshooting

| Problem | Cell | Solution |
|---------|------|----------|
| ImportError: semantic-kernel | Any | `pip install semantic-kernel>=1.0.0` |
| ImportError: pyautogen | 164, 170 | `pip install pyautogen>=0.2.0` |
| NameError: apim_gateway_url | Any | Run earlier cells to establish variables |
| Embedding service not available | 168 | Acceptable - will use keyword search fallback |
| Streaming not showing progressively | 162, 166 | Acceptable - may appear all at once |
| Agent conversation too long | 164, 170 | Increase max_turns or modify prompt |

---

## Variable Dependencies

All Phase 3 cells require these variables from earlier cells:

| Variable | Established In | Purpose |
|----------|---------------|---------|
| `apim_gateway_url` | Earlier APIM setup cell | APIM endpoint URL |
| `subscription_key_both` | Earlier APIM setup cell | Subscription key |
| `headers_both` | Earlier APIM setup cell | Custom headers dict |
| `deployment_name` | Earlier Azure OpenAI cell | Model deployment name |

**Before running Phase 3**: Verify these variables exist by running:
```python
print(f"APIM URL: {apim_gateway_url}")
print(f"Deployment: {deployment_name}")
print(f"Headers: {headers_both}")
```

---

## Execution Time Estimates

| Cell Range | Description | Est. Time |
|------------|-------------|-----------|
| 158 | Phase 3 intro (markdown) | N/A |
| 159-160 | SK Plugin Function Calling | 30-45 sec |
| 161-162 | SK Streaming Chat | 45-60 sec |
| 163-164 | AutoGen Multi-Agent | 60-90 sec |
| 165-166 | SK Agent | 60-90 sec |
| 167-168 | Vector Search/RAG | 45-60 sec |
| 169-170 | Hybrid SK+AutoGen | 60-90 sec |
| **Total** | **All Phase 3 cells** | **5-8 minutes** |

---

## Success Indicators

### Visual Indicators in Output
- ✓ Checkmarks for setup steps
- === Section dividers
- "EXAMPLE 1:", "EXAMPLE 2:" headers
- "Complete" messages
- Statistics summaries
- APIM gateway URL displayed

### Content Indicators
- LLM responses are coherent and relevant
- Function calls happen automatically
- Agent conversations flow naturally
- Search results are relevant
- No Python exceptions or tracebacks

### Integration Indicators
- All statistics show same APIM gateway URL
- No direct Azure OpenAI endpoint mentioned
- Request counts increment in APIM analytics
- Both SK and AutoGen use same gateway

---

## Presenter Notes

### Cell 159-160 (SK Plugin)
**Key talking points**:
- SK plugins encapsulate reusable functionality
- @kernel_function makes methods discoverable
- FunctionChoiceBehavior.Auto() enables autonomous planning
- LLM decides which functions to call and when

**Demo tip**: Show how changing the user message affects which functions are called

---

### Cell 161-162 (Streaming)
**Key talking points**:
- Streaming provides better UX for long responses
- Async iteration enables real-time rendering
- Function calling still works during streaming
- Important for user-facing applications

**Demo tip**: Point out the progressive output (character-by-character)

---

### Cell 163-164 (AutoGen)
**Key talking points**:
- Multi-agent patterns enable specialized roles
- Agents communicate to solve complex tasks
- Tool registration separates LLM decision from execution
- Termination conditions prevent infinite loops

**Demo tip**: Show how agents "talk" to each other in output

---

### Cell 165-166 (SK Agent)
**Key talking points**:
- ChatCompletionAgent is SK's agent abstraction
- Threads maintain conversation state
- Context is preserved across multiple turns
- Supports both standard and streaming responses

**Demo tip**: Show how agent remembers previous conversation turns

---

### Cell 167-168 (Vector Search)
**Key talking points**:
- Vector embeddings enable semantic search
- RAG combines retrieval with generation
- In-memory stores work for prototypes
- Production would use Azure AI Search or Cosmos DB

**Demo tip**: Explain similarity scores and how search differs from keyword matching

---

### Cell 169-170 (Hybrid)
**Key talking points**:
- Combine strengths of both frameworks
- SK for business logic, AutoGen for orchestration
- Enterprise patterns: separation of concerns
- Scalable approach for complex applications

**Demo tip**: Highlight how SK plugins become AutoGen tools seamlessly

---

## Common Questions

**Q: Why use both SK and AutoGen?**
A: SK excels at plugin architecture and Azure integration. AutoGen excels at multi-agent orchestration. Combining them leverages both strengths.

**Q: Do all calls really go through APIM?**
A: Yes! Every cell uses `apim_gateway_url` for the Azure OpenAI client. Check APIM analytics to confirm.

**Q: What if embeddings aren't available?**
A: Cell 168 has a fallback to keyword search. The demo continues with simulated data.

**Q: Can I modify the examples?**
A: Absolutely! Try different prompts, add more functions, or create new agents.

**Q: Is this production-ready?**
A: The patterns are production-ready. You'd add more error handling, logging, and monitoring for actual deployment.

---

## Additional Resources

### Documentation
- Semantic Kernel: https://learn.microsoft.com/en-us/semantic-kernel/
- AutoGen: https://microsoft.github.io/autogen/
- Azure API Management: https://learn.microsoft.com/en-us/azure/api-management/

### Code Samples
- SK Samples: https://github.com/microsoft/semantic-kernel/tree/main/python/samples
- AutoGen Samples: https://github.com/microsoft/autogen/tree/main/notebook

### Workshop Materials
- Phase 3 Research: PHASE-3-SK-AUTOGEN-EXTRAS.md
- Detailed Summary: PHASE-3-CELLS-ADDED.md
- Final Summary: PHASE-3-FINAL-SUMMARY.md

---

**Version**: 1.0
**Last Updated**: 2025-11-17
**Maintained By**: Workshop Team
