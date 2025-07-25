#!/bin/bash

# Setup script for BusinessMap MCP Server
# Uses uv to manage dependencies in isolation

echo "Setting up BusinessMap MCP Server..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Initialize uv project
echo "Initializing uv project..."
uv init --no-readme

# Add dependencies
echo "Adding dependencies..."
uv add "mcp>=1.0.0"
uv add "requests>=2.31.0" 
uv add "pydantic>=2.0.0"

echo "Setup complete!"
echo ""
echo "To test the server:"
echo "export BUSINESSMAP_SUBDOMAIN='YOUR_SUBDOMAIN_HERE'"
echo "export BUSINESSMAP_API_KEY='your-api-key'"
echo "uv run python businessmap_mcp_server.py"