"""Services API module for PCO."""

from typing import Any

from pco.modules.base import BaseModule


class ServicesModule(BaseModule):
    """Module for interacting with PCO Services API."""

    def __init__(self, client):
        super().__init__(client, "/services/v2")

    def list_plans(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all service plans.

        Args:
            params: Query parameters (e.g., per_page, offset, where, order)

        Returns:
            List of service plans
        """
        return self.list("plans", params=params)

    def get_plan(self, plan_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single service plan.

        Args:
            plan_id: Plan ID
            params: Query parameters

        Returns:
            Plan data
        """
        return self.get("plans", plan_id, params=params)

    def create_plan(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new service plan.

        Args:
            data: Plan data
            params: Query parameters

        Returns:
            Created plan
        """
        return self.create("plans", data, params=params)

    def update_plan(self, plan_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a service plan.

        Args:
            plan_id: Plan ID
            data: Updated plan data
            params: Query parameters

        Returns:
            Updated plan
        """
        return self.update("plans", plan_id, data, params=params)

    def delete_plan(self, plan_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a service plan.

        Args:
            plan_id: Plan ID
            params: Query parameters
        """
        self.delete("plans", plan_id, params=params)

    def list_teams(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all teams.

        Args:
            params: Query parameters

        Returns:
            List of teams
        """
        return self.list("teams", params=params)

    def get_team(self, team_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single team.

        Args:
            team_id: Team ID
            params: Query parameters

        Returns:
            Team data
        """
        return self.get("teams", team_id, params=params)

    def create_team(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new team.

        Args:
            data: Team data
            params: Query parameters

        Returns:
            Created team
        """
        return self.create("teams", data, params=params)

    def update_team(self, team_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a team.

        Args:
            team_id: Team ID
            data: Updated team data
            params: Query parameters

        Returns:
            Updated team
        """
        return self.update("teams", team_id, data, params=params)

    def delete_team(self, team_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a team.

        Args:
            team_id: Team ID
            params: Query parameters
        """
        self.delete("teams", team_id, params=params)

    def list_times(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all times.

        Args:
            params: Query parameters

        Returns:
            List of times
        """
        return self.list("times", params=params)

    def get_time(self, time_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single time.

        Args:
            time_id: Time ID
            params: Query parameters

        Returns:
            Time data
        """
        return self.get("times", time_id, params=params)

    def get_plan_items(self, plan_id: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get items for a plan.

        Args:
            plan_id: Plan ID
            params: Query parameters

        Returns:
            List of items
        """
        return self.get_related("plans", plan_id, "items", params=params)

    def get_plan_teams(self, plan_id: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get teams for a plan.

        Args:
            plan_id: Plan ID
            params: Query parameters

        Returns:
            List of teams
        """
        return self.get_related("plans", plan_id, "teams", params=params)
