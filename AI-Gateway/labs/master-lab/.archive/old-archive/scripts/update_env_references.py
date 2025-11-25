#!/usr/bin/env python3
"""
Update all lab cells to load from master-lab.env
"""

import json

print('[*] Reading notebook...')
with open('master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'[*] Total cells: {len(nb["cells"])}')

# Find cell 7 (Load Environment Variables)
print('[*] Updating cell 7 (Load Environment Variables)...')

# New cell content for loading .env
new_env_load_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "from dotenv import load_dotenv\n",
        "import os\n",
        "\n",
        "# Load environment variables from deployment\n",
        "env_file = 'master-lab.env'\n",
        "if os.path.exists(env_file):\n",
        "    load_dotenv(env_file)\n",
        "    print(f'[OK] Loaded environment from {env_file}')\n",
        "    \n",
        "    # Verify key variables are loaded\n",
        "    apim_url = os.getenv('APIM_GATEWAY_URL')\n",
        "    if apim_url:\n",
        "        print(f'[OK] APIM Gateway URL: {apim_url}')\n",
        "    else:\n",
        "        print('[!] Warning: APIM_GATEWAY_URL not found in .env')\n",
        "else:\n",
        "    print(f'[!] {env_file} not found. Run deployment cells first.')\n",
        "    print('[!] Cells 10-17 will deploy infrastructure and create the .env file')\n"
    ]
}

# Replace cell 7 (which should be the env loading cell based on earlier structure)
# But let me check - cell 7 was "Load Environment Variables from Deployment Output"
# Let me find it by looking for the markdown header

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and cell['source']:
        source_text = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        if 'Load Environment Variables from Deployment Output' in source_text:
            print(f'[*] Found env loading header at cell {i}')
            # Add the code cell after it
            nb['cells'][i+1] = new_env_load_cell
            print(f'[OK] Updated cell {i+1} with new env loading code')
            break

print('[*] Saving notebook...')
with open('master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[OK] Notebook updated!')
print()
print('[OK] Changes:')
print('  - Cell 7: Now loads from master-lab.env')
print('  - All lab cells will use environment variables from master-lab.env')
print()
print('[OK] Next steps:')
print('  1. Open master-ai-gateway.ipynb')
print('  2. Run cells 0-17 to deploy and generate .env')
print('  3. Run any lab cells (18+) to test')
