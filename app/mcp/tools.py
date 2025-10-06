from typing import Annotated, Any

from app.config import settings
from app.ddgs import get_ddgs

from .server import mcp

default_max_results = settings.default_max_results or 10


if "text" in settings.mcp_enable_tools:

    @mcp.tool
    async def search_text(
        query: Annotated[str, "search query"],
        max_results: Annotated[int, "maximum number of results to return"] = default_max_results,
    ) -> list[dict[str, Any]]:
        """search web pages"""
        params = {"query": query, "max_results": max_results}
        try:
            results = await get_ddgs().text(**params)
            return results
        except Exception:
            return []


if "images" in settings.mcp_enable_tools:

    @mcp.tool
    async def search_images(
        query: Annotated[str, "search query"],
        max_results: Annotated[int, "maximum number of results to return"] = default_max_results,
    ) -> list[dict[str, Any]]:
        """search images"""

        params = {"query": query, "max_results": max_results}
        try:
            results = await get_ddgs().images(**params)
            return results
        except Exception:
            return []


if "videos" in settings.mcp_enable_tools:

    @mcp.tool
    async def search_videos(
        query: Annotated[str, "search query"],
        max_results: Annotated[int, "maximum number of results to return"] = default_max_results,
    ) -> list[dict[str, Any]]:
        """search videos"""

        params = {"query": query, "max_results": max_results}
        try:
            results = await get_ddgs().videos(**params)
            return results
        except Exception:
            return []


if "news" in settings.mcp_enable_tools:

    @mcp.tool
    async def search_news(
        query: Annotated[str, "search query"],
        max_results: Annotated[int, "maximum number of results to return"] = default_max_results,
    ) -> list[dict[str, Any]]:
        """search news"""

        params = {"query": query, "max_results": max_results}
        try:
            results = await get_ddgs().news(**params)
            return results
        except Exception:
            return []


if "books" in settings.mcp_enable_tools:

    @mcp.tool
    async def search_books(
        query: Annotated[str, "search query"],
        max_results: Annotated[int, "maximum number of results to return"] = default_max_results,
    ) -> list[dict[str, Any]]:
        """search books"""

        params = {"query": query, "max_results": max_results}
        try:
            results = await get_ddgs().books(**params)
            return results
        except Exception:
            return []
