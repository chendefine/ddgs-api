from fastapi.security import HTTPAuthorizationCredentials
from fastmcp.server.auth import AccessToken, AuthProvider

# from fastmcp.server.dependencies import get_http_headers
from app.auth import verify_token


class ApiKeyTokenVerifier(AuthProvider):
    def __init__(self):
        super().__init__(base_url="http://localhost", required_scopes=[])

    async def verify_token(self, api_key: str) -> AccessToken | None:
        api_key = api_key.removeprefix("Bearer ")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=api_key)
        try:
            await verify_token(credentials)
            return AccessToken(token=api_key, client_id="", scopes=[])
        except Exception:
            return None
