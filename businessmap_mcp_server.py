#!/usr/bin/env python3
"""
BusinessMap MCP Server

A Model Context Protocol server for integrating with BusinessMap (formerly Kanbanize).
Provides tools to interact with boards, cards, and users.
"""

import logging
import os
import sys

from mcp.server.fastmcp import FastMCP

from src.tools import register_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("BusinessMap")

register_tools(mcp)

if __name__ == "__main__":
    if not os.getenv("BUSINESSMAP_SUBDOMAIN") or not os.getenv("BUSINESSMAP_API_KEY"):
        print("Error: BUSINESSMAP_SUBDOMAIN and BUSINESSMAP_API_KEY environment variables must be set")
        sys.exit(1)

    mcp.run()
