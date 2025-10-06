from fastmcp import FastMCP

from app.config import settings

from .auth import ApiKeyTokenVerifier

mcp_auth = ApiKeyTokenVerifier() if settings.api_keys else None

# Create MCP server with error masking enabled
mcp = FastMCP("DDG-Search-API", mask_error_details=True, auth=mcp_auth)

mcp_app = mcp.http_app(stateless_http=True)
