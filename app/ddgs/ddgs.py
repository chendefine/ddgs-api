from __future__ import annotations

import asyncio
from typing import Any

from ddgs import DDGS

from .executor import cleanup_executor, get_executor, initialize_executor
from .models import *

# Global DDGS instance
ddgs_instance: AsyncDDGS | None = None


class AsyncDDGS:
    """Async DDGS instance"""

    def __init__(self, proxy: str | None = None, timeout: int | None = 5, verify: bool = True):
        self.executor = get_executor()
        self.ddgs = DDGS(proxy=proxy, timeout=timeout, verify=verify)

    async def text(self, query: str, **kwargs: Any) -> list[TextSearchItem]:
        """async execute a text search"""
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(self.executor, lambda: list(self.ddgs.text(query, **kwargs)))
        return [TextSearchItem(**result) for result in results if result.get("href")] if results else []

    async def images(self, query: str, **kwargs: Any) -> list[ImagesSearchItem]:
        """async execute an image search"""
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(self.executor, lambda: list(self.ddgs.images(query, **kwargs)))
        return [ImagesSearchItem(**result) for result in results if result.get("url")] if results else []

    async def videos(self, query: str, **kwargs: Any) -> list[VideosSearchItem]:
        """async execute a video search"""
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(self.executor, lambda: list(self.ddgs.videos(query, **kwargs)))
        return [VideosSearchItem(**result) for result in results if result.get("content")] if results else []

    async def news(self, query: str, **kwargs: Any) -> list[NewsSearchItem]:
        """async execute a news search"""
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(self.executor, lambda: list(self.ddgs.news(query, **kwargs)))
        return [NewsSearchItem(**result) for result in results if result.get("url")] if results else []

    async def books(self, query: str, **kwargs: Any) -> list[BooksSearchItem]:
        """async execute a book search"""
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(self.executor, lambda: list(self.ddgs.books(query, **kwargs)))
        return [BooksSearchItem(**result) for result in results if result.get("title")] if results else []


def initialize_ddgs():
    """Initialize DDGS instance"""
    initialize_executor()

    global ddgs_instance
    ddgs_instance = AsyncDDGS()


def cleanup_ddgs():
    """Cleanup DDGS instance"""
    cleanup_executor()
    global ddgs_instance
    ddgs_instance = None


def get_ddgs() -> AsyncDDGS:
    """Get DDGS instance (dependency injection)"""
    if ddgs_instance is None:
        raise RuntimeError("DDGS not initialized")
    return ddgs_instance
