"""
API Service Module

Handles all HTTP requests and API communications.
"""

import httpx
import logging
from typing import Any, Dict, Optional
from src import config


async def make_request(url: str, headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
    """
    Make a request to any API endpoint
    
    Args:
        url: The URL to make the request to
        headers: Optional headers to include in the request
        
    Returns:
        JSON response data or None if request failed
    """
    default_headers = {"User-Agent": config.user_agent}
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


async def fetch_weather_data(query: str, endpoint: str = "current", days: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """
    Generic function to fetch weather data from WeatherAPI
    
    Args:
        query: Location query (city name or coordinates)
        endpoint: API endpoint ('current' or 'forecast')
        days: Number of forecast days (for forecast endpoint)
        
    Returns:
        Weather data or error response
    """
    from ..utils.validators import validate_api_key, limit_forecast_days
    
    api_error = validate_api_key(config.weatherapi_key)
    if api_error:
        return {"error": {"message": api_error}}
    
    if endpoint == "current":
        url = f"{config.weatherapi_base}/current.json?key={config.weatherapi_key}&q={query}&aqi=yes"
    elif endpoint == "forecast":
        days = limit_forecast_days(days or 3)
        url = f"{config.weatherapi_base}/forecast.json?key={config.weatherapi_key}&q={query}&days={days}&aqi=no&alerts=no"
    else:
        return {"error": {"message": "Invalid endpoint"}}
    
    return await make_request(url)


