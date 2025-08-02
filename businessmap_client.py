"""
BusinessMap API Client

Provides a client class for interacting with BusinessMap (formerly Kanbanize) API.
"""

import os
import logging
from typing import List, Dict, Any, Optional

import requests

logger = logging.getLogger(__name__)


class BusinessMapClient:
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


def create_client() -> BusinessMapClient:
    """Create and return a BusinessMap client using environment variables"""
    subdomain = os.getenv("BUSINESSMAP_SUBDOMAIN")
    api_key = os.getenv("BUSINESSMAP_API_KEY")
    
    if not subdomain or not api_key:
        raise ValueError("BUSINESSMAP_SUBDOMAIN and BUSINESSMAP_API_KEY environment variables must be set")
    
    return BusinessMapClient(subdomain, api_key)