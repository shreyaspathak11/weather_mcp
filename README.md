# Weather MCP Server

A **Model Context Protocol (MCP) server** that provides AI assistants and applications with real-time weather information and forecasts for any location worldwide. This server acts as a bridge between AI models and weather APIs, allowing them to fetch current weather conditions, forecasts, and location-based weather data.

## What is MCP?

**Model Context Protocol (MCP)** is a standard that allows AI assistants to connect to external data sources and tools. This weather MCP server:

🤖 **Connects AI to Weather Data**: Enables AI assistants like Claude, ChatGPT, or any MCP-compatible application to access weather information  
🌍 **Real-time Weather Access**: Provides current weather conditions and forecasts for any city or coordinates worldwide  
📍 **Smart Location Detection**: Automatically detects user location via IP address for personalized weather data  
⚡ **Instant Responses**: Fast, reliable weather data formatted for AI consumption  

## Features

✨ **Current Weather**: Get real-time weather for any city worldwide  
📅 **Weather Forecasts**: Multi-day weather forecasts (up to 3 days)  
📍 **Auto Location**: Automatic location detection via IP address  
🌐 **Coordinate Support**: Weather lookup by latitude/longitude  
🎯 **User-Friendly**: Weather data formatted with emojis and clear descriptions  
⚡ **High Performance**: Built with async/await for fast responses  

## How It Works

1. **AI Assistant Request**: An AI assistant needs weather information for a user
2. **MCP Connection**: The assistant connects to this weather MCP server
3. **Tool Execution**: The server fetches real-time weather data from WeatherAPI
4. **Formatted Response**: Weather information is returned in a user-friendly format
5. **AI Integration**: The assistant uses this data to provide helpful weather insights

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/shreyaspathak11/weather_mcp.git
cd weather_mcp

# Install dependencies
pip install -r requirements_modular.txt
```

### 2. Configuration

Create a `.env` file in the project root:
```bash
WEATHERAPI_KEY=your_api_key_here
```

Or set the environment variable:
```bash
export WEATHERAPI_KEY="your_api_key_here"
```

> **Note**: A default API key is included for testing, but get your own free key from [WeatherAPI.com](https://www.weatherapi.com/) for production use.

### 3. Running the Server

```bash
# Start the MCP server
python server.py
```

The server will start and be ready to handle MCP requests from AI assistants.

## Available Weather Tools

This MCP server provides the following tools that AI assistants can use:

### 🏙️ Weather by City
- **`get_weather_by_city(city)`** - Get current weather for any city
  ```
  Example: get_weather_by_city("London") 
  Returns: Current temperature, conditions, humidity, wind, etc.
  ```

- **`get_weather_forecast_by_city(city, days)`** - Get multi-day forecast
  ```
  Example: get_weather_forecast_by_city("New York", 3)
  Returns: 3-day forecast with daily highs, lows, conditions
  ```

### 📍 Weather by Coordinates
- **`get_weather_by_coordinates(lat, lon)`** - Weather for exact coordinates
  ```
  Example: get_weather_by_coordinates(40.7128, -74.0060)
  Returns: Weather for precise latitude/longitude
  ```

- **`get_weather_forecast_by_coordinates(lat, lon, days)`** - Forecast by coordinates
  ```
  Example: get_weather_forecast_by_coordinates(35.6762, 139.6503, 2)
  Returns: 2-day forecast for Tokyo coordinates
  ```

### 🎯 Smart Location Detection
- **`get_weather_at_current_location()`** - Weather for user's detected location
  ```
  Automatically detects user location via IP and returns weather
  Includes emoji formatting and location disclaimer
  ```

- **`get_forecast_at_current_location(days)`** - Forecast for detected location
  ```
  Multi-day forecast for user's approximate location
  ```

### 🌐 Location Services
- **`get_user_current_location()`** - Get user's approximate location
  ```
  Returns city, region, country, coordinates, timezone
  ```

- **`get_location_by_ip(ip_address)`** - Location info for specific IP
  ```
  Example: get_location_by_ip("8.8.8.8")
  Returns: Geographic information for the IP address
  ```

- **`get_location_and_weather_by_ip(ip_address)`** - Combined location + weather
  ```
  Get both location details and current weather for an IP
  ```

## Example AI Interactions

### Simple Weather Query
```
User: "What's the weather like in Tokyo?"
AI uses: get_weather_by_city("Tokyo")
Response: "Tokyo is currently 22°C with partly cloudy skies..."
```

### Location-Aware Weather
```
User: "How's the weather where I am?"
AI uses: get_weather_at_current_location()
Response: "🌟 Weather at Your Current Location: 📍 New York, NY, US..."
```

### Planning Assistance
```
User: "Will it rain in London this weekend?"
AI uses: get_weather_forecast_by_city("London", 3)
Response: "Here's the 3-day forecast for London..."
```

## Installation & Setup

### 1. Install Dependencies
```bash
# Install the package and dependencies
pip install -e .
```

### 2. Configure API Key
Create a `.env` file in the root directory:
```env
WEATHERAPI_KEY=your_api_key_here
```

> Get your free API key from [WeatherAPI.com](https://www.weatherapi.com/) - supports 1 million calls/month on the free tier.

### 3. Run the MCP Server
```bash
# Start the server (listens for MCP connections)
python server.py
```

## MCP Integration

### For AI Applications
Connect your AI assistant to this server to enable weather capabilities:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["path/to/weather/server.py"],
      "env": {
        "WEATHERAPI_KEY": "your_api_key"
      }
    }
  }
}
```

### For Claude Desktop
Add to your Claude configuration to give Claude weather abilities:

```json
{
  "weather": {
    "command": "python",
    "args": ["d:/AI Projects/weather/server.py"]
  }
}
```

Once connected, Claude can answer questions like:
- "What's the weather in Paris?"
- "Will it rain tomorrow in my location?"
- "What's the forecast for this weekend?"

## Technical Requirements

- **Python 3.8+**: Required minimum version
- **Dependencies**: httpx, mcp, python-dotenv
- **APIs**: WeatherAPI.com (primary), IP-API.com (location detection)
- **Error Handling**: Comprehensive API failure protection

## License

This project is open source and available under the MIT License.

---

**🌤️ Empowering AI assistants with real-time weather intelligence**
