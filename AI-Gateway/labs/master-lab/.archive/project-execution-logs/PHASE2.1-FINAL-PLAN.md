# Phase 2.1 - Quick Wins - FINAL PLAN

**Created**: 2025-11-14T22:40:00Z
**Status**: READY TO EXECUTE
**User Selection**: Option B - Skip Lab 11, Add AutoGen + Semantic Kernel

---

## Executive Summary

Phase 2.1 will add framework examples (AutoGen + Semantic Kernel) with Azure OpenAI + MCP integration, plus enhancements to existing labs. Complexity reduced by removing realtime audio lab.

**User Requirements**:
1. ❌ Skip Lab 11 (Realtime Audio) - too complex
2. ✅ Add AutoGen framework with Azure OpenAI + MCP
3. ✅ Add Semantic Kernel examples with timeout handling
4. ✅ Azure-only focus (no AWS Bedrock, no Gemini)

**Critical Note**: Semantic Kernel can hang/stay idle. Add timeout handling (<5 min) and diagnostic cells.

---

## Final Integration Plan

### Lab 11: AutoGen Framework with Azure OpenAI + MCP (~12 cells)

**Source**: gemini-mcp-agents lab (modified for Azure OpenAI)

**Content**:
1. **Introduction** (1 markdown cell)
   - AutoGen overview
   - MCP tool integration benefits
   - Azure OpenAI configuration

2. **AutoGen Setup** (2 code cells)
   - Install autogen-agentchat, autogen-ext packages
   - Import statements and configuration

3. **Azure OpenAI Client** (1 code cell)
   ```python
   from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

   model_client = AzureOpenAIChatCompletionClient(
       azure_endpoint=apim_gateway_url,
       api_key=apim_api_key,
       api_version="2024-08-01-preview",
       model_capabilities={
           "function_calling": True,
           "json_output": True,
           "vision": False
       }
   )
   ```

4. **MCP Server Connection** (2 code cells)
   - SSE client setup with MCP servers
   - Tool extraction from MCP servers
   ```python
   from autogen_ext.tools.mcp import SseMcpToolAdapter, SseServerParams, mcp_server_tools

   server_params = SseServerParams(
       url=f"{apim_resource_gateway_url}/weather/sse",
       headers={"Content-Type": "application/json"},
       timeout=30
   )
   tools = await mcp_server_tools(server_params)
   ```

5. **AutoGen Agent with Tools** (3 code cells)
   - Create AssistantAgent with MCP tools
   - Run agent with task
   - Display conversation via Console UI
   ```python
   from autogen_agentchat.agents import AssistantAgent
   from autogen_agentchat.ui import Console

   agent = AssistantAgent(
       name="weather_agent",
       model_client=model_client,
       reflect_on_tool_use=True,
       tools=tools,
       system_message="You are a helpful assistant with access to MCP tools."
   )

   await Console(agent.run_stream(task="What's the weather in Lisbon?"))
   ```

6. **Test Multiple MCP Servers** (2 code cells)
   - Weather MCP server test
   - Oncall MCP server test

7. **Cleanup** (1 markdown cell)
   - Best practices for agent cleanup

**Total**: ~12 cells (6 code, 6 markdown)

---

### Lab 12: Semantic Kernel with Azure OpenAI + MCP (~10 cells)

**Source**: Existing master-lab Cell 182 (enhanced) + new timeout handling

**Content**:
1. **Introduction** (1 markdown cell)
   - Semantic Kernel overview
   - Timeout warning (can hang for >5 min)
   - Diagnostic approach

2. **Semantic Kernel Setup** (2 code cells)
   - Install semantic-kernel package
   - Import statements and kernel initialization
   ```python
   from semantic_kernel import Kernel
   from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

   kernel = Kernel()
   service_id = "azure_openai"
   kernel.add_service(
       AzureChatCompletion(
           service_id=service_id,
           endpoint=apim_gateway_url,
           api_key=apim_api_key,
           api_version="2024-08-01-preview"
       )
   )
   ```

3. **MCP Plugin Creation** (2 code cells)
   - Connect to MCP server
   - Create Semantic Kernel plugin from MCP tools
   ```python
   from semantic_kernel.functions import kernel_function

   class MCPWeatherPlugin:
       @kernel_function(name="get_weather", description="Get weather for a city")
       async def get_weather(self, city: str) -> str:
           # Call MCP server
           response = await mcp_client.call_tool("get_weather", {"city": city})
           return str(response.content)

   kernel.add_plugin(MCPWeatherPlugin(), "weather")
   ```

4. **Timeout Handling** (2 code cells - CRITICAL)
   - Async timeout wrapper
   - Diagnostic cell for hanging issues
   ```python
   import asyncio
   from asyncio import TimeoutError

   async def run_with_timeout(task, timeout_seconds=300):  # 5 min default
       """Run Semantic Kernel task with timeout to prevent hanging"""
       try:
           result = await asyncio.wait_for(task, timeout=timeout_seconds)
           return result
       except TimeoutError:
           print(f"[ERROR] Semantic Kernel task timed out after {timeout_seconds}s")
           print("[DEBUG] Common causes:")
           print("  1. MCP server not responding")
           print("  2. Azure OpenAI endpoint misconfigured")
           print("  3. API key invalid or expired")
           print("  4. Network connectivity issues")
           raise
   ```

5. **Test with Timeout** (2 code cells)
   - Simple prompt test with 60s timeout
   - Complex MCP tool test with 300s timeout
   ```python
   # Test with timeout
   async def test_semantic_kernel():
       result = await kernel.invoke_prompt(
           "What's the weather in Lisbon?",
           settings={"service_id": service_id}
       )
       return result

   # Run with 60 second timeout
   try:
       result = await run_with_timeout(test_semantic_kernel(), timeout_seconds=60)
       print(f"[OK] Result: {result}")
   except TimeoutError:
       print("[FAIL] Semantic Kernel hung - see diagnostic guidance above")
   ```

6. **Diagnostic Cell** (1 code cell - TROUBLESHOOTING)
   ```python
   # DIAGNOSTIC: Use this cell if Semantic Kernel hangs
   print("=== Semantic Kernel Diagnostic ===")

   # Test 1: Basic Azure OpenAI connectivity (bypass Semantic Kernel)
   from openai import AzureOpenAI
   test_client = AzureOpenAI(
       azure_endpoint=apim_gateway_url,
       api_key=apim_api_key,
       api_version="2024-08-01-preview"
   )
   try:
       response = test_client.chat.completions.create(
           model="gpt-4o-mini",
           messages=[{"role": "user", "content": "Hello"}],
           max_tokens=10
       )
       print("[OK] Direct Azure OpenAI works:", response.choices[0].message.content)
   except Exception as e:
       print("[FAIL] Direct Azure OpenAI failed:", str(e))

   # Test 2: MCP server connectivity
   import httpx
   try:
       response = httpx.get(f"{apim_resource_gateway_url}/weather/sse", timeout=5.0)
       print(f"[OK] MCP server responds: {response.status_code}")
   except Exception as e:
       print("[FAIL] MCP server unreachable:", str(e))

   # Test 3: Check Semantic Kernel version
   import semantic_kernel
   print(f"[INFO] Semantic Kernel version: {semantic_kernel.__version__}")
   ```

**Total**: ~10 cells (6 code, 4 markdown)

---

### Enhancements to Existing Labs (8 cells)

#### Lab 02: Backend Pool Load Balancing (+3 cells)

**Source**: zero-to-production lab

**Content**:
1. **Enhanced Backend Config** (1 code cell)
   - Detailed openai_resources with priority, weight, capacity
   ```python
   # Example: Priority-based failover with weighted distribution
   openai_resources = [
       {"name": "openai1", "location": "eastus", "priority": 1, "weight": 100, "capacity": 4},
       {"name": "openai2", "location": "swedencentral", "priority": 2, "weight": 50, "capacity": 8},
       {"name": "openai3", "location": "westus", "priority": 2, "weight": 50, "capacity": 8}
   ]
   ```

2. **Explanation** (1 markdown cell)
   - Priority failover explanation
   - Weight-based distribution
   - Capacity as TPM limit

3. **Visualization** (1 code cell)
   - Regional distribution chart
   ```python
   import matplotlib.pyplot as plt
   # Bar chart showing request distribution by region
   ```

#### Lab 04: Token Metrics Emitting (+5 cells)

**Source**: zero-to-production lab

**Content**:
1. **Matplotlib Setup** (1 code cell)
   - Import pandas, matplotlib

2. **Regional Distribution Viz** (2 cells: 1 markdown + 1 code)
   - Colored bars by region
   - Average response time line

3. **Token Usage Over Time** (2 cells: 1 markdown + 1 code)
   - Time-series plot
   - Token consumption trends

---

## Final Metrics

### Content Addition
| Item | Cells | Type |
|------|-------|------|
| Lab 11: AutoGen + Azure OpenAI | 12 | New lab |
| Lab 12: Semantic Kernel + Timeout | 10 | New lab |
| Lab 02 Enhancement | 3 | Enhancement |
| Lab 04 Enhancement | 5 | Enhancement |
| **Total** | **30** | **Mixed** |

### Master Notebook Growth
- **Current**: 204 cells
- **After Phase 2.1**: 234 cells
- **Growth**: +30 cells (+15%)

### Package Dependencies
```python
# AutoGen (Lab 11)
autogen-agentchat
autogen-ext
nest-asyncio

# Semantic Kernel (Lab 12)
semantic-kernel

# Visualizations (Lab 04 enhancement)
matplotlib
pandas
```

---

## Implementation Checklist

### Pre-Integration
- [x] User approved Option B
- [x] Timeout handling designed for Semantic Kernel
- [x] Diagnostic cells planned
- [x] Azure-only focus confirmed

### Lab 11: AutoGen (12 cells)
- [ ] Extract AutoGen content from gemini-mcp-agents
- [ ] Replace Gemini client with AzureOpenAIChatCompletionClient
- [ ] Test MCP tool integration with weather/oncall servers
- [ ] Verify agent streaming works
- [ ] Add to master notebook after Lab 10

### Lab 12: Semantic Kernel (10 cells)
- [ ] Enhance existing Semantic Kernel content (Cell 182)
- [ ] Add timeout wrapper (5 min max)
- [ ] Create diagnostic troubleshooting cell
- [ ] Test with 60s timeout for simple prompts
- [ ] Test with 300s timeout for MCP tool calls
- [ ] Add to master notebook after Lab 11

### Enhancements (8 cells)
- [ ] Find Lab 02 section in master
- [ ] Add backend pool config examples (3 cells)
- [ ] Find Lab 04 section in master
- [ ] Add matplotlib visualizations (5 cells)

### Post-Integration
- [ ] Update Table of Contents
- [ ] Add package requirements documentation
- [ ] Test timeout handling works
- [ ] Verify all visualizations render
- [ ] Create Phase 2.1 completion summary

---

## Timeline

| Task | Duration | Complexity |
|------|----------|------------|
| Add Lab 11: AutoGen | 12 min | Medium |
| Add Lab 12: Semantic Kernel + Timeout | 15 min | Medium-High |
| Enhance Labs 02 & 04 | 8 min | Low |
| Update TOC/Docs | 5 min | Low |
| **Total** | **40 min** | |

---

## Risk Mitigation

### Risk 1: Semantic Kernel Hangs
**User Warning**: "Semantic Kernel tends to hang and stay idle for very long"
**Mitigation**:
- ✅ Timeout wrapper (asyncio.wait_for) with 5 min max
- ✅ Diagnostic cell to test Azure OpenAI + MCP independently
- ✅ Clear error messages with troubleshooting steps
- ✅ Shorter timeout (60s) for simple tests

### Risk 2: AutoGen Package Conflicts
**Mitigation**:
- Test imports in isolated cell
- Document version requirements
- Graceful degradation if imports fail

### Risk 3: MCP Server Availability
**Mitigation**:
- Use existing working MCP servers (docs-mcp confirmed working)
- Fallback to direct Azure OpenAI if MCP unavailable
- Clear error messages

---

## Key Decisions

1. **Skip Realtime Audio**: Too complex for current integration
2. **Add Both Frameworks**: AutoGen + Semantic Kernel for comprehensive coverage
3. **Timeout Critical**: 5 min max for Semantic Kernel, shorter for simple tests
4. **Diagnostic First**: Troubleshooting cell to identify hanging root cause
5. **Azure-Only**: No AWS, no Gemini - pure Azure focus

---

## Next Steps

### Immediate
1. Extract AutoGen cells from gemini-mcp-agents
2. Modify for AzureOpenAIChatCompletionClient
3. Add Lab 11 to master notebook

### Following
1. Enhance existing Semantic Kernel content
2. Add timeout wrapper and diagnostic cell
3. Add Lab 12 to master notebook

### Final
1. Add visualizations to Labs 02 & 04
2. Update TOC
3. Test all timeout handling

---

**Status**: FINAL PLAN APPROVED
**User Selection**: Option B (Skip Lab 11 Realtime, Add AutoGen + Semantic Kernel)
**Next Action**: Begin extracting AutoGen content
**Critical Note**: Semantic Kernel timeout handling is MANDATORY

---

**Created**: 2025-11-14T22:40:00Z
**For**: Phase 2.1 - Quick Wins Final Plan (Azure-Only, Framework Focus)
