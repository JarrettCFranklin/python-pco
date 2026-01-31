"""Resources API module for PCO."""

from typing import Any

from pco.modules.base import BaseModule


class ResourcesModule(BaseModule):
    """Module for interacting with PCO Resources API."""

    def __init__(self, client):
        super().__init__(client, "/resources/v2")

    def list_items(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all resource items.

        Args:
            params: Query parameters (e.g., per_page, offset, where, order)

        Returns:
            List of items
        """
        return self.list("items", params=params)

    def get_item(self, item_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single resource item.

        Args:
            item_id: Item ID
            params: Query parameters

        Returns:
            Item data
        """
        return self.get("items", item_id, params=params)

    def create_item(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new resource item.

        Args:
            data: Item data
            params: Query parameters

        Returns:
            Created item
        """
        return self.create("items", data, params=params)

    def update_item(self, item_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a resource item.

        Args:
            item_id: Item ID
            data: Updated item data
            params: Query parameters

        Returns:
            Updated item
        """
        return self.update("items", item_id, data, params=params)

    def delete_item(self, item_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a resource item.

        Args:
            item_id: Item ID
            params: Query parameters
        """
        self.delete("items", item_id, params=params)

    def list_checkouts(self, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """List all checkouts.

        Args:
            params: Query parameters

        Returns:
            List of checkouts
        """
        return self.list("checkouts", params=params)

    def get_checkout(self, checkout_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get a single checkout.

        Args:
            checkout_id: Checkout ID
            params: Query parameters

        Returns:
            Checkout data
        """
        return self.get("checkouts", checkout_id, params=params)

    def create_checkout(self, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a new checkout.

        Args:
            data: Checkout data
            params: Query parameters

        Returns:
            Created checkout
        """
        return self.create("checkouts", data, params=params)

    def update_checkout(self, checkout_id: str, data: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Update a checkout.

        Args:
            checkout_id: Checkout ID
            data: Updated checkout data
            params: Query parameters

        Returns:
            Updated checkout
        """
        return self.update("checkouts", checkout_id, data, params=params)

    def delete_checkout(self, checkout_id: str, params: dict[str, Any] | None = None) -> None:
        """Delete a checkout.

        Args:
            checkout_id: Checkout ID
            params: Query parameters
        """
        self.delete("checkouts", checkout_id, params=params)

    def get_item_checkouts(self, item_id: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get checkouts for an item.

        Args:
            item_id: Item ID
            params: Query parameters

        Returns:
            List of checkouts
        """
        return self.get_related("items", item_id, "checkouts", params=params)
