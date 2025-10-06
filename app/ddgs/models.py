from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field


class TextSearchItem(BaseModel):
    """Text search item model"""

    title: Annotated[str, Field(description="web title")]
    href: Annotated[str, Field(description="url")]
    body: Annotated[str, Field(description="summary")]


class ImagesSearchItem(BaseModel):
    """Images search item model"""

    title: Annotated[str, Field(description="web title")]
    image: Annotated[str, Field(description="image url")]
    thumbnail: Annotated[str | None, Field(description="thumbnail url")]
    url: Annotated[str | None, Field(description="web url where image is from")]
    height: Annotated[int | None, Field(description="image height")]
    width: Annotated[int | None, Field(description="image width")]
    source: Annotated[str | None, Field(description="search engine source")]


class VideosSearchItem(BaseModel):
    """Videos search item model"""

    title: Annotated[str, Field(description="web title")]
    content: Annotated[str, Field(description="web url where video is from")]
    description: Annotated[str | None, Field(description="video description")]
    duration: Annotated[str | None, Field(description="video duration")]
    embed_html: Annotated[str | None, Field(description="video embed html code")]
    embed_url: Annotated[str | None, Field(description="video embed url")]
    image_token: Annotated[str | None, Field(description="video image token")]
    images: Annotated[dict[str, str] | None, Field(description="video thumbnail images urls")]
    provider: Annotated[str | None, Field(description="search engine source")]
    published: Annotated[str | None, Field(description="video published time(UTC)")]
    publisher: Annotated[str | None, Field(description="video platform")]
    statistics: Annotated[dict[str, int] | None, Field(description="video statistics")]
    uploader: Annotated[str | None, Field(description="video uploader")]


class NewsSearchItem(BaseModel):
    """News search item model"""

    title: Annotated[str, Field(description="news title")]
    body: Annotated[str, Field(description="news summary")]
    url: Annotated[str, Field(description="news url")]
    image: Annotated[str | None, Field(description="news image url")]
    date: Annotated[str | None, Field(description="news published time")]
    source: Annotated[str | None, Field(description="news source")]


class BooksSearchItem(BaseModel):
    """Books search item model"""

    title: Annotated[str, Field(description="book title")]
    author: Annotated[str | None, Field(description="book author")]
    publisher: Annotated[str | None, Field(description="book platform")]
    info: Annotated[str | None, Field(description="book info")]
    url: Annotated[str, Field(description="book url")]
    thumbnail: Annotated[str | None, Field(description="book cover url")]
