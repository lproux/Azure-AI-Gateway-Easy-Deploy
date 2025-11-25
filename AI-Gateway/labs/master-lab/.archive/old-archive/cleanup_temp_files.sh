#!/bin/bash
# Cleanup temporary files created during troubleshooting

echo "=========================================="
echo "Cleaning up temporary files..."
echo "=========================================="
echo ""

# Files to KEEP
KEEP_FILES=(
    "requirements.txt"
    "requirements-py312.txt"
    "master-ai-gateway-fix-MCP-clean.ipynb"
    "master-ai-gateway-fix-MCP.ipynb"
    "master-lab.env"
    "bootstrap.env.template"
    "notebook_mcp_helpers.py"
    "README.md"
)

# Create archive directory for documentation
ARCHIVE_DIR="archive_$(date +%Y%m%d)"
mkdir -p "$ARCHIVE_DIR"

echo "Archiving documentation files to: $ARCHIVE_DIR"
echo ""

# Move all .md files except README.md
for file in *.md; do
    if [[ "$file" != "README.md" ]]; then
        echo "  Archiving: $file"
        mv "$file" "$ARCHIVE_DIR/"
    fi
done

# Move all .py helper scripts (keep notebook_mcp_helpers.py)
for file in *.py; do
    if [[ "$file" != "notebook_mcp_helpers.py" ]]; then
        echo "  Archiving: $file"
        mv "$file" "$ARCHIVE_DIR/"
    fi
done

# Move all .sh scripts
for file in *.sh; do
    if [[ "$file" != "cleanup_temp_files.sh" ]]; then
        echo "  Archiving: $file"
        mv "$file" "$ARCHIVE_DIR/"
    fi
done

# Move XML files
for file in *.xml; do
    echo "  Archiving: $file"
    mv "$file" "$ARCHIVE_DIR/"
done

# Move log files
for file in *.log *.txt; do
    if [[ "$file" != "requirements.txt" ]] && [[ "$file" != "requirements-py312.txt" ]]; then
        echo "  Archiving: $file"
        mv "$file" "$ARCHIVE_DIR/" 2>/dev/null
    fi
done

echo ""
echo "=========================================="
echo "✅ Cleanup Complete!"
echo "=========================================="
echo ""
echo "Files kept in current directory:"
ls -1 | grep -E '\.(txt|ipynb|env|py)$'
echo ""
echo "Archived files moved to: $ARCHIVE_DIR"
echo ""
