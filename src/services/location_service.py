"""
Location Service Module

Handles location detection and geographic operations.
"""

import httpx
import logging
from typing import Dict, Any, Optional
from src import config
from src.utils import format_location_info, format_current_location_info


class LocationService:
    """Service class for location operations"""
    
    @staticmethod
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

    @staticmethod
    async def fetch_ip_location(ip_address: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get location information using IP-API service
        
        Args:
            ip_address: IP address to lookup (if None, uses current IP)
            
        Returns:
            Location data or None if failed
        """
        url = f"http://ip-api.com/json/{ip_address}" if ip_address else "http://ip-api.com/json/"
        data = await LocationService.make_request(url)
        
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

    @staticmethod
    async def reverse_geocode_coordinates(lat: float, lon: float) -> Optional[str]:
        """
        Convert coordinates to a readable location using WeatherAPI geocoding
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Formatted location string or fallback coordinates
        """
        try:
            url = f"{config.weatherapi_base}/search.json?key={config.weatherapi_key}&q={lat},{lon}"
            data = await LocationService.make_request(url)
            
            if data and len(data) > 0:
                location = data[0]
                return f"{location.get('name', '')}, {location.get('region', '')}, {location.get('country', '')}"
            else:
                return f"Location at {lat}, {lon}"
        except Exception as e:
            logging.error(f"Error reverse geocoding: {e}")
            return f"Location at {lat}, {lon}"

    @staticmethod
    async def get_user_location() -> Optional[Dict[str, Any]]:
        """
        Get user's approximate location based on their IP address
        
        Returns:
            Location data dictionary or None if failed
        """
        return await LocationService.fetch_ip_location()

    @staticmethod
    async def get_location_by_ip(ip_address: str) -> str:
        """
        Get location information for a specific IP address
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Formatted location information string
        """
        if not ip_address:
            return "IP address is required to fetch location."
        
        data = await LocationService.fetch_ip_location(ip_address)

        if not data:
            return "Unable to fetch location data. Please try again later."

        return format_location_info(ip_address, data).strip()

    @staticmethod
    async def get_current_location_info() -> str:
        """
        Get formatted current location information with emojis
        
        Returns:
            Formatted location information string
        """
        location_data = await LocationService.get_user_location()
        
        if not location_data:
            return "❌ Sorry, I couldn't determine your current location. This might be due to network restrictions or VPN usage."
        
        return format_current_location_info(location_data).strip()

    @staticmethod
    async def reverse_geocode(lat: float, lon: float) -> Optional[str]:
        """
        Convert coordinates to a readable location
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Formatted location string or None if failed
        """
        return await LocationService.reverse_geocode_coordinates(lat, lon)
