import httpx
import logging
from mcp.server.fastmcp import FastMCP
import os
from typing import Any

"""
Weather MCP Server

This server provides tools to fetch current weather and forecasts for any city worldwide using WeatherAPI.
It also includes location detection tools to get weather for the user's current location.
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

# Constants for WeatherAPI
WEATHERAPI_BASE = "https://api.weatherapi.com/v1"
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY","c1e8d2b4514b4baf9c4184055251007") 
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


def validate_api_key() -> str | None:
    """Validate that WeatherAPI key is available"""
    if not WEATHERAPI_KEY:
        return "Error: WEATHERAPI_KEY environment variable is not set. Please get an API key from weatherapi.com and add it to your .env file."
    return None


def limit_forecast_days(days: int) -> int:
    """Limit forecast days to WeatherAPI's free tier limit"""
    return min(max(days, 1), 3)  # Free tier allows up to 3 days


def format_location_string(location: dict) -> str:
    """Format location data into a readable string"""
    name = location.get('name', 'Unknown location')
    region = location.get('region', '')
    country = location.get('country', '')
    
    if region:
        return f"{name}, {region}, {country}"
    return f"{name}, {country}"


def format_current_weather(location: dict, current: dict, with_emojis: bool = False) -> str:
    """Format current weather data into a readable string"""
    condition = current.get("condition", {})
    location_str = format_location_string(location)
    
    if with_emojis:
        return f"""
    🌟 Weather at Your Current Location:
    📍 {location_str}

    ☁️  Current Conditions: {condition.get('text', 'Unknown')}
    🌡️  Temperature: {current.get('temp_c', 'Unknown')}°C (feels like {current.get('feelslike_c', 'Unknown')}°C)
    💧 Humidity: {current.get('humidity', 'Unknown')}%
    🏔️  Pressure: {current.get('pressure_mb', 'Unknown')} mb
    💨 Wind: {current.get('wind_kph', 'Unknown')} km/h {current.get('wind_dir', '')}
    ☀️  UV Index: {current.get('uv', 'Unknown')}
    👁️  Visibility: {current.get('vis_km', 'Unknown')} km

    🕐 Local Time: {location.get('localtime', 'Unknown')}
    ⏰ Last Updated: {current.get('last_updated', 'Unknown')}
    """
    else:
        return f"""
        Weather for {location_str}:

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


def format_forecast_day(day_forecast: dict, with_emojis: bool = False) -> str:
    """Format a single day's forecast data"""
    date = day_forecast.get("date", "")
    day_data = day_forecast.get("day", {})
    condition = day_data.get("condition", {})
    
    if with_emojis:
        return f"""
        📅 {date}:
        ☁️  Weather: {condition.get('text', 'Unknown')}
        🌡️  Max Temperature: {day_data.get('maxtemp_c', 'Unknown')}°C
        🌡️  Min Temperature: {day_data.get('mintemp_c', 'Unknown')}°C
        🌡️  Avg Temperature: {day_data.get('avgtemp_c', 'Unknown')}°C
        💧 Humidity: {day_data.get('avghumidity', 'Unknown')}%
        💨 Max Wind: {day_data.get('maxwind_kph', 'Unknown')} km/h
        🌧️  Chance of Rain: {day_data.get('daily_chance_of_rain', 'Unknown')}%
        ☀️  UV Index: {day_data.get('uv', 'Unknown')}
        """
    else:
        return f"""
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


async def fetch_weather_data(query: str, endpoint: str = "current", days: int = None) -> dict[str, Any] | None:
    """Generic function to fetch weather data from WeatherAPI"""
    api_error = validate_api_key()
    if api_error:
        return {"error": {"message": api_error}}
    
    if endpoint == "current":
        url = f"{WEATHERAPI_BASE}/current.json?key={WEATHERAPI_KEY}&q={query}&aqi=yes"
    elif endpoint == "forecast":
        days = limit_forecast_days(days or 3)
        url = f"{WEATHERAPI_BASE}/forecast.json?key={WEATHERAPI_KEY}&q={query}&days={days}&aqi=no&alerts=no"
    else:
        return {"error": {"message": "Invalid endpoint"}}
    
    return await make_request(url)


async def get_location_by_ip_api(ip_address: str = None) -> dict[str, Any] | None:
    """Get location information using IP-API service"""
    url = f"http://ip-api.com/json/{ip_address}" if ip_address else "http://ip-api.com/json/"
    data = await make_request(url)
    
    if not data:
        return None
    
    if data.get("status") == "fail":
        logging.error(f"IP location failed: {data.get('message', 'Unknown error')}")
        return None
    
    if data.get("status") == "success":
        return {
            "city": data.get("city"),
            "region": data.get("regionName"), 
            "country": data.get("country"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "timezone": data.get("timezone")
        }
    
    return None


async def get_user_location_by_ip() -> dict[str, Any] | None:
    """
    Get user's approximate location based on their IP address
    """
    return await get_location_by_ip_api()


async def reverse_geocode_coordinates(lat: float, lon: float) -> str | None:
    """
    Convert coordinates to a readable location using a geocoding service
    """
    try:
        # Use a geocoding API to convert coordinates to location
        async with httpx.AsyncClient() as client:
            url = f"https://api.weatherapi.com/v1/search.json?key={WEATHERAPI_KEY}&q={lat},{lon}"
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                location = data[0]
                return f"{location.get('name', '')}, {location.get('region', '')}, {location.get('country', '')}"
            else:
                return f"Location at {lat}, {lon}"
    except Exception as e:
        logging.error(f"Error reverse geocoding: {e}")
        return f"Location at {lat}, {lon}"


# IMPLEMENTATION OF TOOLS
# Tools are functions that can be called by the MCP client


@mcp.tool()
async def get_weather_by_city(city: str) -> str:
    """Get current weather for any city worldwide using WeatherAPI.

    Args:
        city: Name of the city (e.g., "Durgapur", "London", "New York")
    """
    data = await fetch_weather_data(city, "current")

    if not data:
        return f"Unable to fetch weather data for {city}. Please check the city name and ensure you have a valid API key."

    if "error" in data:
        return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

    location = data.get("location", {})
    current = data.get("current", {})
    
    return format_current_weather(location, current).strip()


@mcp.tool()
async def get_weather_forecast_by_city(city: str, days: int = 3) -> str:
    """Get weather forecast for any city worldwide using WeatherAPI.

    Args:
        city: Name of the city (e.g., "Durgapur", "London", "New York")
        days: Number of forecast days (1-10, default is 3)
    """
    data = await fetch_weather_data(city, "forecast", days)

    if not data:
        return f"Unable to fetch forecast data for {city}. Please check the city name and ensure you have a valid API key."

    if "error" in data:
        return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

    location = data.get("location", {})
    forecast = data.get("forecast", {})
    forecast_days = forecast.get("forecastday", [])
    
    if not forecast_days:
        return f"No forecast data available for {city}."
    
    forecasts = [format_forecast_day(day_forecast).strip() for day_forecast in forecast_days]
    
    header = f"{len(forecast_days)}-Day Weather Forecast for {format_location_string(location)}:\n"
    return header + "\n---\n".join(forecasts)


@mcp.tool()
async def get_location_by_ip(ip_address: str) -> str:
    """Get location information based on IP address.

    Args:
        ip_address: IP address of the user (e.g., "8.8.8.8")
    """
    if not ip_address:
        return "IP address is required to fetch location."
    
    data = await get_location_by_ip_api(ip_address)

    if not data:
        return "Unable to fetch location data. Please try again later."

    city = data.get("city", "Unknown city")
    region = data.get("region", "Unknown region")
    country = data.get("country", "Unknown country")
    lat = data.get("lat", "Unknown latitude")
    lon = data.get("lon", "Unknown longitude")
    
    location_info = f"""
        Location information for IP {ip_address}:

        City: {city}
        Region: {region}
        Country: {country}
        Latitude: {lat}
        Longitude: {lon}
    """
    
    return location_info.strip()


@mcp.tool()
async def get_weather_by_coordinates(lat: float, lon: float) -> str:
    """Get current weather for a specific location using coordinates (latitude and longitude).

    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    if lat is None or lon is None:
        return "Latitude and longitude are required to fetch weather."
    
    query = f"{lat},{lon}"
    data = await fetch_weather_data(query, "current")

    if not data:
        return "Unable to fetch weather data. Please try again later."

    if "error" in data:
        return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

    location = data.get("location", {})
    current = data.get("current", {})
    
    return format_current_weather(location, current).strip()


@mcp.tool()
async def get_weather_forecast_by_coordinates(lat: float, lon: float, days: int = 3) -> str:
    """Get weather forecast for a specific location using coordinates (latitude and longitude).

    Args:
        lat: Latitude of the location
        lon: Longitude of the location
        days: Number of forecast days (1-10, default is 3)
    """
    if lat is None or lon is None:
        return "Latitude and longitude are required to fetch forecast."
    
    query = f"{lat},{lon}"
    data = await fetch_weather_data(query, "forecast", days)

    if not data:
        return "Unable to fetch forecast data. Please try again later."

    if "error" in data:
        return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

    location = data.get("location", {})
    forecast = data.get("forecast", {})
    forecast_days = forecast.get("forecastday", [])
    
    if not forecast_days:
        return "No forecast data available for the specified location."
    
    forecasts = [format_forecast_day(day_forecast).strip() for day_forecast in forecast_days]
    
    header = f"{len(forecast_days)}-Day Weather Forecast for {format_location_string(location)}:\n"
    return header + "\n---\n".join(forecasts)


@mcp.tool()
async def get_location_and_weather_by_ip(ip_address: str) -> str:
    """Get location and weather information based on IP address.

    Args:
        ip_address: IP address of the user (e.g., "8.8.8.8")
    """
    if not ip_address:
        return "IP address is required to fetch location and weather."
    
    location_data = await get_location_by_ip_api(ip_address)

    if not location_data:
        return "Unable to fetch location data. Please try again later."

    city = location_data.get("city", "Unknown city")
    region = location_data.get("region", "Unknown region") 
    country = location_data.get("country", "Unknown country")
    lat = location_data.get("lat", "Unknown latitude")
    lon = location_data.get("lon", "Unknown longitude")
    
    # Fetch weather data for the detected location
    weather_info = await get_weather_by_coordinates(lat, lon)
    
    location_info = f"""
        Location information for IP {ip_address}:

        City: {city}
        Region: {region}
        Country: {country}
        Latitude: {lat}
        Longitude: {lon}
    """
    
    return location_info.strip() + "\n\n" + weather_info


@mcp.tool()
async def get_user_current_location() -> str:
    """Get the user's current approximate location based on their IP address.
    
    This tool attempts to detect the user's location using their IP address.
    Note: This provides approximate location and may not be 100% accurate.
    
    Returns:
        A string describing the user's approximate location and coordinates
    """
    location_data = await get_user_location_by_ip()
    
    if not location_data:
        return "❌ Sorry, I couldn't determine your current location. This might be due to network restrictions or VPN usage."
    
    city = location_data.get("city", "Unknown")
    region = location_data.get("region", "")
    country = location_data.get("country", "Unknown")
    lat = location_data.get("lat")
    lon = location_data.get("lon")
    timezone = location_data.get("timezone", "Unknown")
    
    location_info = f"""
    📍 Your Current Location (approximate):
    
    🏙️  City: {city}
    🗺️  Region: {region}
    🌍 Country: {country}
    📐 Coordinates: {lat}, {lon}
    🕐 Timezone: {timezone}
    
    💡 Note: This location is detected using your IP address and may not be completely accurate.
    If you're using a VPN, the location might show where your VPN server is located.
    """
    
    return location_info.strip()


@mcp.tool()
async def get_weather_at_current_location() -> str:
    """Get current weather at the user's detected location.
    
    This tool combines location detection with weather fetching to provide
    weather information for the user's current approximate location.
    
    Returns:
        Current weather information for the user's detected location
    """
    location_data = await get_user_location_by_ip()
    
    if not location_data:
        return "❌ Sorry, I couldn't determine your current location to get the weather. You can ask for weather in a specific city instead!"
    
    city = location_data.get("city")
    lat = location_data.get("lat")
    lon = location_data.get("lon")
    
    if not city and (lat is None or lon is None):
        return "❌ Could not determine a valid location for weather lookup."
    
    # Use city name if available, otherwise use coordinates
    query = city if city else f"{lat},{lon}"
    
    data = await fetch_weather_data(query, "current")

    if not data:
        return f"Unable to fetch weather data for your current location ({query}). Please try asking for weather in a specific city."

    if "error" in data:
        return f"Error getting weather for your location: {data['error'].get('message', 'Unknown error occurred')}"

    location = data.get("location", {})
    current = data.get("current", {})
    
    weather_info = format_current_weather(location, current, with_emojis=True)
    
    return weather_info.strip() + "\n\n💡 Location detected via IP address - may be approximate"


@mcp.tool()
async def get_forecast_at_current_location(days: int = 3) -> str:
    """Get weather forecast at the user's detected location.
    
    Args:
        days: Number of forecast days (1-3, default is 3)
    
    Returns:
        Weather forecast for the user's detected location
    """
    return await WeatherService.get_forecast_at_current_location(days)
