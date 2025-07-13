"""
Weather Service Module

Handles weather-related operations and data processing.
"""

from src.services import fetch_weather_data
from src.utils import format_current_weather, format_forecast_day, format_location_string


class WeatherService:
    """Service class for weather operations"""
    
    @staticmethod
    async def get_current_weather(query: str, with_emojis: bool = False) -> str:
        """
        Get current weather for a location
        
        Args:
            query: Location query (city name or coordinates)
            with_emojis: Whether to format with emojis
            
        Returns:
            Formatted weather information string
        """
        data = await fetch_weather_data(query, "current")

        if not data:
            return f"Unable to fetch weather data for {query}. Please check the location and ensure you have a valid API key."

        if "error" in data:
            return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

        location = data.get("location", {})
        current = data.get("current", {})
        
        return format_current_weather(location, current, with_emojis).strip()
    
    @staticmethod
    async def get_weather_forecast(query: str, days: int = 3, with_emojis: bool = False) -> str:
        """
        Get weather forecast for a location
        
        Args:
            query: Location query (city name or coordinates)
            days: Number of forecast days
            with_emojis: Whether to format with emojis
            
        Returns:
            Formatted forecast information string
        """
        data = await fetch_weather_data(query, "forecast", days)

        if not data:
            return f"Unable to fetch forecast data for {query}. Please check the location and ensure you have a valid API key."

        if "error" in data:
            return f"Error: {data['error'].get('message', 'Unknown error occurred')}"

        location = data.get("location", {})
        forecast = data.get("forecast", {})
        forecast_days = forecast.get("forecastday", [])
        
        if not forecast_days:
            return f"No forecast data available for {query}."
        
        forecasts = [format_forecast_day(day_forecast, with_emojis).strip() for day_forecast in forecast_days]
        
        header = f"{len(forecast_days)}-Day Weather Forecast for {format_location_string(location)}:\\n"
        return header + "\\n---\\n".join(forecasts)
    
    @staticmethod
    async def get_weather_by_coordinates(lat: float, lon: float, with_emojis: bool = False) -> str:
        """
        Get current weather by coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            with_emojis: Whether to format with emojis
            
        Returns:
            Formatted weather information string
        """
        if lat is None or lon is None:
            return "Latitude and longitude are required to fetch weather."
        
        query = f"{lat},{lon}"
        return await WeatherService.get_current_weather(query, with_emojis)
    
    @staticmethod
    async def get_forecast_by_coordinates(lat: float, lon: float, days: int = 3, with_emojis: bool = False) -> str:
        """
        Get weather forecast by coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Number of forecast days
            with_emojis: Whether to format with emojis
            
        Returns:
            Formatted forecast information string
        """
        if lat is None or lon is None:
            return "Latitude and longitude are required to fetch forecast."
        
        query = f"{lat},{lon}"
        return await WeatherService.get_weather_forecast(query, days, with_emojis)
    
    @staticmethod
    async def get_weather_at_current_location() -> str:
        """
        Get current weather at user's detected location
        
        Returns:
            Formatted weather information string
        """
        from .location_service import LocationService
        
        location_data = await LocationService.get_user_location()
        
        if not location_data:
            return "❌ Sorry, I couldn't determine your current location to get the weather. You can ask for weather in a specific city instead!"
        
        city = location_data.get("city")
        lat = location_data.get("lat")
        lon = location_data.get("lon")
        
        if not city and (lat is None or lon is None):
            return "❌ Could not determine a valid location for weather lookup."
        
        # Use city name if available, otherwise use coordinates
        query = city if city else f"{lat},{lon}"
        
        weather_info = await WeatherService.get_current_weather(query, with_emojis=True)
        
        return weather_info + "\n\n💡 Location detected via IP address - may be approximate"
    
    @staticmethod
    async def get_forecast_at_current_location(days: int = 3) -> str:
        """
        Get weather forecast at user's detected location
        
        Args:
            days: Number of forecast days (1-3, default is 3)
        
        Returns:
            Formatted forecast information string
        """
        from .location_service import LocationService
        
        location_data = await LocationService.get_user_location()
        
        if not location_data:
            return "❌ Sorry, I couldn't determine your current location to get the forecast. You can ask for forecast in a specific city instead!"
        
        city = location_data.get("city")
        lat = location_data.get("lat")
        lon = location_data.get("lon")
        
        if not city and (lat is None or lon is None):
            return "❌ Could not determine a valid location for weather lookup."
        
        # Use city name if available, otherwise use coordinates
        query = city if city else f"{lat},{lon}"
        
        forecast_info = await WeatherService.get_weather_forecast(query, days, with_emojis=True)
        
        # Customize the header for current location
        if "Weather Forecast for" in forecast_info:
            lines = forecast_info.split("\n", 1)
            if len(lines) > 1:
                # Replace the header with current location version
                location_part = lines[0].split("for ", 1)[-1].rstrip(":")
                new_header = f"🌟 {days}-Day Weather Forecast for Your Location:\n📍 {location_part}:\n\n💡 Location detected via IP address - may be approximate\n"
                forecast_info = new_header + "\n" + "─" * 50 + lines[1]
        
        return forecast_info
