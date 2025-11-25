"""
MCP Helper Functions for Jupyter Notebooks

This module provides helper functions to simplify calling MCP servers
and APIM-routed REST APIs from Jupyter notebooks in the workshop exercises.

Supports 4 Data Sources:
- 2 Direct MCP Servers (Excel, Docs)
- 2 APIM-Routed REST APIs (GitHub, Weather)

Usage:
    from notebook_mcp_helpers import MCPClient

    # Initialize client
    mcp = MCPClient()

    # Call Excel Analytics tools
    result = mcp.excel.analyze_sales(
        file_path="/app/data/sales_performance.xlsx",
        group_by="Region"
    )

    # Call GitHub API through APIM
    repo = mcp.github.get_repository("microsoft", "semantic-kernel")

    # Call Weather API through APIM
    weather = mcp.weather.get_weather("Seattle", country_code="US")
"""

import json
import httpx
from typing import Dict, Any, Optional, List
from pathlib import Path


class MCPError(Exception):
    """Exception raised for MCP errors"""
    pass


class MCPClient:
    """Main MCP client for workshop exercises"""

    def __init__(self, config_file: str = ".mcp-servers-config"):
        """
        Initialize MCP client with configuration

        Supports 4 data sources:
        - 2 Direct MCP Servers (Excel, Docs)
        - 2 APIM-Routed REST APIs (GitHub, Weather)

        Args:
            config_file: Path to MCP servers configuration file
        """
        self.config = self._load_config(config_file)

        # Direct MCP Servers (Native MCP Protocol)
        excel_url = self.config.get("EXCEL_MCP_URL", "")
        self.excel = ExcelAnalyticsMCP(excel_url) if excel_url else None

        docs_url = self.config.get("DOCS_MCP_URL", "")
        self.docs = ResearchDocumentsMCP(docs_url) if docs_url else None

        # APIM Configuration
        apim_key = self.config.get("APIM_SUBSCRIPTION_KEY", "")

        # GitHub through APIM (REST API, not MCP protocol)
        apim_github_url = self.config.get("APIM_GITHUB_URL", "")
        if apim_github_url and apim_key:
            self.github = APIMGitHubClient(apim_github_url, apim_key)
        else:
            self.github = None

        # Weather through APIM (REST API)
        apim_weather_url = self.config.get("APIM_WEATHER_URL", "")
        weather_api_key = self.config.get("OPENWEATHER_API_KEY", "")
        if apim_weather_url and apim_key and weather_api_key:
            self.weather = WeatherAPIClient(apim_weather_url, apim_key, weather_api_key)
        else:
            self.weather = None

        self._request_id = 0

    def _load_config(self, config_file: str) -> Dict[str, str]:
        """Load configuration from file"""
        config = {}
        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}\n"
                f"Please run deployment script first."
            )

        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value

        return config

    def _next_id(self) -> int:
        """Get next request ID"""
        self._request_id += 1
        return self._request_id

    def call_tool(
        self,
        server_url: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generic tool call to any MCP server

        Args:
            server_url: MCP server URL
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        response = httpx.post(
            f"{server_url}/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=30.0
        )

        response.raise_for_status()
        result = response.json()

        if "error" in result:
            raise MCPError(f"MCP Error: {result['error']}")

        return result.get("result", {})


class ExcelAnalyticsMCP:
    """Excel Analytics MCP Server client"""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self._request_id = 0

    def _call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to call Excel MCP tools"""
        response = httpx.post(
            f"{self.server_url}/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=30.0
        )

        response.raise_for_status()
        result = response.json()

        # Check for JSON-RPC error response
        if "error" in result and result["error"] is not None:
            error_msg = result["error"]
            if isinstance(error_msg, dict):
                error_msg = error_msg.get("message", str(error_msg))
            raise MCPError(f"Excel MCP Error: {error_msg}")

        # Return the result content (may be wrapped in content field)
        if "result" in result:
            result_data = result["result"]
            # Handle MCP tool response format with content array
            if isinstance(result_data, dict) and "content" in result_data:
                content = result_data["content"]
                if isinstance(content, list) and len(content) > 0:
                    # Extract text from first content item
                    return content[0].get("text", content[0]) if isinstance(content[0], dict) else content[0]
            return result_data

        return {}

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def upload_excel(
        self,
        local_file_path: str,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a local Excel file to the MCP server

        Args:
            local_file_path: Path to local Excel file
            sheet_name: Optional sheet name

        Returns:
            Upload result with file info
        """
        import base64
        from pathlib import Path

        file_path = Path(local_file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {local_file_path}")

        # Read and encode file
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
            file_content_base64 = base64.b64encode(file_bytes).decode('utf-8')

        return self._call("upload_excel", {
            "file_name": file_path.name,
            "file_content_base64": file_content_base64,
            "sheet_name": sheet_name
        })

    def load_excel(
        self,
        file_path: str,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Load an Excel file into memory

        Args:
            file_path: Path to Excel file (e.g., "/app/data/sales_performance.xlsx")
            sheet_name: Optional sheet name

        Returns:
            Dict with file info, columns, preview
        """
        return self._call("load_excel", {
            "file_path": file_path,
            "sheet_name": sheet_name
        })

    def analyze_sales(
        self,
        file_path: str,
        group_by: str = "Region",
        metric: str = "TotalSales"
    ) -> Dict[str, Any]:
        """
        Analyze sales data from Excel file

        Args:
            file_path: Path to Excel file
            group_by: Column to group by (e.g., "Region", "Product")
            metric: Metric to analyze (e.g., "TotalSales", "Quantity")

        Returns:
            Dict with analysis results and summary
        """
        return self._call("analyze_sales", {
            "file_path": file_path,
            "group_by": group_by,
            "metric": metric
        })

    def calculate_costs(
        self,
        file_path: str,
        resource_type_col: str = "Resource_Type",
        cost_col: str = "Daily_Cost"
    ) -> Dict[str, Any]:
        """
        Calculate Azure resource costs from Excel data

        Args:
            file_path: Path to Excel file with cost data
            resource_type_col: Column name for resource type
            cost_col: Column name for cost

        Returns:
            Dict with cost analysis and monthly projection
        """
        return self._call("calculate_costs", {
            "file_path": file_path,
            "resource_type_col": resource_type_col,
            "cost_col": cost_col
        })

    def generate_chart(
        self,
        file_path: str,
        chart_type: str,
        x_column: str,
        y_column: str
    ) -> Dict[str, Any]:
        """
        Generate a chart from Excel data

        Args:
            file_path: Path to Excel file
            chart_type: Type of chart ("bar", "line", "pie")
            x_column: Column for X-axis
            y_column: Column for Y-axis

        Returns:
            Dict with base64-encoded image
        """
        return self._call("generate_chart", {
            "file_path": file_path,
            "chart_type": chart_type,
            "x_column": x_column,
            "y_column": y_column
        })


class ResearchDocumentsMCP:
    """Research Documents MCP Server client"""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self._request_id = 0

    def _call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to call Docs MCP tools"""
        response = httpx.post(
            f"{self.server_url}/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=30.0
        )

        response.raise_for_status()
        result = response.json()

        # Check for JSON-RPC error response
        if "error" in result and result["error"] is not None:
            error_msg = result["error"]
            if isinstance(error_msg, dict):
                error_msg = error_msg.get("message", str(error_msg))
            raise MCPError(f"Docs MCP Error: {error_msg}")

        # Return the result content (may be wrapped in content field)
        if "result" in result:
            result_data = result["result"]
            # Handle MCP tool response format with content array
            if isinstance(result_data, dict) and "content" in result_data:
                content = result_data["content"]
                if isinstance(content, list) and len(content) > 0:
                    # Extract text from first content item
                    return content[0].get("text", content[0]) if isinstance(content[0], dict) else content[0]
            return result_data

        return {}

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def list_documents(self, pattern: str = "*.md") -> Dict[str, Any]:
        """
        List available documents

        Args:
            pattern: Glob pattern to filter files

        Returns:
            Dict with list of documents
        """
        return self._call("list_documents", {"pattern": pattern})

    def search_documents(
        self,
        query: str,
        case_sensitive: bool = False
    ) -> Dict[str, Any]:
        """
        Search documents for keywords

        Args:
            query: Search query
            case_sensitive: Whether search is case-sensitive

        Returns:
            Dict with search results and context
        """
        return self._call("search_documents", {
            "query": query,
            "case_sensitive": case_sensitive
        })

    def get_document_content(self, file_name: str) -> Dict[str, Any]:
        """
        Get full content of a document

        Args:
            file_name: Name of the document

        Returns:
            Dict with document content
        """
        return self._call("get_document_content", {"file_name": file_name})

    def compare_documents(self, file_names: List[str]) -> Dict[str, Any]:
        """
        Compare multiple documents

        Args:
            file_names: List of document file names

        Returns:
            Dict with comparison analysis
        """
        return self._call("compare_documents", {"file_names": file_names})


class APIMGitHubClient:
    """
    GitHub REST API client through Azure API Management

    This client uses GitHub's REST API v3 through APIM gateway.
    Provides access to repositories, commits, issues, and search functionality.

    Usage:
        client = APIMGitHubClient(
            base_url="https://apim-gateway.azure-api.net/github",
            subscription_key="your-apim-key"
        )

        # Get repository info
        repo = client.get_repository("microsoft", "semantic-kernel")

        # Search repositories
        results = client.search_repositories("AI language:python")

        # List commits
        commits = client.list_repository_commits("microsoft", "semantic-kernel")
    """

    def __init__(self, base_url: str, subscription_key: str):
        """
        Initialize GitHub API client

        Args:
            base_url: APIM GitHub API base URL (e.g., https://apim-xxx.azure-api.net/github)
            subscription_key: APIM subscription key
        """
        self.base_url = base_url.rstrip('/')
        self.subscription_key = subscription_key
        self.headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'Notebook-MCP-Helper'
        }

    def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal GET request to GitHub API through APIM"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = httpx.get(url, headers=self.headers, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()

    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Search for GitHub repositories

        Args:
            query: Search query (e.g., "AI language:python", "machine learning")
            sort: Sort field ("stars", "forks", "updated")
            order: Sort order ("asc", "desc")
            per_page: Results per page (max 100)

        Returns:
            Dict with total_count and items (list of repositories)
        """
        params = {
            'q': query,
            'sort': sort,
            'order': order,
            'per_page': min(per_page, 100)
        }
        return self._get('search/repositories', params)

    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get details about a specific repository

        Args:
            owner: Repository owner (e.g., "microsoft")
            repo: Repository name (e.g., "vscode")

        Returns:
            Dict with repository details including stars, forks, description, etc.
        """
        return self._get(f'repos/{owner}/{repo}')

    def get_issues(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get issues for a repository (alias for list_repository_issues)

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state ("open", "closed", or "all")
            per_page: Results per page (max 100)

        Returns:
            List of repository issues
        """
        return self.list_repository_issues(owner, repo, state, per_page)

    def list_repository_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        List issues for a repository

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state ("open", "closed", or "all")
            per_page: Results per page (max 100)

        Returns:
            List of repository issues
        """
        params = {
            'state': state,
            'per_page': min(per_page, 100)
        }
        return self._get(f'repos/{owner}/{repo}/issues', params)

    def get_repository_readme(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get README content for a repository

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dict with README content and metadata
        """
        return self._get(f'repos/{owner}/{repo}/readme')

    def get_commits(
        self,
        owner: str,
        repo: str,
        per_page: int = 10,
        sha: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recent commits for a repository (alias for list_repository_commits)

        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Number of commits to return (max 100)
            sha: SHA or branch to start listing commits from

        Returns:
            List of recent commits
        """
        return self.list_repository_commits(owner, repo, per_page, sha)

    def list_repository_commits(
        self,
        owner: str,
        repo: str,
        per_page: int = 10,
        sha: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List recent commits for a repository

        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Number of commits to return (max 100)
            sha: SHA or branch to start listing commits from

        Returns:
            List of recent commits
        """
        params = {
            'per_page': min(per_page, 100)
        }
        if sha:
            params['sha'] = sha

        return self._get(f'repos/{owner}/{repo}/commits', params)

    def get_repository_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        Get programming languages used in a repository

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dict mapping language names to bytes of code
        """
        return self._get(f'repos/{owner}/{repo}/languages')

    def get_repository_contributors(
        self,
        owner: str,
        repo: str,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get contributors for a repository

        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Results per page (max 100)

        Returns:
            List of contributors with contribution counts
        """
        params = {'per_page': min(per_page, 100)}
        return self._get(f'repos/{owner}/{repo}/contributors', params)


class WeatherAPIClient:
    """
    OpenWeatherMap API client through Azure API Management

    This client uses OpenWeatherMap REST API v2.5 through APIM gateway.
    Provides real-time weather data, forecasts, and historical weather.

    Free tier: 1,000 API calls/day, 60 calls/minute
    Get API key: https://openweathermap.org/api

    Usage:
        client = WeatherAPIClient(
            base_url="https://apim-gateway.azure-api.net/weather",
            subscription_key="your-apim-key",
            weather_api_key="your-openweather-key"
        )

        # Get current weather
        weather = client.get_weather("London")

        # Get forecast
        forecast = client.get_forecast("New York", days=5)
    """

    def __init__(self, base_url: str, subscription_key: str, weather_api_key: str):
        """
        Initialize Weather API client

        Args:
            base_url: APIM Weather API base URL (e.g., https://apim-xxx.azure-api.net/weather)
            subscription_key: APIM subscription key
            weather_api_key: OpenWeatherMap API key
        """
        self.base_url = base_url.rstrip('/')
        self.subscription_key = subscription_key
        self.weather_api_key = weather_api_key
        self.headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'User-Agent': 'Notebook-MCP-Helper'
        }

    def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Internal GET request to Weather API through APIM"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Add API key to params
        if params is None:
            params = {}
        params['appid'] = self.weather_api_key

        response = httpx.get(url, headers=self.headers, params=params, timeout=30.0)
        response.raise_for_status()

        return response.json()

    def get_weather(
        self,
        city: str,
        country_code: Optional[str] = None,
        units: str = "metric"
    ) -> Dict[str, Any]:
        """
        Get current weather for a city

        Args:
            city: City name (e.g., "London", "New York")
            country_code: Optional ISO 3166 country code (e.g., "GB", "US")
            units: Temperature units ("metric", "imperial", "standard")
                   metric = Celsius, imperial = Fahrenheit

        Returns:
            Dict with weather data including:
            - temp: Current temperature
            - feels_like: Feels like temperature
            - description: Weather description
            - humidity: Humidity percentage
            - wind_speed: Wind speed
        """
        query = city
        if country_code:
            query = f"{city},{country_code}"

        params = {
            'q': query,
            'units': units
        }

        return self._get('weather', params)

    def get_weather_by_coords(
        self,
        lat: float,
        lon: float,
        units: str = "metric"
    ) -> Dict[str, Any]:
        """
        Get current weather by geographic coordinates

        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature units ("metric", "imperial", "standard")

        Returns:
            Dict with weather data
        """
        params = {
            'lat': lat,
            'lon': lon,
            'units': units
        }

        return self._get('weather', params)

    def get_forecast(
        self,
        city: str,
        country_code: Optional[str] = None,
        units: str = "metric",
        cnt: int = 40
    ) -> Dict[str, Any]:
        """
        Get 5-day weather forecast (3-hour intervals)

        Args:
            city: City name
            country_code: Optional ISO 3166 country code
            units: Temperature units
            cnt: Number of forecast points (max 40 = 5 days * 8 intervals)

        Returns:
            Dict with forecast data including list of forecasts
        """
        query = city
        if country_code:
            query = f"{city},{country_code}"

        params = {
            'q': query,
            'units': units,
            'cnt': min(cnt, 40)  # Max 40 entries (5 days)
        }

        return self._get('forecast', params)

    def search_cities(self, city_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for cities by name (returns coordinates and country)

        Args:
            city_name: City name to search
            limit: Max number of results (default: 5)

        Returns:
            List of matching cities with coordinates
        """
        # Note: OpenWeatherMap Geocoding API uses /geo/1.0/direct
        # This is a different endpoint from weather data
        params = {
            'q': city_name,
            'limit': limit
        }

        try:
            # Try geocoding endpoint
            return self._get('geo/1.0/direct', params)
        except Exception:
            # Fallback: return current weather which includes coords
            weather = self.get_weather(city_name)
            return [{
                'name': city_name,
                'lat': weather.get('coord', {}).get('lat'),
                'lon': weather.get('coord', {}).get('lon'),
                'country': weather.get('sys', {}).get('country')
            }]

    def format_weather_summary(self, weather_data: Dict[str, Any]) -> str:
        """
        Format weather data into a readable summary

        Args:
            weather_data: Weather data from get_weather()

        Returns:
            Formatted string summary
        """
        try:
            main = weather_data.get('main', {})
            weather = weather_data.get('weather', [{}])[0]
            wind = weather_data.get('wind', {})

            summary = f"""
Weather Summary for {weather_data.get('name', 'Unknown')}:
  Condition: {weather.get('description', 'N/A').title()}
  Temperature: {main.get('temp', 'N/A')}°C (feels like {main.get('feels_like', 'N/A')}°C)
  Humidity: {main.get('humidity', 'N/A')}%
  Wind Speed: {wind.get('speed', 'N/A')} m/s
  Pressure: {main.get('pressure', 'N/A')} hPa
"""
            return summary.strip()
        except Exception as e:
            return f"Error formatting weather data: {e}"


# Convenience functions for quick usage
def quick_mcp_client() -> MCPClient:
    """Create a quick MCP client with default config"""
    return MCPClient()


def display_chart(chart_result: Dict[str, Any]):
    """
    Display a chart from Excel Analytics MCP result

    Args:
        chart_result: Result from generate_chart()
    """
    import base64
    from IPython.display import Image, display

    if "image_base64" in chart_result:
        img_data = base64.b64decode(chart_result["image_base64"])
        display(Image(data=img_data))
    else:
        print("No chart image found in result")


def display_sales_analysis(analysis_result: Dict[str, Any]):
    """
    Display sales analysis results as a formatted table

    Args:
        analysis_result: Result from analyze_sales()
    """
    import pandas as pd
    from IPython.display import display

    if "analysis" in analysis_result:
        df = pd.DataFrame(analysis_result["analysis"])
        print(f"\n📊 Sales Analysis Summary")
        print(f"   Total: ${analysis_result['summary']['total']:,.2f}")
        print(f"   Average: ${analysis_result['summary']['average']:,.2f}")
        print(f"   Count: {analysis_result['summary']['count']}\n")
        display(df)
    else:
        print("No analysis data found in result")


def display_document_search(search_result: Dict[str, Any]):
    """
    Display document search results

    Args:
        search_result: Result from search_documents()
    """
    if "results" in search_result:
        print(f"\n🔍 Found {search_result['results_count']} documents matching '{search_result['query']}':\n")

        for i, doc in enumerate(search_result["results"], 1):
            print(f"{i}. 📄 {doc['file_name']}")
            print(f"   Matches: {doc['match_count']}")
            print(f"   Context: {doc['context'][:100]}...")
            print()
    else:
        print("No search results found")


# Azure OpenAI Integration Functions
import os

async def call_azure_openai(prompt: str, system_message: str = "You are a helpful data analyst.") -> str:
    """
    Call Azure OpenAI through APIM Gateway

    Args:
        prompt: User prompt/question
        system_message: System context for the AI

    Returns:
        AI-generated response text
    """
    # Get configuration from environment
    APIM_ENDPOINT = os.getenv('APIM_GATEWAY_URL', 'https://apim-mcp-gateway-xxxxxx.azure-api.net')
    APIM_KEY = os.getenv('APIM_SUBSCRIPTION_KEY', os.getenv('AZURE_OPENAI_KEY', 'your-subscription-key'))
    DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_GPT4O', 'gpt-4o')

    url = f"{APIM_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2024-08-01-preview"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": APIM_KEY,
        "api-key": APIM_KEY  # Fallback for direct Azure OpenAI
    }

    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]


# Example usage template
EXAMPLE_USAGE = """
# Example: Using MCP Helpers in Jupyter Notebook

from notebook_mcp_helpers import MCPClient, display_chart, display_sales_analysis

# Initialize MCP client (4 data sources)
mcp = MCPClient()

# 1. Excel Analytics (Direct MCP)
sales_result = mcp.excel.analyze_sales(
    file_path="/app/data/sales_performance.xlsx",
    group_by="Region",
    metric="TotalSales"
)
display_sales_analysis(sales_result)

# Generate and display chart
chart_result = mcp.excel.generate_chart(
    file_path="/app/data/sales_performance.xlsx",
    chart_type="bar",
    x_column="Region",
    y_column="TotalSales"
)
display_chart(chart_result)

# 2. Document Search (Direct MCP)
search_result = mcp.docs.search_documents(query="Azure OpenAI")
display_document_search(search_result)

# 3. GitHub API (APIM-Routed REST)
repo = mcp.github.get_repository("microsoft", "semantic-kernel")
print(f"Repository: {repo['full_name']}")
print(f"Stars: {repo['stargazers_count']:,}")
print(f"Description: {repo['description']}")

# Search repositories
results = mcp.github.search_repositories("AI language:python", per_page=5)
for item in results['items']:
    print(f"- {item['full_name']} ({item['stargazers_count']} stars)")

# 4. Weather API (APIM-Routed REST)
weather = mcp.weather.get_weather("Seattle", country_code="US")
summary = mcp.weather.format_weather_summary(weather)
print(summary)

# Get forecast
forecast = mcp.weather.get_forecast("London", country_code="GB", cnt=8)
for item in forecast['list'][:4]:
    print(f"{item['dt_txt']}: {item['main']['temp']}°C - {item['weather'][0]['description']}")
"""

if __name__ == "__main__":
    print("MCP Helper Functions for Jupyter Notebooks")
    print("=" * 50)
    print(EXAMPLE_USAGE)
