# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI-based REST API wrapper for DuckDuckGo Search (DDGS library). Provides endpoints for text, image, video, news, and books search with configurable defaults via environment variables.

## Development Commands

### Setup
```bash
# Install dependencies (using uv - fast Python package manager)
uv sync

# Run development server with auto-reload
fastapi dev app/main.py
```

### Code Quality
```bash
# Run linter and formatter
uv run ruff check .
uv run ruff format .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Package Management

This project uses **uv** instead of Poetry for faster dependency management:

```bash
# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Update dependencies
uv sync

# Update a specific package
uv sync --upgrade-package <package-name>
```

## Architecture

### Core Components

- **[app/main.py](app/main.py)**: FastAPI application entry point with lifespan management
  - Initializes global DDGS instance on startup via `initialize_ddgs()`
  - Cleans up on shutdown via `cleanup_ddgs()`

- **[app/ddgs/ddgs.py](app/ddgs/ddgs.py)**: DDGS instance management
  - Maintains singleton `ddgs_instance` initialized from settings
  - Provides `get_ddgs()` dependency injection function used by all routes

- **[app/config.py](app/config.py)**: Configuration system using pydantic-settings
  - Loads from `.env` file or environment variables
  - Aggregates `default_*` settings into `default_search_params` dict
  - This dict is merged into each search request in routes

- **[app/models.py](app/models.py)**: Pydantic request models
  - `BaseSearchRequest` provides common fields (query, region, safesearch, etc.)
  - Specialized models (Images, Videos, News, Books) extend with type-specific fields
  - `to_dict()` method merges request params with defaults

- **[app/routes/search.py](app/routes/search.py)**: Search API endpoints
  - `GET /search`: Quick text search
  - `POST /search/text|images|videos|news|books`: Typed search endpoints
  - Each endpoint merges request params with `settings.default_search_params`

- **[app/executor.py](app/executor.py)**: Thread pool executor management
  - Maintains singleton `executor` instance for blocking I/O operations
  - Provides `get_executor()` function used by routes via `run_in_executor`
  - Configured via `settings.executor_max_workers`

### Configuration Flow

1. Environment variables → `Settings` class ([app/config.py](app/config.py))
2. `Settings.__init__()` aggregates `default_*` vars into `default_search_params` dict
3. Routes merge this dict with request params via `request.to_dict(settings.default_search_params)`
4. Merged params passed to DDGS methods

### Dependency Injection

All route handlers use `ddgs: DDGS = Depends(get_ddgs)` to access the singleton DDGS instance initialized during app startup.

## Ruff Configuration

- Line length: 180 characters
- Target: Python 3.12+
- Key ignores: E501 (line length), N802/N818 (naming), B008 (FastAPI defaults), S324 (security)
