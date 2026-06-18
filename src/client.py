"""
BusinessMap API Client

Provides a client class for interacting with BusinessMap (formerly Kanbanize) API.
"""

import logging
import os
from typing import Any

import requests

from .types import CardTemplate

logger = logging.getLogger(__name__)

DEFAULT_BOARD_ID = 3  # Development board
DEFAULT_COLUMN_ID = 37  # Ready for Development column
DEFAULT_TAG_ID = 98 # Add Python by default
DEFAULT_LANE_ID = 12 # BRIGHTSCRIP lane


class BusinessMapClient:
    """Client for interacting with BusinessMap API"""

    def __init__(self, subdomain: str, api_key: str):
        self.base_url = f"https://{subdomain}.kanbanize.com/api/v2"
        self.headers = {"Accept": "application/json", "apikey": api_key}

    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict[str, Any]:
        """Make HTTP request to BusinessMap API"""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if not response.ok:
            logger.error(f"Request failed: {response.status_code} {response.text}")

        response.raise_for_status()

        return response.json()

    def get_workspaces(self) -> list[dict[str, Any]]:
        """Get all workspaces"""
        result = self._make_request("GET", "/workspaces")
        return result.get("data", [])

    def get_boards(self) -> list[dict[str, Any]]:
        """Get all boards"""
        result = self._make_request("GET", "/boards")
        return result.get("data", [])

    def get_cards(self, board_id: int | None = None, limit: int = 50) -> dict[str, Any]:
        """Get cards, optionally filtered by board"""
        params = {"limit": limit}
        if board_id:
            params["board_id"] = board_id

        result = self._make_request("GET", "/cards", params=params)
        return result.get("data", {})

    def get_user_cards(
        self, user_id: int, board_id: int | None = None, column_id: int | None = None, limit: int = 50
    ) -> dict[str, Any]:
        """Get cards assigned to a specific user"""
        params = {"limit": limit, "owner_user_ids": user_id}
        if board_id:
            params["board_id"] = board_id
        if column_id:
            params["column_ids"] = column_id

        result = self._make_request("GET", "/cards", params=params)
        return result.get("data", {})

    def get_card(self, card_id: int) -> dict[str, Any]:
        """Get detailed information about a specific card"""
        result = self._make_request("GET", f"/cards/{card_id}")
        card_data = result.get("data", {})

        # Add URL to the card data
        if card_data and "board_id" in card_data:
            board_id = card_data["board_id"]
            subdomain = self.base_url.split("//")[1].split(".")[0]
            card_data["url"] = f"https://{subdomain}.kanbanize.com/ctrl_board/{board_id}/cards/{card_id}/details/"

        return card_data

    def search_cards(self, query: str, board_id: int | None = None, limit: int = 20) -> list[dict[str, Any]]:
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

    def get_users(self) -> list[dict[str, Any]]:
        """Get all users"""
        result = self._make_request("GET", "/users")
        return result.get("data", [])

    def get_current_user(self) -> dict[str, Any]:
        """Get current user information"""
        result = self._make_request("GET", "/me")
        return result.get("data", {})

    @staticmethod
    def get_template_embedded_description(template_type: CardTemplate, description: str) -> str:
        """Get card template based on type with description incorporated"""
        templates = {
            CardTemplate.FEATURE: f"""<p><span class="text-big">Feature set:</span></p><ul><li>{description}&nbsp;</li></ul><p><span class="text-big">Testing scenarios / Acceptance criteria:</span></p><ul><li>&nbsp;</li></ul><p><span class="text-big">Deployment:</span></p><ul><li>&nbsp;</li></ul><p>&nbsp;</p>""",
            CardTemplate.BUG: f"""<p><span class="text-big">Current Behavior:</span>{description}</p><ul><li>&nbsp;</li></ul><p><span class="text-big">Expected Behavior:</span></p><ul><li>&nbsp;</li></ul><p><span class="text-big">How to reproduce</span></p><ul><li>&nbsp;</li></ul><p><span class="text-big">Deployment:</span></p><ul><li>&nbsp;</li></ul><p>&nbsp;</p>""",
            CardTemplate.SUPPORT: f"""<p><span class="text-big">Feature set:</span>{description}</p><ul><li>&nbsp;</li></ul><p><span class="text-big">Testing scenarios / Acceptance criteria:</span></p><ul><li>&nbsp;</li></ul><p><span class="text-big">Related sources:</span></p><ul><li>&nbsp;</li></ul><p><span class="text-big">Deployment:</span></p><ul><li>&nbsp;</li></ul><p>&nbsp;</p>""",
        }

        return templates.get(template_type, "")

    def create_card(
        self,
        title: str,
        description: str,
        owner_user_id: int | None = None,
        tag_ids: list[int] | None = None,
        board_id: int = DEFAULT_BOARD_ID,
        lane_id: int = DEFAULT_LANE_ID,
        column_id: int = DEFAULT_COLUMN_ID,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Create a new card.

        Args:
            title (str): The title of the new card.
            description (str): The description html for the new card.
            board_id (int, optional): The ID of the board where the card will be created. Default is Development.
            lane_id (int, optional): The ID of the lane where the card will be created. Default is BRIGHTSCRIP.
            column_id (int, optional): The ID of the column under which the card is created. Default is Ready for Development.
            owner_user_id (int, optional): The ID of the user who will own the card. If None, uses the current user.
            tag_ids (list[int], optional): A list of tag IDs to add to the card. Default is the Python tag.

        """
        if tag_ids is None:
            tag_ids = [DEFAULT_TAG_ID]


        data = {
            "title": title,
            "description": description,
            "board_id": board_id,
            "lane_id": lane_id,
            "column_id": column_id,
            "owner_user_id": owner_user_id,
            "tag_ids_to_add": tag_ids,
            **kwargs,
        }

        response = self._make_request("POST", "/cards", json=data)
        result = response.get("data")

        if result:
            return result[0]
        return {}

    def update_card(self, card_id: int, **kwargs) -> dict[str, Any]:
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
