"""Check-Ins API module for PCO."""

from typing import Any

from pco.modules.base import BaseModule


class CheckInsModule(BaseModule):
    """Module for interacting with PCO Check-Ins API."""

    def __init__(self, client):
        super().__init__(client, "/check_ins/v2")

    def list_events(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all check-in events.

        Args:
            params: Query parameters (e.g., per_page, offset, where, order)

        Returns:
            List of events
        """
        return self.list("events", params=params)

    def get_event(self, event_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single check-in event.

        Args:
            event_id: Event ID
            params: Query parameters

        Returns:
            Event data
        """
        return self.get("events", event_id, params=params)

    def create_event(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new check-in event.

        Args:
            data: Event data
            params: Query parameters

        Returns:
            Created event
        """
        return self.create("events", data, params=params)

    def update_event(self, event_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a check-in event.

        Args:
            event_id: Event ID
            data: Updated event data
            params: Query parameters

        Returns:
            Updated event
        """
        return self.update("events", event_id, data, params=params)

    def delete_event(self, event_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a check-in event.

        Args:
            event_id: Event ID
            params: Query parameters
        """
        self.delete("events", event_id, params=params)

    def list_locations(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all check-in locations.

        Args:
            params: Query parameters

        Returns:
            List of locations
        """
        return self.list("locations", params=params)

    def get_location(self, location_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single check-in location.

        Args:
            location_id: Location ID
            params: Query parameters

        Returns:
            Location data
        """
        return self.get("locations", location_id, params=params)

    def create_location(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new check-in location.

        Args:
            data: Location data
            params: Query parameters

        Returns:
            Created location
        """
        return self.create("locations", data, params=params)

    def update_location(self, location_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a check-in location.

        Args:
            location_id: Location ID
            data: Updated location data
            params: Query parameters

        Returns:
            Updated location
        """
        return self.update("locations", location_id, data, params=params)

    def delete_location(self, location_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a check-in location.

        Args:
            location_id: Location ID
            params: Query parameters
        """
        self.delete("locations", location_id, params=params)

    def get_event_locations(self, event_id: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get locations for an event.

        Args:
            event_id: Event ID
            params: Query parameters

        Returns:
            List of locations
        """
        return self.get_related("events", event_id, "locations", params=params)
