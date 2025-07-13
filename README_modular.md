# Weather MCP Server - Modular Architecture

This is a refactored version of the Weather MCP Server with a clean, modular architecture that separates concerns and improves maintainability.

## Architecture

```
weather/
├── src/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── api_service.py      # HTTP requests and API communications
│   │   ├── weather_service.py  # Weather data processing
│   │   └── location_service.py # Location detection and operations
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py       # Validation functions
│   │   └── formatters.py       # Data formatting functions
│   └── __init__.py
├── server_modular.py           # Main MCP server using modular structure
├── server.py                   # Original monolithic server (for comparison)
├── requirements_modular.txt    # Dependencies for modular version
└── README_modular.md          # This file
```

## Modules Description

### Services Layer

#### `api_service.py`
- **Purpose**: Handles all HTTP requests and API communications
- **Functions**:
  - `make_request()`: Generic HTTP request handler
  - `fetch_weather_data()`: WeatherAPI data fetching
  - `fetch_ip_location()`: IP-based location detection
  - `reverse_geocode_coordinates()`: Coordinate to location conversion

#### `weather_service.py`
- **Purpose**: Processes weather data and provides weather operations
- **Class**: `WeatherService` with static methods:
  - `get_current_weather()`: Current weather for any location
  - `get_weather_forecast()`: Multi-day forecast
  - `get_weather_by_coordinates()`: Weather by lat/lon
  - `get_forecast_by_coordinates()`: Forecast by lat/lon

#### `location_service.py`
- **Purpose**: Manages location detection and geographic operations
- **Class**: `LocationService` with static methods:
  - `get_user_location()`: User's IP-based location
  - `get_location_by_ip()`: Location for specific IP
  - `get_current_location_info()`: Formatted current location
  - `reverse_geocode()`: Coordinates to readable location

### Utils Layer

#### `validators.py`
- **Purpose**: Input validation and data constraints
- **Functions**:
  - `validate_api_key()`: API key validation
  - `limit_forecast_days()`: Enforce forecast day limits

#### `formatters.py`
- **Purpose**: Data formatting and presentation
- **Functions**:
  - `format_location_string()`: Location display formatting
  - `format_current_weather()`: Current weather formatting
  - `format_forecast_day()`: Forecast day formatting
  - `format_location_info()`: IP location info formatting
  - `format_current_location_info()`: Current location with emojis

## Benefits of Modular Architecture

### 1. **Separation of Concerns**
- Each module has a single, well-defined responsibility
- API communication is separated from data processing
- Formatting is separated from business logic

### 2. **Improved Maintainability**
- Changes to formatting don't affect API logic
- New weather services can be added without touching location code
- Bug fixes are isolated to specific modules

### 3. **Better Testability**
- Each module can be unit tested independently
- Mock dependencies easily for testing
- Clear interfaces between components

### 4. **Code Reusability**
- Utility functions can be used across different services
- Common formatting patterns are centralized
- API service can be extended for other weather providers

### 5. **Scalability**
- Easy to add new weather data sources
- Simple to implement caching at the service layer
- Clear path for adding new location providers

## Usage

### Running the Modular Server

```bash
python server_modular.py
```

### Environment Variables

Set your WeatherAPI key:
```bash
export WEATHERAPI_KEY="your_api_key_here"
```

### Available Tools

The modular server provides the same MCP tools as the original:

- `get_weather_by_city(city: str)`
- `get_weather_forecast_by_city(city: str, days: int = 3)`
- `get_location_by_ip(ip_address: str)`
- `get_weather_by_coordinates(lat: float, lon: float)`
- `get_weather_forecast_by_coordinates(lat: float, lon: float, days: int = 3)`
- `get_location_and_weather_by_ip(ip_address: str)`
- `get_user_current_location()`
- `get_weather_at_current_location()`
- `get_forecast_at_current_location(days: int = 3)`

## Dependencies

Install dependencies:
```bash
pip install -r requirements_modular.txt
```

## Code Quality Improvements

### Before (Monolithic)
- 600+ lines in single file
- Duplicate code for API requests
- Repeated formatting logic
- Mixed concerns (API + formatting + validation)

### After (Modular)
- Clean separation into focused modules
- Reusable components
- DRY (Don't Repeat Yourself) principles
- Single Responsibility Principle
- Easy to extend and maintain

## Future Enhancements

The modular structure makes it easy to add:

1. **Caching Layer**: Add caching service for API responses
2. **Multiple Weather Providers**: Support for additional weather APIs
3. **Database Integration**: Store location preferences and history
4. **Configuration Management**: Centralized config handling
5. **Logging Service**: Structured logging across all modules
6. **Rate Limiting**: API rate limit management
7. **Health Checks**: Service health monitoring

This architecture provides a solid foundation for building a production-ready weather service with proper separation of concerns and maintainable code structure.
