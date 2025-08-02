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
        
        # Test get_user_cards for user ID 21 (martin.dluhos)
        print("\nTesting get_user_cards for user 21 on Development board...")
        my_cards_data = client.get_user_cards(user_id=21, board_id=3, limit=10)
        my_cards = my_cards_data.get("data", [])
        print(f"✅ Found {len(my_cards)} cards assigned to user 21:")
        for card in my_cards:
            print(f"  - {card['title']} (ID: {card['card_id']})")
        
        # Test get_user_cards with column_id filter (In Progress - column 31)
        print("\nTesting get_user_cards for user 21 in In Progress column (31)...")
        progress_cards_data = client.get_user_cards(user_id=21, board_id=3, column_id=31, limit=10)
        progress_cards = progress_cards_data.get("data", [])
        print(f"✅ Found {len(progress_cards)} cards in column 31:")
        for card in progress_cards:
            print(f"  - {card['title']} (ID: {card['card_id']})")
        
        # Test get_card with URL functionality
        if progress_cards:
            test_card_id = progress_cards[0]['card_id']
            print(f"\nTesting get_card details with URL for card {test_card_id}...")
            card_details = client.get_card(test_card_id)
            if 'url' in card_details:
                print(f"✅ URL field added successfully: {card_details['url']}")
            else:
                print("❌ URL field not found in card details")
        
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing BusinessMap API connection...")
    test_connection()