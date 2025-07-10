# Weather MCP Server

A Model Context Protocol (MCP) server that provides real-time weather information and forecasts for cities worldwide using the WeatherAPI service.

## Features

- **Current Weather**: Get real-time weather conditions for any city
- **Weather Forecast**: Get up to 3-day weather forecasts
- **Global Coverage**: Works with cities worldwide
- **Detailed Information**: Includes temperature, humidity, wind, UV index, and more
- **Travel Planning**: Helps with weather-based travel decisions

## Example Use Case

**Question**: "I am at Durgapur, tell me if I can travel to Kolkata without worrying about rain?"

**Response**: Let me check the current weather conditions in both Durgapur and Kolkata to help you plan your travel.

### Weather Analysis Results

**Current situation**: There are thundery outbreaks near Durgapur, and both cities have high humidity (91-94%) with misty/overcast conditions.

**Today and tomorrow**: Both cities are forecasted to have moderate rain with very high chances of precipitation (85-92%). The journey between Durgapur and Kolkata will likely involve encountering rain.

### Travel Recommendations

- 🌂 Carry an umbrella and waterproof clothing
- 🚗 If traveling by road, drive carefully due to reduced visibility and wet roads
- ⏰ Allow extra time for your journey as rain may cause delays
- 🚌 Check train/bus schedules as they might be affected by weather

**Conclusion**: While you can certainly travel, I'd suggest being well-prepared for wet conditions rather than traveling without rain concerns. If your travel is flexible, you might want to monitor the weather for a day or two to see if conditions improve.

## Installation

1. Clone this repository
2. Install dependencies using UV (recommended) or pip:

```bash
# Create virtual enviroment and run
uv venv
.venv\Scripts\activate

# Install dependencies
uv add mcp[cli] httpx

```

3. Set up your WeatherAPI key:
   - Get a free API key from [WeatherAPI.com](https://www.weatherapi.com/)
   - Set the environment variable:
     ```bash
     WEATHERAPI_KEY=your_api_key_here
     ```

## Usage

### Running the MCP Server

```bash
code $env:AppData\Claude\claude_desktop_config.json
```
Add following to the file

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "D:/YOUR/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ],
      "env": {
        "WEATHERAPI_KEY": "your-api-key"
      }
    }
  }
}
```
### Available Tools

#### 1. `get_weather_by_city(city: str)`
Get current weather conditions for any city.

**Parameters:**
- `city`: Name of the city (e.g., "Durgapur", "London", "New York")

**Example Response:**
```
Weather for Durgapur, West Bengal, India:

Current Conditions: Partly cloudy
Temperature: 28°C (feels like 32°C)
Humidity: 78%
Pressure: 1012 mb
Wind: 15 km/h NE
UV Index: 6
Visibility: 10 km

Local Time: 2025-07-11 14:30
Last Updated: 2025-07-11 14:15
```

#### 2. `get_weather_forecast_by_city(city: str, days: int = 3)`
Get weather forecast for any city.

**Parameters:**
- `city`: Name of the city
- `days`: Number of forecast days (1-3, default is 3)

**Example Response:**
```
3-Day Weather Forecast for Kolkata, West Bengal, India:

2025-07-11:
Weather: Moderate rain
Max Temperature: 30°C
Min Temperature: 25°C
Avg Temperature: 27°C
Humidity: 85%
Max Wind: 20 km/h
Chance of Rain: 90%
UV Index: 4
---
2025-07-12:
Weather: Light rain
Max Temperature: 29°C
Min Temperature: 24°C
Avg Temperature: 26°C
Humidity: 82%
Max Wind: 18 km/h
Chance of Rain: 75%
UV Index: 5
```

## Project Structure

```
weather/
├── main.py              # Entry point for the MCP server
├── weather.py           # Main weather functionality and M
├── pyproject.toml       # Project configuration and 
├── uv.lock              # UV lock file for dependency 
└── README.md            # This file
```

## Dependencies

- **httpx**: For making HTTP requests to weather APIs
- **mcp**: Model Context Protocol framework
- **Python 3.13+**: Required Python version

## API Information

This project uses [WeatherAPI.com](https://www.weatherapi.com/) which provides:
- Current weather conditions
- Weather forecasts
- Global city coverage
- Free tier with up to 1,000 calls/month

## Error Handling

The server includes comprehensive error handling for:
- Invalid city names
- API key issues
- Network connectivity problems
- Rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the WeatherAPI documentation
- Ensure your API key is properly set
- Verify city names are spelled correctly
- Check your internet connection

---

*Built with Model Context Protocol (MCP) for seamless integration with AI assistants.*