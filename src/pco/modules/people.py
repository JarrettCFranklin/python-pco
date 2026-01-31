"""People API module for PCO."""

from typing import Any

from pco.modules.base import BaseModule


class PeopleModule(BaseModule):
    """Module for interacting with PCO People API."""

    def __init__(self, client):
        super().__init__(client, "/people/v2")

    def list_people(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all people.

        Args:
            params: Query parameters (e.g., per_page, offset, where, order)

        Returns:
            List of people
        """
        return self.list("people", params=params)

    def get_person(self, person_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single person.

        Args:
            person_id: Person ID
            params: Query parameters

        Returns:
            Person data
        """
        return self.get("people", person_id, params=params)

    def create_person(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new person.

        Args:
            data: Person data
            params: Query parameters

        Returns:
            Created person
        """
        return self.create("people", data, params=params)

    def update_person(self, person_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a person.

        Args:
            person_id: Person ID
            data: Updated person data
            params: Query parameters

        Returns:
            Updated person
        """
        return self.update("people", person_id, data, params=params)

    def delete_person(self, person_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a person.

        Args:
            person_id: Person ID
            params: Query parameters
        """
        self.delete("people", person_id, params=params)

    def list_households(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all households.

        Args:
            params: Query parameters

        Returns:
            List of households
        """
        return self.list("households", params=params)

    def get_household(self, household_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single household.

        Args:
            household_id: Household ID
            params: Query parameters

        Returns:
            Household data
        """
        return self.get("households", household_id, params=params)

    def create_household(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new household.

        Args:
            data: Household data
            params: Query parameters

        Returns:
            Created household
        """
        return self.create("households", data, params=params)

    def update_household(self, household_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a household.

        Args:
            household_id: Household ID
            data: Updated household data
            params: Query parameters

        Returns:
            Updated household
        """
        return self.update("households", household_id, data, params=params)

    def delete_household(self, household_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a household.

        Args:
            household_id: Household ID
            params: Query parameters
        """
        self.delete("households", household_id, params=params)

    def get_person_households(self, person_id: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get households for a person.

        Args:
            person_id: Person ID
            params: Query parameters

        Returns:
            List of households
        """
        return self.get_related("people", person_id, "households", params=params)

    def get_household_people(self, household_id: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get people in a household.

        Args:
            household_id: Household ID
            params: Query parameters

        Returns:
            List of people
        """
        return self.get_related("households", household_id, "people", params=params)
