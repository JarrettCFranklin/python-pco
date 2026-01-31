"""OAuth 2.0 authentication for PCO API."""

from typing import Any

import httpx


class OAuth2Token:
    """OAuth 2.0 token storage and management."""

    def __init__(
        self,
        access_token: str,
        token_type: str = "Bearer",
        expires_in: int | None = None,
        refresh_token: str | None = None,
        scope: str | None = None,
    ):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.scope = scope
        self._expires_at: float | None = None

        if expires_in:
            import time

            self._expires_at = time.time() + expires_in

    def is_expired(self) -> bool:
        """Check if the token is expired."""
        if self._expires_at is None:
            return False
        import time

        return time.time() >= self._expires_at

    def to_header(self) -> dict[str, str]:
        """Convert token to Authorization header format."""
        return {"Authorization": f"{self.token_type} {self.access_token}"}


class OAuth2Client:
    """OAuth 2.0 client for PCO API authentication."""

    BASE_URL = "https://api.planningcenteronline.com"
    TOKEN_URL = "https://api.planningcenteronline.com/oauth/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str | None = None,
        http_client: httpx.Client | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._http_client = http_client or httpx.Client()
        self._token: OAuth2Token | None = None

    def get_authorization_url(self, state: str | None = None, scope: str = "people services check_ins giving resources") -> str:
        """Generate the authorization URL for OAuth flow."""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": scope,
        }
        if self.redirect_uri:
            params["redirect_uri"] = self.redirect_uri
        if state:
            params["state"] = state

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.BASE_URL}/oauth/authorize?{query_string}"

    def exchange_code_for_token(self, code: str) -> OAuth2Token:
        """Exchange authorization code for access token."""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.redirect_uri:
            data["redirect_uri"] = self.redirect_uri

        response = self._http_client.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()

        self._token = OAuth2Token(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in"),
            refresh_token=token_data.get("refresh_token"),
            scope=token_data.get("scope"),
        )
        return self._token

    def refresh_access_token(self) -> OAuth2Token:
        """Refresh the access token using refresh token."""
        if not self._token or not self._token.refresh_token:
            raise ValueError("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._token.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = self._http_client.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()

        self._token = OAuth2Token(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in"),
            refresh_token=token_data.get("refresh_token") or self._token.refresh_token,
            scope=token_data.get("scope") or self._token.scope,
        )
        return self._token

    def set_token(self, token: OAuth2Token) -> None:
        """Set the token manually (for token storage/retrieval)."""
        self._token = token

    def get_token(self) -> OAuth2Token | None:
        """Get the current token."""
        if self._token and self._token.is_expired() and self._token.refresh_token:
            try:
                self.refresh_access_token()
            except Exception:
                pass  # If refresh fails, return expired token
        return self._token

    def get_authorization_header(self) -> dict[str, str]:
        """Get the authorization header for API requests."""
        token = self.get_token()
        if not token:
            raise ValueError("No token available. Please authenticate first.")
        return token.to_header()

    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()

    def __enter__(self) -> "OAuth2Client":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
