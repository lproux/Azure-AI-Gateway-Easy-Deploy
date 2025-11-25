#!/usr/bin/env python3
"""
Replace Cell 86 with the working Lab 08 test from master-ai-gateway-fix-MCP.ipynb
"""
import json
from pathlib import Path

working_notebook = Path('master-ai-gateway-fix-MCP.ipynb')
clean_notebook = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 COPYING WORKING LAB 08 CELL")
print("=" * 80)

# Load both notebooks
with open(working_notebook, 'r', encoding='utf-8') as f:
    working = json.load(f)

with open(clean_notebook, 'r', encoding='utf-8') as f:
    clean = json.load(f)

# Find Lab 08 test cell in working notebook
working_lab08_cell = None
for cell in working['cells']:
    source = ''.join(cell.get('source', []))
    if 'Lab 08: Model Routing test' in source and 'gpt-4.1-nano' in source:
        working_lab08_cell = source
        print("\n✅ Found Lab 08 test cell in working notebook")
        break

if not working_lab08_cell:
    print("\n❌ Could not find Lab 08 test cell in working notebook")
    exit(1)

# Remove the policy application cell (Cell 86, index 85) and use Cell 87 as the test
# Since we added a policy cell, we need to remove it and just use the test
print("\n[*] Removing policy application cell (Cell 86)")
print("[*] Updating Cell 87 with working Lab 08 test")

# Remove Cell 86 (index 85) - the failed policy application cell
del clean['cells'][85]

# Now Cell 86 (was 87) is the test cell - update it with working version
clean['cells'][85]['source'] = working_lab08_cell

print("\n✅ Updated Cell 86 with working Lab 08 test")

# Save backup
backup_path = clean_notebook.with_suffix('.ipynb.backup-working-lab08')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(clean, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {clean_notebook}")
with open(clean_notebook, 'w', encoding='utf-8') as f:
    json.dump(clean, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ LAB 08 UPDATED WITH WORKING VERSION!")
print("=" * 80)
print("\nChanges Made:")
print("  ✅ Removed policy application cell")
print("  ✅ Cell 86: Working Lab 08 test (from master-ai-gateway-fix-MCP.ipynb)")
print("  ✅ Uses error handling for models that might fail")
print("\n💡 How It Works:")
print("  - Tests both gpt-4o-mini and gpt-4.1-nano")
print("  - Backend pool load balances across foundries")
print("  - If gpt-4.1-nano routed to foundry2: Shows error (expected)")
print("  - If routed to foundry1/3: Works successfully")
print("  - Uses retry logic with JWT authentication")
print("\n🎯 Next Steps:")
print("  1. Reload notebook")
print("  2. Run Cell 86 (Lab 08 test)")
print("  3. Expected: gpt-4o-mini works, gpt-4.1-nano may work or error")
print("=" * 80)
