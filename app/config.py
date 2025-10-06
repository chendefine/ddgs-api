from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration, loaded from environment variables or .env file"""

    # DDGS initialization parameters
    ddgs_proxy: str | None = None
    ddgs_timeout: int | None = None

    # Default search parameters
    default_region: str | None = None
    default_safesearch: str | None = None
    default_timelimit: str | None = None
    default_max_results: int | None = None
    default_page: int | None = None
    default_backend: str | None = None

    default_search_params: dict[str, Any] = {}

    # API keys
    api_keys: list[str] | str = ""

    # API base
    api_prefix: str = ""

    # MCP
    mcp_enable_tools: list[str] = ["text"]

    # Thread pool configuration for blocking I/O operations
    executor_max_workers: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.default_region:
            self.default_search_params["region"] = self.default_region

        if self.default_safesearch:
            self.default_search_params["safesearch"] = self.default_safesearch

        if self.default_timelimit:
            self.default_search_params["timelimit"] = self.default_timelimit

        if self.default_max_results:
            self.default_search_params["max_results"] = self.default_max_results

        if self.default_page:
            self.default_search_params["page"] = self.default_page

        if self.default_backend:
            self.default_search_params["backend"] = self.default_backend

        if isinstance(self.api_keys, str) and self.api_keys:
            self.api_keys = [self.api_keys]

        if self.api_prefix and not self.api_prefix.startswith("/"):
            self.api_prefix = f"/{self.api_prefix}"


settings = Settings()
