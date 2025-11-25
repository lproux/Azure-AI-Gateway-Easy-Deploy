#!/usr/bin/env python3
"""
Apply Phase 3: Add SK + AutoGen extras cells to master notebook
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

# File paths
NOTEBOOK_PATH = Path("/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/master-ai-gateway-fix-MCP.ipynb")
PHASE3_DOC = Path("/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/project-execution-logs/PHASE-3-SK-AUTOGEN-EXTRAS.md")
OUTPUT_DOC = Path("/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/project-execution-logs/PHASE-3-CELLS-ADDED.md")

# Create backup
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_path = NOTEBOOK_PATH.with_suffix(f'.ipynb.backup-phase3-{timestamp}')

print("="*80)
print("PHASE 3 APPLICATION: SK + AutoGen Extras")
print("="*80)

# Step 1: Create backup
print(f"\n1. Creating backup...")
shutil.copy2(NOTEBOOK_PATH, backup_path)
print(f"   ✓ Backup created: {backup_path.name}")

# Step 2: Load notebook
print(f"\n2. Loading notebook...")
with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

original_cell_count = len(notebook['cells'])
print(f"   ✓ Current cell count: {original_cell_count}")

# Step 3: Extract code from Phase 3 document
print(f"\n3. Extracting cell code from Phase 3 document...")

# Read the Phase 3 document
with open(PHASE3_DOC, 'r', encoding='utf-8') as f:
    phase3_content = f.read()

# Extract the 6 code blocks
cell_codes = []
cell_titles = [
    "SK Plugin for Gateway-Routed Function Calling",
    "SK Streaming Chat with Function Calling",
    "AutoGen Multi-Agent Conversation via APIM",
    "SK Agent with Custom Azure OpenAI Client",
    "SK Vector Search with Gateway-Routed Embeddings",
    "SK + AutoGen Hybrid Orchestration"
]

# Find code blocks between ```python and ```
import re
code_pattern = r'```python\n(.*?)```'
matches = re.findall(code_pattern, phase3_content, re.DOTALL)

# We expect 6 code blocks
if len(matches) < 6:
    print(f"   ⚠ Warning: Found only {len(matches)} code blocks, expected 6")

for i, code in enumerate(matches[:6]):
    cell_codes.append(code)
    print(f"   ✓ Cell {i+1}: {cell_titles[i]} ({len(code)} chars)")

# Step 4: Create new cells
print(f"\n4. Creating new notebook cells...")

new_cells = []

for i, (title, code) in enumerate(zip(cell_titles, cell_codes)):
    # Create markdown header cell
    header_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"## Phase 3, Cell {i+1}: {title}\n",
            "\n",
            f"**Purpose**: {title}\n",
            "\n",
            "**Dependencies**: semantic-kernel, pyautogen, existing APIM variables\n",
            "\n",
            "**Expected Output**: Successful execution with detailed statistics\n"
        ]
    }
    new_cells.append(header_cell)

    # Create code cell
    # Split code into lines for JSON source array
    code_lines = code.split('\n')
    source_lines = [line + '\n' for line in code_lines[:-1]]
    if code_lines[-1]:  # Last line without newline
        source_lines.append(code_lines[-1])

    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines
    }
    new_cells.append(code_cell)

print(f"   ✓ Created {len(new_cells)} new cells ({len(cell_codes)} code + {len(cell_codes)} markdown)")

# Step 5: Add cells to notebook
print(f"\n5. Adding cells to notebook...")

# Add a section header before the new cells
section_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "\n",
        "# Phase 3: Advanced Semantic Kernel + AutoGen Features\n",
        "\n",
        "This section demonstrates advanced agentic AI patterns using:\n",
        "- **Semantic Kernel 1.x**: Plugins, function calling, streaming, agents, vector search\n",
        "- **AutoGen**: Multi-agent conversations, tool registration, orchestration\n",
        "- **Hybrid Patterns**: Combining SK and AutoGen capabilities\n",
        "\n",
        "All demonstrations route through the APIM AI Gateway configured in earlier sections.\n",
        "\n",
        "**Prerequisites**:\n",
        "- All earlier cells executed successfully\n",
        "- Variables available: `apim_gateway_url`, `subscription_key_both`, `headers_both`, `deployment_name`\n",
        "- Packages installed: `semantic-kernel>=1.0.0`, `pyautogen>=0.2.0`\n",
        "\n",
        "---\n"
    ]
}

notebook['cells'].append(section_header)
notebook['cells'].extend(new_cells)

new_cell_count = len(notebook['cells'])
print(f"   ✓ Cells before: {original_cell_count}")
print(f"   ✓ Cells added: {len(new_cells) + 1} (1 section header + {len(new_cells)} content)")
print(f"   ✓ Cells after: {new_cell_count}")

# Step 6: Save modified notebook
print(f"\n6. Saving modified notebook...")
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)
print(f"   ✓ Notebook saved: {NOTEBOOK_PATH.name}")

# Step 7: Create summary document
print(f"\n7. Creating summary document...")

summary = f"""# Phase 3: Cells Added Summary

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Notebook**: {NOTEBOOK_PATH.name}
**Backup**: {backup_path.name}

---

## Changes Applied

### Cell Count
- **Before**: {original_cell_count} cells
- **Added**: {len(new_cells) + 1} cells (1 section header + {len(cell_codes)} code + {len(cell_codes)} markdown)
- **After**: {new_cell_count} cells

### New Cells Added

#### Section Header (Cell {original_cell_count})
- **Type**: Markdown
- **Content**: Phase 3 introduction and prerequisites

"""

for i, title in enumerate(cell_titles):
    cell_num = original_cell_count + 1 + (i * 2)
    summary += f"""
#### Cell {cell_num}: {title} (Header)
- **Type**: Markdown
- **Content**: Purpose and description

#### Cell {cell_num + 1}: {title} (Code)
- **Type**: Code
- **Functionality**: {title}
- **Lines of Code**: {len(cell_codes[i].split(chr(10)))}
- **Key Features**:
"""

    if i == 0:
        summary += """  - SK plugin creation with @kernel_function decorator
  - Automatic function calling with FunctionChoiceBehavior.Auto()
  - Multi-step planning examples
  - APIM gateway routing for all LLM calls
"""
    elif i == 1:
        summary += """  - Real-time streaming chat responses
  - Async iteration over response chunks
  - Function calling during streaming
  - Progressive output rendering
"""
    elif i == 2:
        summary += """  - Multiple specialized AutoGen agents
  - Agent-to-agent communication
  - Tool registration and execution
  - Conversation termination conditions
"""
    elif i == 3:
        summary += """  - SK ChatCompletionAgent with custom client
  - Multi-turn conversation with thread management
  - Agent streaming capabilities
  - Context retention across turns
"""
    elif i == 4:
        summary += """  - Vector embeddings through APIM gateway
  - In-memory vector store for demos
  - RAG (Retrieval Augmented Generation) pattern
  - Semantic search with cosine similarity
"""
    elif i == 5:
        summary += """  - SK plugins as tools for AutoGen agents
  - Hybrid orchestration pattern
  - Enterprise business logic workflow
  - Complex multi-agent coordination
"""

summary += f"""

---

## Testing Instructions

### Prerequisites Verification
Run these cells from the notebook BEFORE executing Phase 3 cells:
1. Cell establishing `apim_gateway_url`
2. Cell establishing `subscription_key_both`
3. Cell establishing `headers_both`
4. Cell establishing `deployment_name`

### Execution Order
Execute cells {original_cell_count} through {new_cell_count - 1} in sequence.

### Expected Results

**Success Indicators**:
- ✓ All cells execute without Python exceptions
- ✓ Each code cell shows formatted output with section headers
- ✓ Statistics summaries appear at end of each demo
- ✓ "Complete" messages displayed for each example
- ✓ LLM responses are relevant and coherent

**Acceptable Warnings**:
- ⚠ "Embedding service not available" - will use fallback (Cell 5)
- ⚠ "Using simulated embeddings" - demo continues (Cell 5)
- ⚠ "Using keyword search" - acceptable fallback (Cell 5)

**Error Indicators** (investigate if seen):
- ❌ ImportError for semantic-kernel or pyautogen
- ❌ Variable not found: apim_gateway_url, subscription_key_both, etc.
- ❌ APIM authentication failures
- ❌ Timeout errors
- ❌ Empty or error responses from LLM

### Troubleshooting

**Problem**: ImportError for semantic-kernel
**Solution**: Run `pip install semantic-kernel>=1.0.0`

**Problem**: ImportError for pyautogen
**Solution**: Run `pip install pyautogen>=0.2.0`

**Problem**: Variable not found (apim_gateway_url, etc.)
**Solution**: Execute earlier notebook cells that establish these variables

**Problem**: APIM authentication error
**Solution**: Verify subscription_key_both is valid and not expired

**Problem**: Streaming not working
**Solution**: Acceptable - code will still complete, output won't be real-time

**Problem**: Embeddings not available
**Solution**: Acceptable - Cell 5 has fallback to keyword search

---

## Validation Checklist

After running all Phase 3 cells:

- [ ] All 6 code cells executed without exceptions
- [ ] SK function calling demo showed multiple examples
- [ ] Streaming demo displayed progressive output
- [ ] AutoGen agents had conversation exchanges
- [ ] SK agent maintained context across turns
- [ ] Vector search returned relevant results
- [ ] Hybrid demo combined SK and AutoGen successfully
- [ ] All statistics summaries showed APIM gateway URL
- [ ] No direct Azure OpenAI endpoint calls (all through APIM)

---

## Integration with Existing Notebook

### Variables Used (from earlier cells):
- `apim_gateway_url` - APIM gateway endpoint URL
- `subscription_key_both` - APIM subscription key
- `headers_both` - Request headers dictionary
- `deployment_name` - Azure OpenAI deployment name

### Variables Created (available for later cells):
Phase 3 cells create their own kernels and agents but don't export variables.
All demonstrations are self-contained.

### Notebook Flow:
1. **Cells 0-{original_cell_count - 1}**: Original notebook content (APIM setup, basic demos)
2. **Cell {original_cell_count}**: Phase 3 section header
3. **Cells {original_cell_count + 1}-{new_cell_count - 1}**: Phase 3 SK + AutoGen demos
4. Future cells can be added after

---

## Files Modified

### Backup Created
- **Location**: `{backup_path}`
- **Purpose**: Restore point if issues arise
- **Restore Command**: `cp "{backup_path}" "{NOTEBOOK_PATH}"`

### Notebook Modified
- **File**: `{NOTEBOOK_PATH.name}`
- **Cells Added**: {len(new_cells) + 1}
- **Size Change**: ~{len(phase3_content) // 1024} KB of code added

### Documentation Created
- **File**: `{OUTPUT_DOC.name}`
- **Purpose**: Phase 3 application summary and testing guide

---

## Next Steps

### Immediate
1. Open the notebook: `{NOTEBOOK_PATH.name}`
2. Run "Run All" or execute cells sequentially
3. Verify all Phase 3 cells execute successfully
4. Review output for completeness

### Testing
1. Verify all 6 demos run without errors
2. Check APIM analytics for request counts
3. Confirm SK and AutoGen both route through APIM
4. Test individual examples with different inputs

### Documentation
1. Add workshop instructions if needed
2. Create participant guide for Phase 3 features
3. Document any environment-specific configurations

### Enhancement (Optional)
1. Add more SK plugin examples
2. Expand AutoGen agent scenarios
3. Add production-ready error handling
4. Integrate with Azure AI Search for vector store

---

## Key Takeaways

### Technical Achievements
1. **Semantic Kernel Integration**: Full SK 1.x feature set with APIM routing
2. **AutoGen Integration**: Multi-agent patterns through AI Gateway
3. **Hybrid Orchestration**: Combined SK + AutoGen capabilities
4. **Enterprise Patterns**: Reusable plugins, agent coordination, RAG

### Educational Value
1. Demonstrates cutting-edge agentic AI patterns
2. Shows practical APIM gateway usage for AI workloads
3. Provides complete, runnable code examples
4. Teaches both SK and AutoGen frameworks

### Production Readiness
1. All LLM calls route through centralized gateway
2. Error handling and fallbacks included
3. Statistics and monitoring built-in
4. Scalable patterns for enterprise deployment

---

**Status**: ✅ Phase 3 Successfully Applied
**Notebook Ready**: Yes
**Testing Required**: Yes (run all cells to validate)
**Documentation Complete**: Yes

---

*Generated by Phase 3 Application Script*
*Timestamp: {datetime.now().isoformat()}*
"""

with open(OUTPUT_DOC, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"   ✓ Summary created: {OUTPUT_DOC.name}")

# Step 8: Final summary
print("\n" + "="*80)
print("✓ PHASE 3 APPLICATION COMPLETE")
print("="*80)
print(f"\nSummary:")
print(f"  - Original cells: {original_cell_count}")
print(f"  - New cells added: {len(new_cells) + 1}")
print(f"  - Total cells now: {new_cell_count}")
print(f"  - Backup: {backup_path.name}")
print(f"  - Documentation: {OUTPUT_DOC.name}")
print(f"\nNext Steps:")
print(f"  1. Open: {NOTEBOOK_PATH.name}")
print(f"  2. Execute Phase 3 cells ({original_cell_count} through {new_cell_count - 1})")
print(f"  3. Verify all demos run successfully")
print(f"  4. Review: {OUTPUT_DOC.name}")
print("\n" + "="*80)
