# DDGS API

[中文文档](README_ZH.md) | English

FastAPI-based REST API wrapper for DuckDuckGo Search with MCP (Model Context Protocol) support.

## Features

- **REST API**: Text, image, video, news, and books search endpoints
- **MCP Server**: Integrates with Claude Desktop and other MCP clients
- **Configurable Defaults**: Environment-based configuration for search parameters
- **API Key Authentication**: Optional authentication support

## Quick Start

### Installation

```bash
# Install dependencies
uv sync

# Copy environment configuration
cp .env.example .env
```

### Run Server

```bash
# Development mode with auto-reload
fastapi dev app/main.py

# Production mode
fastapi run app/main.py
```

Server runs at: `http://localhost:8000`

## API Endpoints

### REST API

- `GET /search?query=<query>` - Quick text search
- `POST /search/text` - Text search with parameters
- `POST /search/images` - Image search
- `POST /search/videos` - Video search
- `POST /search/news` - News search
- `POST /search/books` - Books search

API documentation: `http://localhost:8000/docs`

### MCP Server

MCP endpoint: `http://localhost:8000/mcp`

Available tools:
- `search_text` - Search text content

## Configuration

Key environment variables in `.env`:

```bash
# Proxy (optional)
DDGS_PROXY=

# Default search parameters
DEFAULT_REGION=wt-wt
DEFAULT_SAFESEARCH=moderate
DEFAULT_MAX_RESULTS=10

# API authentication (optional)
API_KEYS=your-api-key

# MCP enabled tools
MCP_ENABLE_TOOLS=text
```

## MCP Client Setup

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ddgs": {
      "url": "http://localhost:8000/mcp",
      "transport": {
        "type": "http"
      },
      "auth": {
        "type": "bearer",
        "token": "your-api-key"
      }
    }
  }
}
```

### Python Client

```python
from fastmcp.client import Client

async with Client("http://localhost:8000/mcp", auth="your-api-key") as client:
    tools = await client.list_tools()
    result = await client.call_tool("search_text", arguments={"query": "python"})
```

## Docker Deployment

### Build Image

```bash
# Build image
uv pip install -U ddgs # update ddgs (optional)
docker build -t ddgs-api:latest .
```

### Run Docker

```bash
# Basic run
docker run -d -p 8000:8000 --name ddgs-api ddgs-api:latest

# Run with environment variables (recommended)
docker run -d -p 8000:8000 --name ddgs-api \
  -e DDGS_PROXY=socks5://127.0.0.1:1080 \
  -e DEFAULT_MAX_RESULTS=20 \
  -e API_KEYS=your-api-key \
  ddgs-api:latest

# Run with .env file
docker run -d -p 8000:8000 --name ddgs-api \
  --env-file .env \
  ddgs-api:latest
```

Available environment variables:

**DDGS Initialization:**
- `DDGS_PROXY` - Proxy address
  - Supported protocols: `http://`, `https://`, `socks5://`, `socks5h://`
  - Examples: `socks5://127.0.0.1:1080` or `http://user:pass@proxy:port`
  - Special value: `tb` (use Tor Browser)
- `DDGS_TIMEOUT` - Request timeout in seconds (default: 5)

**Default Search Parameters:**
- `DEFAULT_REGION` - Default search region
  - Examples: `wt-wt` (global), `us-en` (USA), `cn-zh` (China), `uk-en`, `jp-jp`, `ru-ru`, etc.
- `DEFAULT_SAFESEARCH` - Safe search level
  - Options: `on` (strict), `moderate` (default), `off` (disabled)
- `DEFAULT_TIMELIMIT` - Time limit
  - Options: `d` (day), `w` (week), `m` (month), `y` (year)
- `DEFAULT_MAX_RESULTS` - Default maximum results (default: 10)
- `DEFAULT_PAGE` - Default page number (default: 1)
- `DEFAULT_BACKEND` - Search backend (default: `auto`)
  - Text search: `bing`, `brave`, `duckduckgo`, `google`, `mojeek`, `mullvad_brave`, `mullvad_google`, `yandex`, `yahoo`, `wikipedia`
  - Images/Videos: `duckduckgo` only
  - News: `bing`, `duckduckgo`, `yahoo`
  - Books: `annasarchive` only

**API Configuration:**
- `API_KEYS` - API authentication keys (comma-separated)
- `API_PREFIX` - API path prefix (e.g., `/api/v1`)

**MCP Configuration:**
- `MCP_ENABLE_TOOLS` - Enabled MCP tools (comma-separated, e.g., `text,news,books`)

**Performance Configuration:**
- `EXECUTOR_MAX_WORKERS` - Thread pool max workers (default: 100)
