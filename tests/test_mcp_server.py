#!/usr/bin/env python3

import pytest
from dotenv import load_dotenv
from src.client import create_client
from src.types import CardTemplate

@pytest.fixture
def client():
    """Create and return a BusinessMap client fixture"""
    load_dotenv()
    return create_client()

def test_get_workspaces(client):
    """Test the get_workspaces method"""
    workspaces = client.get_workspaces()
    assert isinstance(workspaces, list)
    assert len(workspaces) > 0

def test_get_boards(client):
    """Test the get_boards method"""
    boards = client.get_boards()
    assert isinstance(boards, list)
    assert len(boards) > 0
    for board in boards:
        assert 'name' in board
        assert 'board_id' in board

def test_get_cards(client):
    """Test the get_cards method"""
    cards_data = client.get_cards(board_id=3, limit=3)
    assert isinstance(cards_data, dict)
    cards = cards_data.get("data", [])
    assert isinstance(cards, list)
    for card in cards:
        assert 'title' in card
        assert 'card_id' in card

def test_get_users(client):
    """Test the get_users method"""
    users = client.get_users()
    assert isinstance(users, list)
    assert len(users) > 0

def test_get_user_cards(client):
    """Test the get_user_cards method"""
    my_cards_data = client.get_user_cards(user_id=21, board_id=3, limit=10)
    assert isinstance(my_cards_data, dict)
    my_cards = my_cards_data.get("data", [])
    assert isinstance(my_cards, list)
    
    # Test with column filter
    progress_cards_data = client.get_user_cards(user_id=21, board_id=3, column_id=31, limit=10)
    assert isinstance(progress_cards_data, dict)
    progress_cards = progress_cards_data.get("data", [])
    assert isinstance(progress_cards, list)

def test_get_card(client):
    """Test the get_card method"""
    # Get a card to test with
    cards_data = client.get_cards(board_id=3, limit=1)
    cards = cards_data.get("data", [])
    assert len(cards) > 0, "No cards available to test get_card method"
    
    test_card_id = cards[0]['card_id']
    card_details = client.get_card(test_card_id)
    assert isinstance(card_details, dict)
    assert 'title' in card_details
    # URL field should be added by the client
    assert 'url' in card_details

def test_search_cards(client):
    """Test the search_cards method"""
    matching_cards = client.search_cards("test", board_id=3, limit=5)
    assert isinstance(matching_cards, list)

@pytest.mark.skip(reason="We don't want to create cards in the test suite")
def test_create_card(client):
    """Test the create_card method"""

    # Test creating a feature card
    new_card = client.create_card(
        board_id=3,  # Development board
        title="Test Feature Card - Pytest",
        template=CardTemplate.FEATURE,
        description="This is a test feature description",
        lane_id=12
    )
    
    assert isinstance(new_card, dict)
    assert 'card_id' in new_card
    
    # Verify the card was created by fetching its details
    card_details = client.get_card(new_card['card_id'])
    assert card_details.get('title') == "Test Feature Card - Pytest"