#!/usr/bin/env python3
"""
BusinessMap MCP Server

A Model Context Protocol server for integrating with BusinessMap (formerly Kanbanize).
Provides tools to interact with boards, cards, and users.
"""

import os
import sys
import logging

from mcp.server.fastmcp import FastMCP

from businessmap_tools import register_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("BusinessMap")

# Register all tools
register_tools(mcp)

if __name__ == "__main__":
    import sys
    
    # Check if environment variables are set
    if not os.getenv("BUSINESSMAP_SUBDOMAIN") or not os.getenv("BUSINESSMAP_API_KEY"):
        print("Error: BUSINESSMAP_SUBDOMAIN and BUSINESSMAP_API_KEY environment variables must be set")
        sys.exit(1)
    
    # Run the MCP server
    mcp.run()