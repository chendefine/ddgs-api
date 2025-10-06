import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import verify_token
from app.config import settings
from app.ddgs import get_ddgs
from app.models import BooksSearchRequest, ImagesSearchRequest, NewsSearchRequest, TextSearchRequest, VideosSearchRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["Search"], dependencies=[Depends(verify_token)])


@router.get("")
async def search(request: TextSearchRequest = Query(...)) -> list[dict[str, Any]]:
    """Quick search (direct text search)"""
    params = request.to_dict(settings.default_search_params)
    try:
        results = await get_ddgs().text(**params)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/text")
async def search_text(request: TextSearchRequest) -> list[dict[str, Any]]:
    """Text search"""
    params = request.to_dict(settings.default_search_params)
    try:
        results = await get_ddgs().text(**params)
        return results
    except Exception as e:
        logger.error(f"Error searching text: {e}, params: {params}")
        return []


@router.post("/images")
async def search_images(request: ImagesSearchRequest) -> list[dict[str, Any]]:
    """Image search"""
    params = request.to_dict(settings.default_search_params)
    # Add image-specific parameters
    if request.size is not None:
        params["size"] = request.size
    if request.color is not None:
        params["color"] = request.color
    if request.type_image is not None:
        params["type_image"] = request.type_image
    if request.layout is not None:
        params["layout"] = request.layout
    if request.license_image is not None:
        params["license_image"] = request.license_image

    try:
        results = await get_ddgs().images(**params)
        return results
    except Exception as e:
        logger.error(f"Error searching images: {e}, params: {params}")
        return []


@router.post("/videos")
async def search_videos(request: VideosSearchRequest) -> list[dict[str, Any]]:
    """Video search"""
    params = request.to_dict(settings.default_search_params)
    # Add video-specific parameters
    if request.resolution is not None:
        params["resolution"] = request.resolution
    if request.duration is not None:
        params["duration"] = request.duration
    if request.license_videos is not None:
        params["license_videos"] = request.license_videos

    try:
        results = await get_ddgs().videos(**params)
        return results
    except Exception as e:
        logger.error(f"Error searching videos: {e}, params: {params}")
        return []


@router.post("/news")
async def search_news(request: NewsSearchRequest) -> list[dict[str, Any]]:
    """News search"""
    params = request.to_dict(settings.default_search_params)
    try:
        results = await get_ddgs().news(**params)
        return results
    except Exception as e:
        logger.error(f"Error searching news: {e}, params: {params}")
        return []


@router.post("/books")
async def search_books(request: BooksSearchRequest) -> list[dict[str, Any]]:
    """Books search"""
    params = request.to_dict(settings.default_search_params)
    try:
        results = await get_ddgs().books(**params)
        return results
    except Exception as e:
        logger.error(f"Error searching books: {e}, params: {params}")
        return []
