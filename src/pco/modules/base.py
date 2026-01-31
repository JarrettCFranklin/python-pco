"""Base module class for PCO API modules."""

from typing import Any

from pco.client import PCOClient


class BaseModule:
    """Base class for PCO API modules."""

    def __init__(self, client: PCOClient, base_path: str):
        """Initialize base module.

        Args:
            client: PCOClient instance
            base_path: Base API path for this module (e.g., '/people/v2')
        """
        self.client = client
        self.base_path = base_path.rstrip("/")

    def _build_path(self, *parts: str) -> str:
        """Build API path from parts."""
        path = self.base_path
        for part in parts:
            if part:
                path = f"{path}/{part.lstrip('/')}"
        return path

    def list(self, resource: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List resources.

        Args:
            resource: Resource name (e.g., 'people', 'households')
            params: Query parameters

        Returns:
            API response
        """
        endpoint = self._build_path(resource)
        return self.client.get(endpoint, params=params)

    def get(self, resource: str, resource_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single resource.

        Args:
            resource: Resource name (e.g., 'people', 'households')
            resource_id: Resource ID
            params: Query parameters

        Returns:
            API response
        """
        endpoint = self._build_path(resource, resource_id)
        response = self.client.get(endpoint, params=params)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected dict response, got {type(response)}")

    def create(self, resource: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new resource.

        Args:
            resource: Resource name
            data: Resource data
            params: Query parameters

        Returns:
            Created resource
        """
        endpoint = self._build_path(resource)
        response = self.client.post(endpoint, json=data, params=params)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected dict response, got {type(response)}")

    def update(self, resource: str, resource_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a resource.

        Args:
            resource: Resource name
            resource_id: Resource ID
            data: Updated data
            params: Query parameters

        Returns:
            Updated resource
        """
        endpoint = self._build_path(resource, resource_id)
        response = self.client.patch(endpoint, json=data, params=params)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected dict response, got {type(response)}")

    def delete(self, resource: str, resource_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a resource.

        Args:
            resource: Resource name
            resource_id: Resource ID
            params: Query parameters
        """
        endpoint = self._build_path(resource, resource_id)
        self.client.delete(endpoint, params=params)

    def get_related(self, resource: str, resource_id: str, related: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get related resources.

        Args:
            resource: Resource name
            resource_id: Resource ID
            related: Related resource name
            params: Query parameters

        Returns:
            API response
        """
        endpoint = self._build_path(resource, resource_id, related)
        return self.client.get(endpoint, params=params)
