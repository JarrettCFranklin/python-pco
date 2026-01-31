"""Giving API module for PCO."""

from typing import Any

from pco.modules.base import BaseModule


class GivingModule(BaseModule):
    """Module for interacting with PCO Giving API."""

    def __init__(self, client):
        super().__init__(client, "/giving/v2")

    def list_funds(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all giving funds.

        Args:
            params: Query parameters (e.g., per_page, offset, where, order)

        Returns:
            List of funds
        """
        return self.list("funds", params=params)

    def get_fund(self, fund_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single giving fund.

        Args:
            fund_id: Fund ID
            params: Query parameters

        Returns:
            Fund data
        """
        return self.get("funds", fund_id, params=params)

    def create_fund(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new giving fund.

        Args:
            data: Fund data
            params: Query parameters

        Returns:
            Created fund
        """
        return self.create("funds", data, params=params)

    def update_fund(self, fund_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a giving fund.

        Args:
            fund_id: Fund ID
            data: Updated fund data
            params: Query parameters

        Returns:
            Updated fund
        """
        return self.update("funds", fund_id, data, params=params)

    def delete_fund(self, fund_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a giving fund.

        Args:
            fund_id: Fund ID
            params: Query parameters
        """
        self.delete("funds", fund_id, params=params)

    def list_batches(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all giving batches.

        Args:
            params: Query parameters

        Returns:
            List of batches
        """
        return self.list("batches", params=params)

    def get_batch(self, batch_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single giving batch.

        Args:
            batch_id: Batch ID
            params: Query parameters

        Returns:
            Batch data
        """
        return self.get("batches", batch_id, params=params)

    def create_batch(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new giving batch.

        Args:
            data: Batch data
            params: Query parameters

        Returns:
            Created batch
        """
        return self.create("batches", data, params=params)

    def update_batch(self, batch_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a giving batch.

        Args:
            batch_id: Batch ID
            data: Updated batch data
            params: Query parameters

        Returns:
            Updated batch
        """
        return self.update("batches", batch_id, data, params=params)

    def delete_batch(self, batch_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a giving batch.

        Args:
            batch_id: Batch ID
            params: Query parameters
        """
        self.delete("batches", batch_id, params=params)

    def list_donations(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all donations.

        Args:
            params: Query parameters

        Returns:
            List of donations
        """
        return self.list("donations", params=params)

    def get_donation(self, donation_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single donation.

        Args:
            donation_id: Donation ID
            params: Query parameters

        Returns:
            Donation data
        """
        return self.get("donations", donation_id, params=params)

    def get_batch_donations(self, batch_id: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get donations for a batch.

        Args:
            batch_id: Batch ID
            params: Query parameters

        Returns:
            List of donations
        """
        return self.get_related("batches", batch_id, "donations", params=params)
