"""
BusinessMap Card Types

Shared type definitions for BusinessMap MCP server.
"""

from enum import Enum


class CardTemplate(Enum):
    FEATURE = "feature"
    BUG = "bug"
    SUPPORT = "support"