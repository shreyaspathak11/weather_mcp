"""
Formatters Module

Contains formatting functions for weather data and locations.
"""

from typing import Dict, Any


def format_location_string(location: Dict[str, Any]) -> str:
    """
    Format location data into a readable string
    
    Args:
        location: Location data dictionary
        
    Returns:
        Formatted location string
    """
    name = location.get('name', 'Unknown location')
    region = location.get('region', '')
    country = location.get('country', '')
    
    if region:
        return f"{name}, {region}, {country}"
    return f"{name}, {country}"


def format_current_weather(location: Dict[str, Any], current: Dict[str, Any], with_emojis: bool = False) -> str:
    """
    Format current weather data into a readable string
    
    Args:
        location: Location data dictionary
        current: Current weather data dictionary
        with_emojis: Whether to include emojis in the output
        
    Returns:
        Formatted weather information string
    """
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


def format_forecast_day(day_forecast: Dict[str, Any], with_emojis: bool = False) -> str:
    """
    Format a single day's forecast data
    
    Args:
        day_forecast: Single day forecast data dictionary
        with_emojis: Whether to include emojis in the output
        
    Returns:
        Formatted forecast day string
    """
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


def format_location_info(ip_address: str, location_data: Dict[str, Any]) -> str:
    """
    Format location information for display
    
    Args:
        ip_address: IP address that was looked up
        location_data: Location data dictionary
        
    Returns:
        Formatted location information string
    """
    city = location_data.get("city", "Unknown city")
    region = location_data.get("region", "Unknown region")
    country = location_data.get("country", "Unknown country")
    lat = location_data.get("lat", "Unknown latitude")
    lon = location_data.get("lon", "Unknown longitude")
    
    return f"""
        Location information for IP {ip_address}:

        City: {city}
        Region: {region}
        Country: {country}
        Latitude: {lat}
        Longitude: {lon}
    """


def format_current_location_info(location_data: Dict[str, Any]) -> str:
    """
    Format current location information with emojis
    
    Args:
        location_data: Location data dictionary
        
    Returns:
        Formatted location information string with emojis
    """
    city = location_data.get("city", "Unknown")
    region = location_data.get("region", "")
    country = location_data.get("country", "Unknown")
    lat = location_data.get("lat")
    lon = location_data.get("lon")
    timezone = location_data.get("timezone", "Unknown")
    
    return f"""
    📍 Your Current Location (approximate):
    
    🏙️  City: {city}
    🗺️  Region: {region}
    🌍 Country: {country}
    📐 Coordinates: {lat}, {lon}
    🕐 Timezone: {timezone}
    
    💡 Note: This location is detected using your IP address and may not be completely accurate.
    If you're using a VPN, the location might show where your VPN server is located.
    """
