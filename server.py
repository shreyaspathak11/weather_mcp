"""
Weather MCP Server

This server provides tools to fetch current weather and forecasts for any city worldwide using WeatherAPI.
It also includes location detection tools to get weather for the user's current location.

Modular version with separated concerns:
- API Service: Handles all HTTP requests
- Weather Service: Handles weather data processing
- Location Service: Handles location detection
- Utils: Contains validators and formatters
"""

import sys
import os


from mcp.server.fastmcp import FastMCP
from src.services.weather_service import WeatherService
from src.services.location_service import LocationService

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Initialize the MCP server
mcp = FastMCP("weather")


# IMPLEMENTATION OF TOOLS
# Tools are functions that can be called by the MCP client


@mcp.tool()
async def get_weather_by_city(city: str) -> str:
    """Get current weather for any city worldwide using WeatherAPI.

    Args:
        city: Name of the city (e.g., "Durgapur", "London", "New York")
    """
    return await WeatherService.get_current_weather(city)


@mcp.tool()
async def get_weather_forecast_by_city(city: str, days: int = 3) -> str:
    """Get weather forecast for any city worldwide using WeatherAPI.

    Args:
        city: Name of the city (e.g., "Durgapur", "London", "New York")
        days: Number of forecast days (1-10, default is 3)
    """
    return await WeatherService.get_weather_forecast(city, days)


@mcp.tool()
async def get_location_by_ip(ip_address: str) -> str:
    """Get location information based on IP address.

    Args:
        ip_address: IP address of the user (e.g., "8.8.8.8")
    """
    return await LocationService.get_location_by_ip(ip_address)


@mcp.tool()
async def get_weather_by_coordinates(lat: float, lon: float) -> str:
    """Get current weather for a specific location using coordinates (latitude and longitude).

    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    return await WeatherService.get_weather_by_coordinates(lat, lon)


@mcp.tool()
async def get_weather_forecast_by_coordinates(lat: float, lon: float, days: int = 3) -> str:
    """Get weather forecast for a specific location using coordinates (latitude and longitude).

    Args:
        lat: Latitude of the location
        lon: Longitude of the location
        days: Number of forecast days (1-10, default is 3)
    """
    return await WeatherService.get_forecast_by_coordinates(lat, lon, days)


@mcp.tool()
async def get_location_and_weather_by_ip(ip_address: str) -> str:
    """Get location and weather information based on IP address.

    Args:
        ip_address: IP address of the user (e.g., "8.8.8.8")
    """
    if not ip_address:
        return "IP address is required to fetch location and weather."
    
    # Get location info
    location_info = await LocationService.get_location_by_ip(ip_address)
    
    # Get location data for weather lookup
    location_data = await LocationService.fetch_ip_location(ip_address)
    if not location_data:
        return location_info + "\n\nUnable to fetch weather data."
    
    # Get weather data
    lat = location_data.get("lat")
    lon = location_data.get("lon")
    weather_info = await WeatherService.get_weather_by_coordinates(lat, lon)
    
    return location_info + "\n\n" + weather_info


@mcp.tool()
async def get_user_current_location() -> str:
    """Get the user's current approximate location based on their IP address.
    
    This tool attempts to detect the user's location using their IP address.
    Note: This provides approximate location and may not be 100% accurate.
    
    Returns:
        A string describing the user's approximate location and coordinates
    """
    return await LocationService.get_current_location_info()


@mcp.tool()
async def get_weather_at_current_location() -> str:
    """Get current weather at the user's detected location.
    
    This tool combines location detection with weather fetching to provide
    weather information for the user's current approximate location.
    
    Returns:
        Current weather information for the user's detected location
    """
    return await WeatherService.get_weather_at_current_location()


@mcp.tool()
async def get_forecast_at_current_location(days: int = 3) -> str:
    """Get weather forecast at the user's detected location.
    
    Args:
        days: Number of forecast days (1-3, default is 3)
    
    Returns:
        Weather forecast for the user's detected location
    """
    return await WeatherService.get_forecast_at_current_location(days)


if __name__ == "__main__":
    mcp.run()
