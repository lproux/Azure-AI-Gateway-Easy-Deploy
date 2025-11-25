import os
import json
import re

labs_path = "C:\\Users\\lproux\\OneDrive - Microsoft\\bkp\\Documents\\GitHub\\MCP-servers-internalMSFT-and-external\\AI-Gateway\\labs"

# MCP-related labs
mcp_labs = [
    "model-context-protocol",
    "mcp-from-api",
    "mcp-client-authorization",
    "mcp-a2a-agents",
    "realtime-mcp-agents",
    "mcp-registry-apic",
    "openai-agents",
    "ai-agent-service"
]

all_mcp_servers = {}

for lab_folder in mcp_labs:
    lab_full_path = os.path.join(labs_path, lab_folder)

    if not os.path.isdir(lab_full_path):
        print(f"[-] Lab folder not found: {lab_folder}")
        continue

    print(f"\n[+] Analyzing: {lab_folder}")
    all_mcp_servers[lab_folder] = {
        'servers': [],
        'images': [],
        'container_apps': []
    }

    # Find notebook files
    for root, dirs, files in os.walk(lab_full_path):
        for file in files:
            if file.endswith('.ipynb') and 'clean-up' not in file:
                nb_path = os.path.join(root, file)

                try:
                    with open(nb_path, 'r', encoding='utf-8') as f:
                        nb_data = json.load(f)

                    for cell in nb_data.get('cells', []):
                        if cell.get('cell_type') == 'code':
                            source = ''.join(cell.get('source', []))

                            # Look for MCP server variables
                            if '_mcp_server_image' in source:
                                matches = re.findall(r'(\w+)_mcp_server_image\s*=\s*["\']([^"\']+)["\']', source)
                                for match in matches:
                                    server_name = match[0]
                                    image_name = match[1]
                                    if server_name not in [s['name'] for s in all_mcp_servers[lab_folder]['servers']]:
                                        all_mcp_servers[lab_folder]['servers'].append({
                                            'name': server_name,
                                            'image': image_name
                                        })
                                        print(f"   [*] Found server: {server_name} -> {image_name}")

                            # Look for container app names
                            if 'containerapp_resource_name' in source or 'ContainerApp' in source:
                                matches = re.findall(r'(\w+)_containerapp_resource_name', source)
                                for match in matches:
                                    if match not in all_mcp_servers[lab_folder]['container_apps']:
                                        all_mcp_servers[lab_folder]['container_apps'].append(match)
                                        print(f"   [*] Found container app: {match}")

                except Exception as e:
                    print(f"   [!] Error reading {file}: {e}")

# Print summary
print(f"\n\n[SUMMARY]")
unique_servers = set()
for lab, data in all_mcp_servers.items():
    for server in data['servers']:
        unique_servers.add(server['name'])

print(f"Total unique MCP servers: {len(unique_servers)}")
print(f"\nUnique MCP servers:")
for server in sorted(unique_servers):
    print(f"   - {server}")

print(f"\n\n[DETAILED BREAKDOWN BY LAB]")
for lab, data in all_mcp_servers.items():
    if data['servers'] or data['container_apps']:
        print(f"\n{lab}:")
        if data['servers']:
            print(f"   Servers: {', '.join([s['name'] for s in data['servers']])}")
        if data['container_apps']:
            print(f"   Container Apps: {', '.join(data['container_apps'])}")
