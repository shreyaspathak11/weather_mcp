import os
import dotenv


class Config:
    """Configuration class for Weather MCP Server"""
    
    def __init__(self):
        dotenv.load_dotenv()
        
    @classmethod
    def load(cls):
        """Load configuration and return instance"""
        return cls()
    
    @property
    def weatherapi_key(self) -> str:
        """Get WeatherAPI key from environment"""
        return os.getenv("WEATHERAPI_KEY")
    
    @property
    def weatherapi_base(self) -> str:
        """Get WeatherAPI base URL"""
        return "https://api.weatherapi.com/v1"
    
    @property
    def user_agent(self) -> str:
        """Get user agent string"""
        return "weather-app/1.0"


# Global config instance
config = Config.load()
