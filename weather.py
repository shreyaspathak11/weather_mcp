import httpx
import logging
import os
from typing import Any
from mcp.server.fastmcp import FastMCP

"""
Weather MCP Server

This server provides tools to fetch current weather and forecasts for any city worldwide using WeatherAPI.
"""

# Initialize the MCP server
mcp = FastMCP("weather")

# Constants for WeatherAPI
WEATHERAPI_BASE = "https://api.weatherapi.com/v1"
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY") 
USER_AGENT = "weather-app/1.0"

# HELPER FUNCTIONS
# These functions are used to make requests to weather APIs
async def make_request(url: str, headers: dict = None) -> dict[str, Any] | None:
    """
    Make a request to weather API
    """
    default_headers = {"User-Agent": USER_AGENT}
    if headers:
        default_headers.update(headers)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=default_headers, timeout=30.0)
            response.raise_for_status()
            logging.info(f"Request to {url} successful with status code {response.status_code}")
            return response.json()
        except Exception as e:
            logging.error(f"Error occurred while making request to {url}: {e}")
            return None


# IMPLEMENTATION OF TOOLS
# Tools are functions that can be called by the MCP client


@mcp.tool()
async def get_weather_by_city(city: str) -> str:
    """Get current weather for any city worldwide using WeatherAPI.

    Args:
        city: Name of the city (e.g., "Durgapur", "London", "New York")
    """
    # Using WeatherAPI for global weather data
    url = f"{WEATHERAPI_BASE}/current.json?key={WEATHERAPI_KEY}&q={city}&aqi=yes"
    data = await make_request(url)

    if not data:
        return f"Unable to fetch weather data for {city}. Please check the city name and ensure you have a valid API key."

    if "error" in data:
        return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

    # Extract weather information
    location = data.get("location", {})
    current = data.get("current", {})
    condition = current.get("condition", {})
    
    # Format the weather information
    weather_info = f"""
        Weather for {location.get('name', city)}, {location.get('region', '')}, {location.get('country', '')}:

        Current Conditions: {condition.get('text', 'Unknown')}
        Temperature: {current.get('temp_c', 'Unknown')}°C (feels like {current.get('feelslike_c', 'Unknown')}°C)
        Humidity: {current.get('humidity', 'Unknown')}%
        Pressure: {current.get('pressure_mb', 'Unknown')} mb
        Wind: {current.get('wind_kph', 'Unknown')} km/h {current.get('wind_dir', '')}
        UV Index: {current.get('uv', 'Unknown')}
        Visibility: {current.get('vis_km', 'Unknown')} km

        Local Time: {location.get('localtime', 'Unknown')}
        Last Updated: {current.get('last_updated', 'Unknown')}
    """
    
    return weather_info.strip()


@mcp.tool()
async def get_weather_forecast_by_city(city: str, days: int = 3) -> str:
    """Get weather forecast for any city worldwide using WeatherAPI.

    Args:
        city: Name of the city (e.g., "Durgapur", "London", "New York")
        days: Number of forecast days (1-10, default is 3)
    """
    # Limit days to WeatherAPI's free tier limit
    days = min(max(days, 1), 3)  # Free tier allows up to 3 days
    
    # Using WeatherAPI for global weather forecast
    url = f"{WEATHERAPI_BASE}/forecast.json?key={WEATHERAPI_KEY}&q={city}&days={days}&aqi=no&alerts=no"
    data = await make_request(url)

    if not data:
        return f"Unable to fetch forecast data for {city}. Please check the city name and ensure you have a valid API key."

    if "error" in data:
        return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

    # Extract forecast information
    location = data.get("location", {})
    forecast = data.get("forecast", {})
    forecast_days = forecast.get("forecastday", [])
    
    if not forecast_days:
        return f"No forecast data available for {city}."
    
    forecasts = []
    for day_forecast in forecast_days:
        date = day_forecast.get("date", "")
        day_data = day_forecast.get("day", {})
        condition = day_data.get("condition", {})
        
        forecast_info = f"""
            {date}:
            Weather: {condition.get('text', 'Unknown')}
            Max Temperature: {day_data.get('maxtemp_c', 'Unknown')}°C
            Min Temperature: {day_data.get('mintemp_c', 'Unknown')}°C
            Avg Temperature: {day_data.get('avgtemp_c', 'Unknown')}°C
            Humidity: {day_data.get('avghumidity', 'Unknown')}%
            Max Wind: {day_data.get('maxwind_kph', 'Unknown')} km/h
            Chance of Rain: {day_data.get('daily_chance_of_rain', 'Unknown')}%
            UV Index: {day_data.get('uv', 'Unknown')}
        """
        forecasts.append(forecast_info.strip())
    
    header = f"{days}-Day Weather Forecast for {location.get('name', city)}, {location.get('region', '')}, {location.get('country', '')}:\n"
    return header + "\n---\n".join(forecasts)
    

if __name__ == "__main__":
    mcp.run()

