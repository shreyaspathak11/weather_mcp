"""
Validators Module

Contains validation functions and utilities.
"""

from typing import Optional


def validate_api_key(api_key: Optional[str]) -> Optional[str]:
    """
    Validate that WeatherAPI key is available
    
    Args:
        api_key: The API key to validate
        
    Returns:
        Error message if invalid, None if valid
    """
    if not api_key:
        return "Error: WEATHERAPI_KEY environment variable is not set. Please get an API key from weatherapi.com and add it to your .env file."
    return None


def limit_forecast_days(days: int) -> int:
    """
    Limit forecast days to WeatherAPI's free tier limit
    
    Args:
        days: Requested number of days
        
    Returns:
        Limited number of days (1-3)
    """
    return min(max(days, 1), 3)  # Free tier allows up to 3 days
