"""Main API client for PCO API."""

import time
from typing import Any

import httpx

from pco.auth import OAuth2Client, OAuth2Token
from pco.exceptions import PCOAPIError, PCONotFoundError, PCORateLimitError, PCOValidationError


class PCOClient:
    """Main client for interacting with Planning Center Online API."""

    BASE_URL = "https://api.planningcenteronline.com"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_RETRY_DELAY = 1.0
    MAX_RETRIES = 3

    def __init__(
        self,
        oauth_client: OAuth2Client | None = None,
        token: OAuth2Token | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        http_client: httpx.Client | None = None,
    ):
        """Initialize PCO client.

        Args:
            oauth_client: OAuth2Client instance for authentication
            token: OAuth2Token instance (alternative to oauth_client)
            base_url: Base URL for API (defaults to official PCO API)
            timeout: Request timeout in seconds
            http_client: Custom httpx.Client instance
        """
        if oauth_client and token:
            raise ValueError("Cannot provide both oauth_client and token")

        self.oauth_client = oauth_client
        self._token = token
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self._http_client = http_client or httpx.Client(timeout=self.timeout)

        # Initialize modules
        self._people: PeopleModule | None = None
        self._services: ServicesModule | None = None
        self._checkins: CheckInsModule | None = None
        self._giving: GivingModule | None = None
        self._resources: ResourcesModule | None = None

    def _get_headers(self) -> dict[str, str]:
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        if self.oauth_client:
            headers.update(self.oauth_client.get_authorization_header())
        elif self._token:
            headers.update(self._token.to_header())
        else:
            raise ValueError("No authentication provided. Use oauth_client or token.")

        return headers

    def _handle_response(self, response: httpx.Response) -> dict[str, Any] | list[Any]:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 404:
            raise PCONotFoundError("Resource not found", response_data=response.json() if response.content else None)
        elif response.status_code == 429:
            raise PCORateLimitError("Rate limit exceeded", response_data=response.json() if response.content else None)
        elif response.status_code == 400:
            error_data = response.json() if response.content else None
            message = "Validation error"
            if error_data and isinstance(error_data, dict):
                message = error_data.get("error", message)
            raise PCOValidationError(message, response_data=error_data)
        elif not response.is_success:
            error_data = response.json() if response.content else None
            message = f"API error: {response.status_code}"
            if error_data and isinstance(error_data, dict):
                message = error_data.get("error", message)
            raise PCOAPIError(message, status_code=response.status_code, response_data=error_data)

        if not response.content:
            return {}

        return response.json()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        retries: int = 0,
    ) -> dict[str, Any] | list[Any]:
        """Make HTTP request to PCO API with retry logic."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        try:
            response = self._http_client.request(method, url, headers=headers, params=params, json=json)
            return self._handle_response(response)
        except PCORateLimitError as e:
            if retries < self.MAX_RETRIES:
                # Wait before retrying on rate limit
                time.sleep(self.DEFAULT_RETRY_DELAY * (retries + 1))
                return self._request(method, endpoint, params=params, json=json, retries=retries + 1)
            raise e
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            if retries < self.MAX_RETRIES:
                time.sleep(self.DEFAULT_RETRY_DELAY * (retries + 1))
                return self._request(method, endpoint, params=params, json=json, retries=retries + 1)
            raise PCOAPIError(f"Network error: {e}") from e

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Make GET request."""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Make POST request."""
        return self._request("POST", endpoint, params=params, json=json)

    def put(self, endpoint: str, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Make PUT request."""
        return self._request("PUT", endpoint, params=params, json=json)

    def patch(self, endpoint: str, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Make PATCH request."""
        return self._request("PATCH", endpoint, params=params, json=json)

    def delete(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Make DELETE request."""
        return self._request("DELETE", endpoint, params=params)

    @property
    def people(self) -> PeopleModule:
        """Access People API module."""
        if self._people is None:
            self._people = PeopleModule(self)
        return self._people

    @property
    def services(self) -> ServicesModule:
        """Access Services API module."""
        if self._services is None:
            self._services = ServicesModule(self)
        return self._services

    @property
    def checkins(self) -> CheckInsModule:
        """Access Check-Ins API module."""
        if self._checkins is None:
            self._checkins = CheckInsModule(self)
        return self._checkins

    @property
    def giving(self) -> GivingModule:
        """Access Giving API module."""
        if self._giving is None:
            self._giving = GivingModule(self)
        return self._giving

    @property
    def resources(self) -> ResourcesModule:
        """Access Resources API module."""
        if self._resources is None:
            self._resources = ResourcesModule(self)
        return self._resources

    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()
        if self.oauth_client:
            self.oauth_client.close()

    def __enter__(self) -> "PCOClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
