#!/usr/bin/env python3
"""Refactor remaining cells 63, 67, 67b, 69, 77 to use working MCP helpers"""

import json

# Load notebook
with open('../master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 63: OnCall tool calling
cell_63_content = """# OnCall: Get on-call engineers

from notebook_mcp_helpers import OnCallMCP

oncall_server_url = "http://20.246.202.123:8080"
oncall = OnCallMCP(oncall_server_url)

print("[*] Getting on-call engineers list...")

try:
    oncall_list = oncall.get_oncall_list()

    print('[SUCCESS] On-call list retrieved:')
    print('-' * 40)

    import json
    if isinstance(oncall_list, str):
        import ast
        try:
            result_parsed = ast.literal_eval(oncall_list)
            output = json.dumps(result_parsed, indent=2)
            # Count active on-calls
            active_count = sum(1 for p in result_parsed if p.get('status') == 'on')
            print(f"Active on-call engineers: {active_count}")
        except:
            output = oncall_list
    else:
        output = json.dumps(oncall_list, indent=2)

    if len(output) > 600:
        output = output[:600] + '\\n...\\n(truncated)'
    print(output)

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] OnCall query complete')
"""

# Cell 67: GitHub repository queries
cell_67_content = """# GitHub: Search and explore repositories

from notebook_mcp_helpers import GitHubMCP

github_server_url = "http://4.158.206.99:8080"
github = GitHubMCP(github_server_url)

print("[*] Searching GitHub for AI projects...")

try:
    # Search for AI repositories
    search_results = github.search_repositories("AI language:python")

    print('[SUCCESS] GitHub search results:')
    print('-' * 40)

    import json
    if isinstance(search_results, str):
        import ast
        try:
            result_parsed = ast.literal_eval(search_results)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = search_results
    else:
        output = json.dumps(search_results, indent=2)

    if len(output) > 800:
        output = output[:800] + '\\n...\\n(truncated)'
    print(output)

    # Get specific repository
    print()
    print("[*] Getting specific repository details...")
    repo = github.get_repository("mlops", "python-ml-framework")
    print(f"[SUCCESS] Repository: {repo}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] GitHub queries complete')
"""

# Cell 67b: Weather - partially working (make it fully working)
cell_67b_content = """# Weather: Get weather data for cities

from notebook_mcp_helpers import WeatherMCP

weather_server_url = "http://4.255.12.152:8080"
weather = WeatherMCP(weather_server_url)

print("[*] Getting weather for multiple cities...")

try:
    cities = ["Seattle", "New York", "Chicago", "San Francisco"]

    for city in cities:
        print(f"\\n[*] Weather for {city}...")
        weather_data = weather.get_weather(city)

        import json
        if isinstance(weather_data, str):
            import ast
            try:
                result_parsed = ast.literal_eval(weather_data)
                print(f"  Temperature: {result_parsed.get('temperature', 'N/A')}°C")
                print(f"  Condition: {result_parsed.get('condition', 'N/A')}")
                print(f"  Humidity: {result_parsed.get('humidity', 'N/A')}%")
            except:
                print(f"  {weather_data}")
        else:
            print(f"  {json.dumps(weather_data, indent=2)}")

    print()
    print('[SUCCESS] All weather data retrieved')

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] Weather queries complete')
"""

# Cell 69: GitHub analysis - list issues and commits
cell_69_content = """# GitHub: Repository analysis

from notebook_mcp_helpers import GitHubMCP

github_server_url = "http://4.158.206.99:8080"
github = GitHubMCP(github_server_url)

print("[*] Analyzing GitHub repository...")

try:
    owner = "education"
    repo = "neural-networks-101"

    # Get repository README
    print(f"[*] Getting README for {owner}/{repo}...")
    readme = github.get_repository_readme(owner, repo)
    print('[SUCCESS] README retrieved')

    # List repository issues
    print(f"\\n[*] Listing issues for {owner}/{repo}...")
    issues = github.list_repository_issues(owner, repo, "open")

    import json
    if isinstance(issues, str):
        import ast
        try:
            result_parsed = ast.literal_eval(issues)
            print(f"[SUCCESS] Found {len(result_parsed)} open issues")
            output = json.dumps(result_parsed[:3], indent=2)  # Show first 3
        except:
            output = issues
    else:
        output = json.dumps(issues, indent=2)

    if len(output) > 600:
        output = output[:600] + '\\n...\\n(truncated)'
    print(output)

    # List recent commits
    print(f"\\n[*] Getting recent commits for {owner}/{repo}...")
    commits = github.list_repository_commits(owner, repo, 5)
    print(f"[SUCCESS] Commits: {commits}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] GitHub analysis complete')
"""

# Cell 77: Product catalog queries
cell_77_content = """# Product Catalog: Browse and search products

from notebook_mcp_helpers import ProductCatalogMCP

product_catalog_server_url = "http://145.133.116.26:8080"
product_catalog = ProductCatalogMCP(product_catalog_server_url)

print("[*] Querying product catalog...")

try:
    # Get products by category
    print("[*] Getting electronics products...")
    electronics = product_catalog.get_products("electronics")

    import json
    if isinstance(electronics, str):
        import ast
        try:
            result_parsed = ast.literal_eval(electronics)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = electronics
    else:
        output = json.dumps(electronics, indent=2)

    if len(output) > 800:
        output = output[:800] + '\\n...\\n(truncated)'
    print(output)

    # Search for products
    print()
    print("[*] Searching for 'laptop' products...")
    search_results = product_catalog.search_products("laptop")
    print(f"[SUCCESS] Search results: {search_results}")

    # Get specific product
    print()
    print("[*] Getting product details for ID 1...")
    product = product_catalog.get_product_by_id(1)
    print(f"[SUCCESS] Product: {product}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] Product catalog queries complete')
"""

# Update all cells
nb['cells'][63]['source'] = cell_63_content.split('\n')
nb['cells'][67]['source'] = cell_67_content.split('\n')

# Find cell 67b - it might be at different index
# Look for cells between 67 and 73
for i in range(67, 73):
    cell_source = ''.join(nb['cells'][i].get('source', []))
    if 'weather' in cell_source.lower() and i != 67:
        print(f"Found weather cell at index {i}, updating...")
        nb['cells'][i]['source'] = cell_67b_content.split('\n')
        break

nb['cells'][69]['source'] = cell_69_content.split('\n')
nb['cells'][77]['source'] = cell_77_content.split('\n')

# Save notebook
with open('../master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\\nCells 63, 67, 67b, 69, 77 refactored successfully!")
print("All remaining cells updated to use working MCP helpers with Streamable HTTP transport")
