from typing import Any

from pydantic import BaseModel, Field


class BaseSearchRequest(BaseModel):
    """Base search request model"""

    query: str = Field(..., description="search query", min_length=1)
    region: str | None = Field(None, description="region to use for the search (e.g., us-en, uk-en, ru-ru, etc.)")
    safesearch: str | None = Field(None, description="safesearch setting (e.g., on, moderate, off)")
    timelimit: str | None = Field(None, description="timelimit for the search (e.g., d, w, m, y) or custom date range")
    max_results: int | None = Field(None, description="maximum number of results to return. Defaults to 10", ge=1, le=100)
    page: int | None = Field(None, description="page of results to return. Defaults to 1", ge=1)
    backend: str | None = Field(None, description='single or comma-delimited backends. Defaults to "auto"')

    def to_dict(self, defaults: dict[str, Any]) -> dict[str, Any]:
        """Convert request to dictionary"""
        return {**defaults, **self.model_dump(exclude_none=True)}


class TextSearchRequest(BaseSearchRequest):
    """Text search request model"""

    pass


class ImagesSearchRequest(BaseSearchRequest):
    """Image search request model"""

    size: str | None = Field(None, description="Image size: Small, Medium, Large, Wallpaper")
    color: str | None = Field(None, description="Image color")
    type_image: str | None = Field(None, description="Image type: photo, clipart, gif, transparent, line")
    layout: str | None = Field(None, description="Image layout: Square, Tall, Wide")
    license_image: str | None = Field(None, description="Image license: any, Public, Share, Modify, ModifyCommercially")


class VideosSearchRequest(BaseSearchRequest):
    """Video search request model"""

    resolution: str | None = Field(None, description="Video resolution: high, standard")
    duration: str | None = Field(None, description="Video duration: short, medium, long")
    license_videos: str | None = Field(None, description="Video license: creativeCommon, youtube")


class NewsSearchRequest(BaseSearchRequest):
    """News search request model"""

    pass


class BooksSearchRequest(BaseSearchRequest):
    """Books search request model"""

    pass
