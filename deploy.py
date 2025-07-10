import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from weather import mcp, get_weather_by_city, get_weather_forecast_by_city

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Create FastAPI app for HTTP endpoints
app = FastAPI(
    title="Weather MCP Server", 
    version="1.0.0",
    description="MCP server providing weather information and forecasts"
)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy", "service": "weather-mcp-server"})

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return JSONResponse({
        "name": "Weather MCP Server",
        "version": "1.0.0",
        "description": "MCP server providing weather information and forecasts",
        "tools": ["get_weather_by_city", "get_weather_forecast_by_city"],
        "mcp_endpoint": "Use this server with MCP-compatible clients",
        "claude_desktop_config": {
            "instructions": "Add this server to Claude Desktop using the deployment URL",
            "note": "This server provides weather data for travel planning and general weather inquiries"
        }
    })

@app.get("/weather/{city}")
async def get_weather_api(city: str):
    """HTTP endpoint for getting weather data"""
    result = await get_weather_by_city(city)
    return JSONResponse({"city": city, "weather": result})

@app.get("/forecast/{city}")
async def get_forecast_api(city: str, days: int = 3):
    """HTTP endpoint for getting weather forecast"""
    result = await get_weather_forecast_by_city(city, days)
    return JSONResponse({"city": city, "forecast": result, "days": days})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"Starting Weather MCP Server on {host}:{port}")
    print("Available endpoints:")
    print(f"  - Health check: http://{host}:{port}/health")
    print(f"  - Service info: http://{host}:{port}/")
    print(f"  - Weather API: http://{host}:{port}/weather/{{city}}")
    print(f"  - Forecast API: http://{host}:{port}/forecast/{{city}}")
    
    uvicorn.run(app, host=host, port=port, reload=debug)
