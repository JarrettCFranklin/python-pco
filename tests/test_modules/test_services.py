"""Tests for ServicesModule."""

from unittest.mock import patch

import pytest

from pco.client import PCOClient
from pco.modules.services import ServicesModule


@pytest.fixture
def services_module(mock_oauth_client):
    """Create a ServicesModule instance for testing."""
    client = PCOClient(oauth_client=mock_oauth_client)
    return ServicesModule(client)


def test_list_plans(services_module):
    """Test listing service plans."""
    plans_data = {"data": [{"id": "1", "type": "Plan"}]}
    with patch.object(services_module.client, "get") as mock_get:
        mock_get.return_value = plans_data
        result = services_module.list_plans()
        assert result == plans_data
        mock_get.assert_called_once_with("/services/v2/plans", params=None)


def test_get_plan(services_module):
    """Test getting a single plan."""
    plan_data = {"data": {"id": "1", "type": "Plan"}}
    with patch.object(services_module.client, "get") as mock_get:
        mock_get.return_value = plan_data
        result = services_module.get_plan("1")
        assert result == plan_data
        mock_get.assert_called_once_with("/services/v2/plans/1", params=None)


def test_get_plan_items(services_module):
    """Test getting items for a plan."""
    items_data = {"data": [{"id": "1", "type": "Item"}]}
    with patch.object(services_module.client, "get") as mock_get:
        mock_get.return_value = items_data
        result = services_module.get_plan_items("1")
        assert result == items_data
        mock_get.assert_called_once_with("/services/v2/plans/1/items", params=None)
