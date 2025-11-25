import uvicorn
from fastmcp import FastMCP, Context

mcp = FastMCP("GitHub")

# Mock GitHub data
MOCK_REPOS = [
    {
        "id": 1,
        "name": "awesome-ai",
        "full_name": "aidevs/awesome-ai",
        "description": "A curated list of AI resources and projects",
        "language": "Python",
        "stars": 15234,
        "forks": 2314,
        "open_issues": 45,
        "url": "https://github.com/aidevs/awesome-ai",
        "topics": ["ai", "machine-learning", "deep-learning"]
    },
    {
        "id": 2,
        "name": "python-ml-framework",
        "full_name": "mlops/python-ml-framework",
        "description": "Modern machine learning framework for Python",
        "language": "Python",
        "stars": 8234,
        "forks": 1420,
        "open_issues": 23,
        "url": "https://github.com/mlops/python-ml-framework",
        "topics": ["python", "machine-learning", "mlops"]
    },
    {
        "id": 3,
        "name": "ai-chatbot",
        "full_name": "chatbots/ai-chatbot",
        "description": "Intelligent chatbot powered by GPT",
        "language": "Python",
        "stars": 6789,
        "forks": 892,
        "open_issues": 12,
        "url": "https://github.com/chatbots/ai-chatbot",
        "topics": ["ai", "chatbot", "gpt", "nlp"]
    },
    {
        "id": 4,
        "name": "neural-networks-101",
        "full_name": "education/neural-networks-101",
        "description": "Introduction to neural networks with Python examples",
        "language": "Python",
        "stars": 4567,
        "forks": 678,
        "open_issues": 8,
        "url": "https://github.com/education/neural-networks-101",
        "topics": ["neural-networks", "education", "python"]
    },
    {
        "id": 5,
        "name": "data-science-toolkit",
        "full_name": "datasci/data-science-toolkit",
        "description": "Essential tools for data science projects",
        "language": "Python",
        "stars": 12456,
        "forks": 1867,
        "open_issues": 34,
        "url": "https://github.com/datasci/data-science-toolkit",
        "topics": ["data-science", "python", "analytics"]
    }
]

@mcp.tool()
async def search_repositories(ctx: Context, query: str) -> str:
    """
    Search for GitHub repositories

    Args:
        query: Search query (e.g., "AI language:python", "machine learning")
    """
    # Simple search implementation
    query_lower = query.lower()
    results = []

    for repo in MOCK_REPOS:
        # Check if query terms appear in name, description, or language
        searchable = f"{repo['name']} {repo['description']} {repo['language']} {' '.join(repo['topics'])}".lower()

        # Extract language filter if present
        if "language:" in query_lower:
            lang_part = query_lower.split("language:")[-1].split()[0]
            if lang_part not in repo['language'].lower():
                continue
            # Remove language: part from query for text search
            query_terms = query_lower.replace(f"language:{lang_part}", "").strip().split()
        else:
            query_terms = query_lower.split()

        # Check if all query terms match
        if all(term in searchable for term in query_terms if term):
            results.append(repo)

    return str({
        "total_count": len(results),
        "items": results
    })

@mcp.tool()
async def get_repository(ctx: Context, owner: str, repo: str) -> str:
    """
    Get details about a specific repository

    Args:
        owner: Repository owner (e.g., "microsoft")
        repo: Repository name (e.g., "vscode")
    """
    full_name = f"{owner}/{repo}".lower()

    # Find matching repo
    for r in MOCK_REPOS:
        if r['full_name'].lower() == full_name:
            return str(r)

    # Return mock data if not found
    return str({
        "id": 999,
        "name": repo,
        "full_name": f"{owner}/{repo}",
        "description": f"Mock repository for {owner}/{repo}",
        "language": "Python",
        "stars": 1234,
        "forks": 234,
        "open_issues": 10,
        "url": f"https://github.com/{owner}/{repo}",
        "topics": ["mock", "example"]
    })

@mcp.tool()
async def list_repository_issues(ctx: Context, owner: str, repo: str, state: str = "open") -> str:
    """
    List issues for a repository

    Args:
        owner: Repository owner
        repo: Repository name
        state: Issue state ("open", "closed", or "all")
    """
    mock_issues = [
        {
            "id": 1,
            "number": 123,
            "title": "Add support for feature X",
            "state": "open",
            "user": {"login": "user1"},
            "labels": [{"name": "enhancement"}],
            "created_at": "2025-01-15T10:00:00Z"
        },
        {
            "id": 2,
            "number": 124,
            "title": "Bug in module Y",
            "state": "open",
            "user": {"login": "user2"},
            "labels": [{"name": "bug"}],
            "created_at": "2025-01-16T14:30:00Z"
        },
        {
            "id": 3,
            "number": 122,
            "title": "Update documentation",
            "state": "closed",
            "user": {"login": "user3"},
            "labels": [{"name": "documentation"}],
            "created_at": "2025-01-14T09:15:00Z"
        }
    ]

    # Filter by state
    if state != "all":
        mock_issues = [issue for issue in mock_issues if issue["state"] == state]

    return str(mock_issues)

@mcp.tool()
async def get_repository_readme(ctx: Context, owner: str, repo: str) -> str:
    """
    Get README content for a repository

    Args:
        owner: Repository owner
        repo: Repository name
    """
    readme_content = f"""# {repo}

Repository: {owner}/{repo}

## Description
This is a mock README file for the {repo} repository.

## Features
- Feature 1: Basic functionality
- Feature 2: Advanced operations
- Feature 3: Integration capabilities

## Installation
```bash
pip install {repo}
```

## Usage
```python
import {repo}

# Your code here
```

## Contributing
Contributions are welcome! Please read CONTRIBUTING.md for details.

## License
MIT License
"""

    return str({
        "content": readme_content,
        "encoding": "utf-8",
        "size": len(readme_content)
    })

@mcp.tool()
async def list_repository_commits(ctx: Context, owner: str, repo: str, limit: int = 10) -> str:
    """
    List recent commits for a repository

    Args:
        owner: Repository owner
        repo: Repository name
        limit: Maximum number of commits to return (default: 10)
    """
    mock_commits = [
        {
            "sha": "abc123def456",
            "commit": {
                "author": {"name": "John Doe", "email": "john@example.com", "date": "2025-01-20T15:30:00Z"},
                "message": "Add new feature for data processing"
            }
        },
        {
            "sha": "def456ghi789",
            "commit": {
                "author": {"name": "Jane Smith", "email": "jane@example.com", "date": "2025-01-19T10:15:00Z"},
                "message": "Fix bug in error handling"
            }
        },
        {
            "sha": "ghi789jkl012",
            "commit": {
                "author": {"name": "Bob Johnson", "email": "bob@example.com", "date": "2025-01-18T14:45:00Z"},
                "message": "Update dependencies"
            }
        }
    ]

    return str(mock_commits[:limit])

if __name__ == "__main__":
    # Use mcp.run() with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=8080, path="/github")
