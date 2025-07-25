#!/usr/bin/env python3
"""
Simple test script for BusinessMap API client (no MCP dependencies)
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional

class TestBusinessmapMcpServer:
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
    
    def get_boards(self) -> List[Dict[str, Any]]:
        """Get all boards"""
        result = self._make_request("GET", "/boards")
        return result.get("data", [])
    
    def get_cards(self, board_id: Optional[int] = None, limit: int = 5) -> Dict[str, Any]:
        """Get cards, optionally filtered by board"""
        params = {"limit": limit}
        if board_id:
            params["board_id"] = board_id
        
        result = self._make_request("GET", "/cards", params=params)
        return result.get("data", {})
    
    def test_connection(self):
        """Test the API connection"""
        try:
            print("Testing boards...")
            boards = self.get_boards()
            print(f"✅ Connection successful! Found {len(boards)} boards:")
            for board in boards:
                print(f"  - {board['name']} (ID: {board['board_id']})")
            
            # Test getting cards from Development board (ID: 3)
            print("\nTesting cards from Development board...")
            cards_data = self.get_cards(board_id=3, limit=3)
            cards = cards_data.get("data", [])
            print(f"✅ Found {len(cards)} sample cards:")
            for card in cards:
                print(f"  - {card['title']} (ID: {card['card_id']})")
            
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

if __name__ == "__main__":
    # Test with your credentials
    subdomain = "YOUR_SUBDOMAIN_HERE"
    api_key = "YOUR_API_KEY_HERE"
    
    print("Testing BusinessMap API connection...")
    client = TestBusinessmapMcpServer(subdomain, api_key)
    client.test_connection()