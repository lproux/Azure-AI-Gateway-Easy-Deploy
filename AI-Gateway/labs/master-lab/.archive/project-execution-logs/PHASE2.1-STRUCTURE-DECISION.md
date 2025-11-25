# Phase 2.1 - Structure Decision

**Created**: 2025-11-14T22:45:00Z
**Issue**: Lab numbering conflict discovered
**Resolution**: Use descriptive section names instead of numbered labs

---

## Discovery

Master notebook structure analysis reveals:
- **## Lab 10**: AI Foundry DeepSeek (cell 77) - MAJOR SECTION
- **### Lab 11-16**: MCP-specific examples (cells 84-96) - SUBSECTIONS
  - ### Lab 11: spotify
  - ### Lab 12: Weather + AI Analysis
  - ### Lab 13: OnCall Schedule via MCP
  - ### Lab 14: GitHub Repository Access
  - ### Lab 15: GitHub + AI Code Analysis
  - ### Lab 16: Spotify Music Search

**Implication**: Cannot add "## Lab 11" and "## Lab 12" without creating numbering conflicts with existing "### Lab 11-16" subsections.

---

## Resolution

**Decision**: Use descriptive section names WITHOUT numbering to avoid conflicts.

### New Section Names (Revised)

**Instead of**:
- ❌ ## Lab 11: AutoGen Framework with Azure OpenAI + MCP
- ❌ ## Lab 12: Semantic Kernel with Timeout Handling

**Use**:
- ✅ ## AutoGen Framework with Azure OpenAI + MCP
- ✅ ## Semantic Kernel with Azure OpenAI + MCP (Timeout Handling)

### Insertion Point

Insert after existing MCP subsections (after cell ~96), creating a clear new section:

```
## Lab 10: AI Foundry DeepSeek
  [content]

### Lab 11-16: MCP Examples
  [existing MCP subsections]

## AutoGen Framework with Azure OpenAI + MCP  <-- NEW
  [AutoGen content]

## Semantic Kernel with Azure OpenAI + MCP (Timeout Handling)  <-- NEW
  [Semantic Kernel content]

[Rest of notebook continues...]
```

---

## Benefits of This Approach

1. ✅ **No Numbering Conflicts**: Avoids confusion with existing ### Lab 11-16
2. ✅ **Clear Organization**: Descriptive names better explain content
3. ✅ **Flexible**: Can add more framework sections later without renumbering
4. ✅ **Consistent**: Matches existing pattern (Lab 10 is only numbered major lab)
5. ✅ **Future-Proof**: Won't break if more MCP labs are added as subsections

---

## Updated TOC Structure

```markdown
# Master AI Gateway Lab

## Table of Contents

### Core Labs
- Lab 01: Zero to Production
- Lab 02: Backend Pool Load Balancing
- Lab 03: Token Rate Limiting
- Lab 04: Token Metrics Emitting
- Lab 05: API Gateway Policy Foundations
- Lab 06: Access Controlling
- Lab 07-09: [Other labs]
- Lab 10: AI Foundry DeepSeek

### MCP Integration Examples
- Lab 11: Spotify (MCP)
- Lab 12: Weather + AI Analysis (MCP)
- Lab 13: OnCall Schedule (MCP)
- Lab 14: GitHub Repository Access (MCP)
- Lab 15: GitHub + AI Code Analysis (MCP)
- Lab 16: Spotify Music Search (MCP)

### Advanced Framework Integration  <-- NEW SECTION
- AutoGen Framework with Azure OpenAI + MCP
- Semantic Kernel with Azure OpenAI + MCP (Timeout Handling)
```

---

## Implementation Plan (Updated)

### Section 1: AutoGen Framework (~12 cells)
**Header**: `## AutoGen Framework with Azure OpenAI + MCP`
**Insert After**: Cell ~96 (after existing MCP labs)
**Content**:
- Introduction to AutoGen
- Azure OpenAI client setup
- MCP tool integration
- Agent creation and execution
- Examples with weather/oncall MCP servers

### Section 2: Semantic Kernel (~10 cells)
**Header**: `## Semantic Kernel with Azure OpenAI + MCP (Timeout Handling)`
**Insert After**: AutoGen section
**Content**:
- Introduction to Semantic Kernel
- Timeout warning and handling
- Azure OpenAI kernel setup
- MCP plugin creation
- Diagnostic troubleshooting cell

### Enhancements (unchanged)
- Lab 02: Backend pool visualizations
- Lab 04: Token metrics charts

---

## Next Steps

1. Insert AutoGen section after cell ~96
2. Insert Semantic Kernel section after AutoGen
3. Add enhancements to Labs 02 & 04
4. Update TOC with new "Advanced Framework Integration" section

---

**Status**: Structure decision made
**Change**: Use descriptive names instead of numbered labs
**Reason**: Avoid conflict with existing ### Lab 11-16 subsections
**Impact**: Clearer organization, no numbering confusion

---

**Created**: 2025-11-14T22:45:00Z
**For**: Phase 2.1 - Structure Decision Documentation
