# Section Renumbering Plan

## Current Structure Analysis

### Issues Found:

1. **Section 0 exists before Section 1**
   - Cell 1: Section 0: Initialize and Deploy (with subsections 0.1-0.8)
   - This should not come before Section 1

2. **Access Control is Lab 1.4, not Section 1**
   - Cell 24: Currently "Lab 1.4: Access Controlling"
   - User wants this as "Section 1"

3. **Duplicate Labs**
   - Cell 53: Lab 01: Zero to Production
   - Cell 56: Lab 1.1: Zero to Production (DUPLICATE)

4. **Misaligned Lab 2.4**
   - Cell 114: Lab 2.4: Built-in LLM Logging
   - Cell 118: Lab 2.4: Built-in LLM Logging (DUPLICATE)
   - Both appear after Section 5, should be in Section 2

5. **Section numbering gaps**
   - Missing some sequential sections

## Proposed New Structure

### Option 1: Access Control as Main Section 1

```
Section 0: Initialize and Deploy (KEEP AS SECTION 0 - Setup/Prerequisites)
  - 0.1 Environment Detection
  - 0.2 Bootstrap Configuration
  - 0.3 Dependencies Installation
  - 0.4 Azure Authentication & Service Principal
  - 0.5 Core Helper Functions
  - 0.6 Deployment Configuration
  - 0.7 Deploy Infrastructure
  - 0.8 Reload Complete Configuration

Section 1: Access Controlling (PROMOTED from Lab 1.4)
  - OAuth 2.0 implementation
  - Token acquisition and validation
  - Azure AD integration

Section 2: Core AI Gateway Features (DEMOTED from Section 1)
  - Lab 2.1: Zero to Production
  - Lab 2.2: Backend Pool Load Balancing
  - Lab 2.3: Token Metrics Emitting
  - Lab 2.4: Content Safety
  - Lab 2.5: Model Routing

Section 3: Advanced Features (RENUMBERED from Section 2)
  - Lab 3.1: Semantic Caching
  - Lab 3.2: Message Storing with Cosmos DB
  - Lab 3.3: Vector Searching with RAG
  - Lab 3.4: Built-in LLM Logging

Section 4: MCP Fundamentals (RENUMBERED from Section 3)
  - 4.1 MCP Server Integration
  - 4.2 Exercise: Sales Analysis via MCP + AI
  - 4.3 Exercise: Azure Cost Analysis via MCP
  - 4.4 Exercise: Function Calling with MCP Tools
  - 4.5 Exercise: Dynamic Column Analysis

Section 5: AI Foundry & Integrations (RENUMBERED from Section 4)
  - Lab 5.1: AI Foundry SDK
  - Lab 5.2: GitHub Repository Access
  - Lab 5.3: GitHub + AI Code Analysis

Section 6: Semantic Kernel & AutoGen (RENUMBERED from Section 5)
  - 6.1 SK Plugin for Gateway-Routed Function Calling
  - 6.2 SK Streaming Chat with Function Calling
  - 6.3 AutoGen Multi-Agent Conversation
  - 6.4 SK Agent with Custom Azure OpenAI Client
  - 6.5 Hybrid SK + AutoGen Orchestration
```

### Option 2: Remove Section 0, Access Control becomes Section 1

```
Section 1: Access Controlling (NEW Section 1)
  - OAuth 2.0 implementation
  - Token acquisition and validation

Section 2: Core AI Gateway Features
  - Labs 2.1-2.5

Section 3: Advanced Features
  - Labs 3.1-3.4

... (etc)
```

## Recommended Approach: Option 1

**Rationale:**
- Keep Section 0 for setup/initialization (common pattern)
- Promotes Access Control to Section 1 (per user request)
- Maintains logical flow: Setup → Security → Features → Advanced → Integrations

## Changes Required

### 1. Cell-by-Cell Changes

| Cell | Current | New | Action |
|------|---------|-----|--------|
| 24 | Lab 1.4: Access Controlling | Section 1: Access Controlling | PROMOTE |
| 35 | Section 1: Core AI Gateway Features | Section 2: Core AI Gateway Features | RENUMBER |
| 36 | Section 2: Advanced Features | Section 3: Advanced Features | RENUMBER |
| 53 | Lab 01: Zero to Production | Lab 2.1: Zero to Production | RENUMBER & FIX |
| 56 | Lab 1.1: Zero to Production | DELETE (duplicate) | DELETE |
| 60 | Lab 1.2: Backend Pool Load Balancing | Lab 2.2: Backend Pool Load Balancing | RENUMBER |
| 70 | Lab 1.3: Token Metrics Emitting | Lab 2.3: Token Metrics Emitting | RENUMBER |
| 73 | Lab 1.5: Content Safety | Lab 2.4: Content Safety | RENUMBER |
| 76 | Lab 1.6: Model Routing | Lab 2.5: Model Routing | RENUMBER |
| 83 | Section 3: MCP Fundamentals | Section 4: MCP Fundamentals | RENUMBER |
| 104 | Section 4: AI Foundry & Integrations | Section 5: AI Foundry & Integrations | RENUMBER |
| 105 | Section 5: Semantic Kernel & AutoGen | Section 6: Semantic Kernel & AutoGen | RENUMBER |
| 114 | Lab 2.4: Built-in LLM Logging | Lab 3.4: Built-in LLM Logging | MOVE to Section 3 |
| 118 | Lab 2.4: Built-in LLM Logging | DELETE (duplicate) | DELETE |

### 2. Table of Contents Update

Replace cell 0 with updated TOC reflecting all changes above.

### 3. Anchor ID Updates

Update all anchor IDs to match new section numbers:
- `#lab1-4` → `#section1`
- `#section1` → `#section2`
- `#section2` → `#section3`
- etc.

## Next Steps

1. ✅ Review this plan with user
2. ⏳ Implement renumbering script
3. ⏳ Update table of contents
4. ⏳ Verify all links work
5. ⏳ Test notebook flow

