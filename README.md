# BusinessMap MCP Server

A Model Context Protocol (MCP) server for integrating BusinessMap (formerly Kanbanize) with Claude Code and other MCP-compatible applications.

## Features

- **Board Management**: List workspaces and boards
- **Card Operations**: Search, view, create, and update cards
- **User Management**: List team members
- **Search Capabilities**: Find cards by title across boards

## Available Tools

### Information Tools
- `list_workspaces()` - Get all workspaces
- `list_boards()` - Get all boards  
- `list_users()` - Get all users
- `get_board_cards(board_id, limit=50)` - Get cards from a specific board
- `get_card_details(card_id)` - Get detailed card information
- `search_cards(query, board_id=None, limit=20)` - Search cards by title

### Management Tools
- `create_card(board_id, title, description="")` - Create new cards
- `update_card(card_id, title=None, description=None)` - Update existing cards

## Setup

### 1. Install Dependencies

```bash
cd businessmap-mcp-server
pip install -r requirements.txt
```

### 2. Set Environment Variables

You need to configure your BusinessMap credentials:

```bash
export BUSINESSMAP_SUBDOMAIN="YOUR_SUBDOMAIN_HERE"
export BUSINESSMAP_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
BUSINESSMAP_SUBDOMAIN=YOUR_SUBDOMAIN_HERE
BUSINESSMAP_API_KEY=your-api-key-here
```

### 3. Test the Server

```bash
python businessmap_mcp_server.py
```

## Claude Code Integration

To use with Claude Code, add this server to your MCP settings:

### Option 1: Using stdio transport

Add to your Claude Code settings (`~/.config/claude-code/settings/default.json`):

```json
{
  "mcpServers": {
    "businessmap": {
      "command": "python",
      "args": ["/path/to/businessmap-mcp-server/businessmap_mcp_server.py"],
      "env": {
        "BUSINESSMAP_SUBDOMAIN": "YOUR_SUBDOMAIN_HERE", 
        "BUSINESSMAP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Option 2: Using uv (recommended)

```json
{
  "mcpServers": {
    "businessmap": {
      "command": "uv",
      "args": ["--directory", "/path/to/businessmap-mcp-server", "run", "python", "businessmap_mcp_server.py"],
      "env": {
        "BUSINESSMAP_SUBDOMAIN": "YOUR_SUBDOMAIN_HERE",
        "BUSINESSMAP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Usage Examples

Once configured, you can use these commands in Claude Code:

- "List all my BusinessMap boards"
- "Show me cards in the Development board" 
- "Search for cards about 'authentication'"
- "Create a new card in board 3 with title 'Fix login bug'"
- "Get details for card 14193"
- "Update card 14193 with a new description"

## API Reference

### BusinessMap API Integration

This server uses BusinessMap's REST API v2. The following endpoints are supported:

- `GET /workspaces` - List workspaces
- `GET /boards` - List boards
- `GET /cards` - List cards (with filtering)
- `GET /cards/{id}` - Get card details
- `GET /users` - List users
- `POST /cards` - Create cards
- `PATCH /cards/{id}` - Update cards

## Security Notes

- Store your API key securely
- Use environment variables rather than hardcoding credentials
- The API key has full access to your BusinessMap account
- Consider creating a dedicated API key for this integration

## Troubleshooting

### Common Issues

1. **Authentication Error**: Verify your API key and subdomain are correct
2. **Connection Error**: Check your internet connection and BusinessMap service status
3. **Permission Error**: Ensure your API key has appropriate permissions

### Debug Mode

Enable debug logging:

```bash
export PYTHONPATH=/path/to/businessmap-mcp-server
export LOG_LEVEL=DEBUG
python businessmap_mcp_server.py
```

## Contributing

Feel free to extend this server with additional BusinessMap API endpoints or features.