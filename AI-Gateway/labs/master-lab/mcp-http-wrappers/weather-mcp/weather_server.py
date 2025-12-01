#!/usr/bin/env python3
"""
OpenWeather MCP HTTP Server
A simple HTTP server that provides weather data via the OpenWeather API.
Exposes endpoints compatible with MCP tool calling patterns.
"""
import os
import json
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Weather MCP Server", version="1.0.0")

# OpenWeather API configuration
OWM_BASE_URL = "https://api.openweathermap.org/data/2.5"
OWM_API_KEY = os.getenv("OWM_API_KEY", "")


def get_api_key():
    """Get the OpenWeather API key from environment."""
    if not OWM_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OWM_API_KEY environment variable not set"
        )
    return OWM_API_KEY


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "weather-mcp",
        "api_key_configured": bool(OWM_API_KEY)
    }


@app.get("/weather")
async def get_weather(city: str, units: str = "metric"):
    """
    Get current weather for a city.

    Args:
        city: City name (e.g., "London", "New York", "Tokyo")
        units: Temperature units - "metric" (Celsius), "imperial" (Fahrenheit), or "standard" (Kelvin)

    Returns:
        Current weather data for the specified city
    """
    api_key = get_api_key()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{OWM_BASE_URL}/weather",
                params={
                    "q": city,
                    "appid": api_key,
                    "units": units
                },
                timeout=10.0
            )

            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid OpenWeather API key")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
            elif response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"OpenWeather API error: {response.text}"
                )

            data = response.json()

            # Format response for MCP-style consumption
            return {
                "city": data.get("name"),
                "country": data.get("sys", {}).get("country"),
                "coordinates": {
                    "lat": data.get("coord", {}).get("lat"),
                    "lon": data.get("coord", {}).get("lon")
                },
                "weather": {
                    "main": data.get("weather", [{}])[0].get("main"),
                    "description": data.get("weather", [{}])[0].get("description"),
                    "icon": data.get("weather", [{}])[0].get("icon")
                },
                "temperature": {
                    "current": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "min": data.get("main", {}).get("temp_min"),
                    "max": data.get("main", {}).get("temp_max"),
                    "unit": "°C" if units == "metric" else "°F" if units == "imperial" else "K"
                },
                "humidity": data.get("main", {}).get("humidity"),
                "pressure": data.get("main", {}).get("pressure"),
                "visibility": data.get("visibility"),
                "wind": {
                    "speed": data.get("wind", {}).get("speed"),
                    "direction": data.get("wind", {}).get("deg"),
                    "unit": "m/s" if units == "metric" else "mph" if units == "imperial" else "m/s"
                },
                "clouds": data.get("clouds", {}).get("all"),
                "timestamp": data.get("dt")
            }
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Failed to connect to OpenWeather API: {str(e)}")


@app.get("/forecast")
async def get_forecast(city: str, units: str = "metric"):
    """
    Get 5-day weather forecast for a city.

    Args:
        city: City name (e.g., "London", "New York", "Tokyo")
        units: Temperature units - "metric" (Celsius), "imperial" (Fahrenheit), or "standard" (Kelvin)

    Returns:
        5-day weather forecast with 3-hour intervals
    """
    api_key = get_api_key()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{OWM_BASE_URL}/forecast",
                params={
                    "q": city,
                    "appid": api_key,
                    "units": units
                },
                timeout=10.0
            )

            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid OpenWeather API key")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
            elif response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"OpenWeather API error: {response.text}"
                )

            data = response.json()

            # Format forecast data
            forecasts = []
            for item in data.get("list", []):
                forecasts.append({
                    "datetime": item.get("dt_txt"),
                    "timestamp": item.get("dt"),
                    "weather": {
                        "main": item.get("weather", [{}])[0].get("main"),
                        "description": item.get("weather", [{}])[0].get("description")
                    },
                    "temperature": {
                        "current": item.get("main", {}).get("temp"),
                        "feels_like": item.get("main", {}).get("feels_like"),
                        "min": item.get("main", {}).get("temp_min"),
                        "max": item.get("main", {}).get("temp_max")
                    },
                    "humidity": item.get("main", {}).get("humidity"),
                    "wind_speed": item.get("wind", {}).get("speed"),
                    "clouds": item.get("clouds", {}).get("all"),
                    "precipitation_probability": item.get("pop", 0) * 100
                })

            return {
                "city": data.get("city", {}).get("name"),
                "country": data.get("city", {}).get("country"),
                "coordinates": {
                    "lat": data.get("city", {}).get("coord", {}).get("lat"),
                    "lon": data.get("city", {}).get("coord", {}).get("lon")
                },
                "forecast_count": len(forecasts),
                "unit": "°C" if units == "metric" else "°F" if units == "imperial" else "K",
                "forecasts": forecasts
            }
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Failed to connect to OpenWeather API: {str(e)}")


@app.post("/messages")
async def mcp_messages(request: Request):
    """
    MCP-compatible JSON-RPC endpoint for tool calls.
    Handles MCP protocol messages for AI model integration.
    """
    try:
        body = await request.json()
        method = body.get("method", "")
        params = body.get("params", {})
        request_id = body.get("id")

        # Handle MCP protocol methods
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "weather-mcp",
                        "version": "1.0.0"
                    }
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_weather",
                            "description": "Get current weather for a city using OpenWeather API",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "city": {
                                        "type": "string",
                                        "description": "City name (e.g., 'London', 'New York', 'Tokyo')"
                                    },
                                    "units": {
                                        "type": "string",
                                        "enum": ["metric", "imperial", "standard"],
                                        "default": "metric",
                                        "description": "Temperature units"
                                    }
                                },
                                "required": ["city"]
                            }
                        },
                        {
                            "name": "get_forecast",
                            "description": "Get 5-day weather forecast for a city",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "city": {
                                        "type": "string",
                                        "description": "City name"
                                    },
                                    "units": {
                                        "type": "string",
                                        "enum": ["metric", "imperial", "standard"],
                                        "default": "metric",
                                        "description": "Temperature units"
                                    }
                                },
                                "required": ["city"]
                            }
                        }
                    ]
                }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            if tool_name == "get_weather":
                result = await get_weather(
                    city=tool_args.get("city", ""),
                    units=tool_args.get("units", "metric")
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }

            elif tool_name == "get_forecast":
                result = await get_forecast(
                    city=tool_args.get("city", ""),
                    units=tool_args.get("units", "metric")
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id") if 'body' in dir() else None,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"Starting Weather MCP Server on port {port}")
    print(f"API Key configured: {bool(OWM_API_KEY)}")
    uvicorn.run(app, host="0.0.0.0", port=port)
