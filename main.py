import sys
import os
from weather import mcp

if __name__ == "__main__":
    # Check if we're running in deployment mode
    if "--deploy" in sys.argv or os.getenv("DEPLOYMENT_MODE") == "true":
        # Import and run HTTP server for deployment
        from deploy import app
        import uvicorn
        
        port = int(os.getenv("PORT", 8000))
        host = os.getenv("HOST", "0.0.0.0")
        print(f"Starting Weather MCP Server in deployment mode on {host}:{port}")
        uvicorn.run(app, host=host, port=port)
    else:
        # Run in MCP mode for local/desktop use
        print("Weather MCP Server Running...")
        mcp.run()