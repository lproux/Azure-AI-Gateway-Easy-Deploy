import os
import json
import glob

# Script to analyze all labs and extract models, resources, and dependencies

labs_path = "C:\\Users\\lproux\\OneDrive - Microsoft\\bkp\\Documents\\GitHub\\MCP-servers-internalMSFT-and-external\\AI-Gateway\\labs"

# Labs to skip
skip_labs = ["_deprecated", "aws-bedrock", "gemini-mcp-agents", "master-lab"]

# Labs to include
included_labs = []

all_models = {}
all_bicep_files = []
all_policy_files = []

# Get all lab folders
for lab_folder in os.listdir(labs_path):
    lab_full_path = os.path.join(labs_path, lab_folder)

    if not os.path.isdir(lab_full_path):
        continue

    if lab_folder in skip_labs:
        print(f"[-] Skipping: {lab_folder}")
        continue

    included_labs.append(lab_folder)
    print(f"[+] Including: {lab_folder}")

    # Find all bicep files
    bicep_files = glob.glob(os.path.join(lab_full_path, "**/*.bicep"), recursive=True)
    all_bicep_files.extend(bicep_files)

    # Find all policy files
    policy_files = glob.glob(os.path.join(lab_full_path, "**/*policy*.xml"), recursive=True)
    all_policy_files.extend(policy_files)

    # Find notebook files to extract models
    notebook_files = glob.glob(os.path.join(lab_full_path, "*.ipynb"), recursive=False)

    for nb_file in notebook_files:
        if "clean-up" in nb_file:
            continue

        try:
            with open(nb_file, 'r', encoding='utf-8') as f:
                nb_data = json.load(f)

            # Look for models_config in code cells
            for cell in nb_data.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))

                    if 'models_config' in source:
                        # Extract lab name
                        lab_name = os.path.basename(os.path.dirname(nb_file))
                        if lab_name not in all_models:
                            all_models[lab_name] = []

                        print(f"   [*] Found models_config in {os.path.basename(nb_file)}")

        except Exception as e:
            print(f"   [!] Error reading {nb_file}: {e}")

print(f"\n[SUMMARY]")
print(f"   Total labs to include: {len(included_labs)}")
print(f"   Total bicep files: {len(all_bicep_files)}")
print(f"   Total policy files: {len(all_policy_files)}")
print(f"\n[LABS TO INCLUDE]")
for lab in sorted(included_labs):
    print(f"   - {lab}")
