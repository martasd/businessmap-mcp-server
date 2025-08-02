"""
BusinessMap MCP Tools

MCP tool functions for interacting with BusinessMap API.
"""

import json
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from businessmap_client import create_client, BusinessMapClient

logger = logging.getLogger(__name__)

# Global client instance (lazily initialized)
_client: Optional[BusinessMapClient] = None


def get_client() -> BusinessMapClient:
    """Get or initialize the BusinessMap client"""
    global _client
    if _client is None:
        _client = create_client()
    return _client


def register_tools(mcp: FastMCP) -> None:
    """Register all BusinessMap tools with the MCP server"""
    
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