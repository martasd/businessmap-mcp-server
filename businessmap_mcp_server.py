#!/usr/bin/env python3
"""
BusinessMap MCP Server

A Model Context Protocol server for integrating with BusinessMap (formerly Kanbanize).
Provides tools to interact with boards, cards, and users.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import requests
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("BusinessMap")

class BusinessmapMcpServer:
    """Client for interacting with BusinessMap API"""
    
    def __init__(self, subdomain: str, api_key: str):
        self.base_url = f"https://{subdomain}.kanbanize.com/api/v2"
        self.headers = {
            "Accept": "application/json",
            "apikey": api_key
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to BusinessMap API"""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_workspaces(self) -> List[Dict[str, Any]]:
        """Get all workspaces"""
        result = self._make_request("GET", "/workspaces")
        return result.get("data", [])
    
    def get_boards(self) -> List[Dict[str, Any]]:
        """Get all boards"""
        result = self._make_request("GET", "/boards")
        return result.get("data", [])
    
    def get_cards(self, board_id: Optional[int] = None, limit: int = 50) -> Dict[str, Any]:
        """Get cards, optionally filtered by board"""
        params = {"limit": limit}
        if board_id:
            params["board_id"] = board_id
        
        result = self._make_request("GET", "/cards", params=params)
        return result.get("data", {})
    
    def get_card(self, card_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific card"""
        result = self._make_request("GET", f"/cards/{card_id}")
        return result.get("data", {})
    
    def search_cards(self, query: str, board_id: Optional[int] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Search cards by title or description"""
        cards_data = self.get_cards(board_id, limit=200)  # Get more cards for search
        cards = cards_data.get("data", [])
        
        # Simple text search in title and description
        matching_cards = []
        query_lower = query.lower()
        
        for card in cards:
            title_match = query_lower in card.get("title", "").lower()
            # We'd need to get full card details to search description
            if title_match:
                matching_cards.append(card)
            
            if len(matching_cards) >= limit:
                break
        
        return matching_cards
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        result = self._make_request("GET", "/users")
        return result.get("data", [])
    
    def create_card(self, board_id: int, title: str, description: str = "", **kwargs) -> Dict[str, Any]:
        """Create a new card"""
        data = {
            "board_id": board_id,
            "title": title,
            "description": description,
            **kwargs
        }
        result = self._make_request("POST", "/cards", json=data)
        return result.get("data", {})
    
    def update_card(self, card_id: int, **kwargs) -> Dict[str, Any]:
        """Update an existing card"""
        result = self._make_request("PATCH", f"/cards/{card_id}", json=kwargs)
        return result.get("data", {})

# Initialize BusinessMap client (will be set from environment)
client: Optional[BusinessmapMcpServer] = None

def get_client() -> BusinessmapMcpServer:
    """Get or initialize the BusinessMap client"""
    global client
    if client is None:
        subdomain = os.getenv("BUSINESSMAP_SUBDOMAIN")
        api_key = os.getenv("BUSINESSMAP_API_KEY")
        
        if not subdomain or not api_key:
            raise ValueError("BUSINESSMAP_SUBDOMAIN and BUSINESSMAP_API_KEY environment variables must be set")
        
        client = BusinessmapMcpServer(subdomain, api_key)
    
    return client

@mcp.tool()
def list_workspaces() -> str:
    """List all BusinessMap workspaces"""
    try:
        workspaces = get_client().get_workspaces()
        return json.dumps(workspaces, indent=2)
    except Exception as e:
        logger.error(f"Error listing workspaces: {e}")
        return f"Error: {e}"

@mcp.tool()
def list_boards() -> str:
    """List all BusinessMap boards"""
    try:
        boards = get_client().get_boards()
        return json.dumps(boards, indent=2)
    except Exception as e:
        logger.error(f"Error listing boards: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_board_cards(board_id: int, limit: int = 50) -> str:
    """Get cards from a specific board
    
    Args:
        board_id: The ID of the board
        limit: Maximum number of cards to return (default: 50)
    """
    try:
        cards_data = get_client().get_cards(board_id, limit)
        return json.dumps(cards_data, indent=2)
    except Exception as e:
        logger.error(f"Error getting board cards: {e}")
        return f"Error: {e}"

@mcp.tool()
def get_card_details(card_id: int) -> str:
    """Get detailed information about a specific card
    
    Args:
        card_id: The ID of the card
    """
    try:
        card = get_client().get_card(card_id)
        return json.dumps(card, indent=2)
    except Exception as e:
        logger.error(f"Error getting card details: {e}")
        return f"Error: {e}"

@mcp.tool()
def search_cards(query: str, board_id: int = None, limit: int = 20) -> str:
    """Search for cards by title
    
    Args:
        query: Search query string
        board_id: Optional board ID to limit search to specific board
        limit: Maximum number of results (default: 20)
    """
    try:
        cards = get_client().search_cards(query, board_id, limit)
        return json.dumps(cards, indent=2)
    except Exception as e:
        logger.error(f"Error searching cards: {e}")
        return f"Error: {e}"

@mcp.tool()
def list_users() -> str:
    """List all BusinessMap users"""
    try:
        users = get_client().get_users()
        return json.dumps(users, indent=2)
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        return f"Error: {e}"

@mcp.tool()
def create_card(board_id: int, title: str, description: str = "") -> str:
    """Create a new card in BusinessMap
    
    Args:
        board_id: The ID of the board where the card should be created
        title: The title of the card
        description: Optional description for the card
    """
    try:
        card = get_client().create_card(board_id, title, description)
        return json.dumps(card, indent=2)
    except Exception as e:
        logger.error(f"Error creating card: {e}")
        return f"Error: {e}"

@mcp.tool()
def update_card(card_id: int, title: str = None, description: str = None) -> str:
    """Update an existing card in BusinessMap
    
    Args:
        card_id: The ID of the card to update
        title: New title for the card (optional)
        description: New description for the card (optional)
    """
    try:
        updates = {}
        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        
        if not updates:
            return "Error: No updates provided"
        
        card = get_client().update_card(card_id, **updates)
        return json.dumps(card, indent=2)
    except Exception as e:
        logger.error(f"Error updating card: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    import sys
    
    # Check if environment variables are set
    if not os.getenv("BUSINESSMAP_SUBDOMAIN") or not os.getenv("BUSINESSMAP_API_KEY"):
        print("Error: BUSINESSMAP_SUBDOMAIN and BUSINESSMAP_API_KEY environment variables must be set")
        sys.exit(1)
    
    # Run the MCP server
    mcp.run()