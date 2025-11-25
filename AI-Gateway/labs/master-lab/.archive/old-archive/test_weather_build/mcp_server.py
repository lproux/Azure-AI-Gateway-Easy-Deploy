import random
import uvicorn
from fastmcp import FastMCP, Context

mcp = FastMCP("Weather")

@mcp.tool()
async def get_cities(ctx: Context, country: str) -> str:
    """Get list of cities for a given country."""
    cities_by_country = {
        "usa": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
        "uk": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
        "australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "india": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"],
        "portugal": ["Lisbon", "Porto", "Braga", "Faro", "Coimbra"],
    }
    return str(cities_by_country.get(country.lower(), []))

@mcp.tool()
async def get_weather(ctx: Context, city: str) -> str:
    """Get weather information for a given city."""
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy"]
    temperature = random.uniform(-10, 35)
    humidity = random.uniform(20, 100)
    weather_info = {
        "city": city,
        "condition": random.choice(weather_conditions),
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
    }
    return str(weather_info)

if __name__ == "__main__":
    # Use mcp.run() with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=8080, path="/weather")
