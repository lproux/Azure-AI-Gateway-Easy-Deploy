#!/bin/bash

echo "========================================================================"
echo "🔍 Checking MCP Server Source Folders"
echo "========================================================================"
echo ""

FOLDERS=(
    "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/gemini-mcp-agents/src/weather"
    "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/gemini-mcp-agents/src/oncall"
    "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/mcp-a2a-agents/src/weather"
    "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/mcp-a2a-agents/src/oncall"
    "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/mcp-a2a-agents/src/spotify"
)

for folder in "${FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        server_name=$(basename "$folder")
        lab_name=$(basename "$(dirname "$(dirname "$folder")")")
        
        echo "📦 ${server_name} (from ${lab_name})"
        echo "   Path: $folder"
        
        # Check for required files
        has_server_py="❌"
        has_dockerfile="❌"
        has_requirements="❌"
        
        [ -f "$folder/server.py" ] && has_server_py="✅"
        [ -f "$folder/Dockerfile" ] && has_dockerfile="✅"
        [ -f "$folder/requirements.txt" ] && has_requirements="✅"
        
        echo "   server.py: $has_server_py"
        echo "   Dockerfile: $has_dockerfile"
        echo "   requirements.txt: $has_requirements"
        
        # List files
        echo "   Files: $(ls "$folder" 2>/dev/null | tr '\n' ', ' | sed 's/,$//')"
        echo ""
    fi
done

echo "========================================================================"
echo "💡 Summary"
echo "========================================================================"
echo "Found source folders for: weather, oncall, spotify"
echo "Still missing: github, product-catalog, place-order, ms-learn"
