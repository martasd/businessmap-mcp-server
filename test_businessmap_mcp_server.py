#!/usr/bin/env python3
"""
Test script for BusinessMap API client using refactored modules
"""

import os
from dotenv import load_dotenv
from businessmap_client import create_client

def test_connection():
    """Test the API connection using the refactored client"""
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        print("Creating BusinessMap client...")
        client = create_client()
        
        print("Testing boards...")
        boards = client.get_boards()
        print(f"✅ Connection successful! Found {len(boards)} boards:")
        for board in boards:
            print(f"  - {board['name']} (ID: {board['board_id']})")
        
        # Test getting cards from Development board (ID: 3)
        print("\nTesting cards from Development board...")
        cards_data = client.get_cards(board_id=3, limit=3)
        cards = cards_data.get("data", [])
        print(f"✅ Found {len(cards)} sample cards:")
        for card in cards:
            print(f"  - {card['title']} (ID: {card['card_id']})")
        
        # Test workspaces
        print("\nTesting workspaces...")
        workspaces = client.get_workspaces()
        print(f"✅ Found {len(workspaces)} workspaces")
        
        # Test users
        print("\nTesting users...")
        users = client.get_users()
        print(f"✅ Found {len(users)} users")
        
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing BusinessMap API connection...")
    test_connection()