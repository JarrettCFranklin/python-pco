"""Tests for PeopleModule."""

from unittest.mock import MagicMock, patch

import pytest

from pco.client import PCOClient
from pco.modules.people import PeopleModule


@pytest.fixture
def people_module(mock_oauth_client):
    """Create a PeopleModule instance for testing."""
    client = PCOClient(oauth_client=mock_oauth_client)
    return PeopleModule(client)


def test_list_people(people_module, sample_people_list):
    """Test listing people."""
    with patch.object(people_module.client, "get") as mock_get:
        mock_get.return_value = sample_people_list
        result = people_module.list_people()
        assert result == sample_people_list
        mock_get.assert_called_once_with("/people/v2/people", params=None)


def test_get_person(people_module, sample_person_data):
    """Test getting a single person."""
    with patch.object(people_module.client, "get") as mock_get:
        mock_get.return_value = sample_person_data
        result = people_module.get_person("123")
        assert result == sample_person_data
        mock_get.assert_called_once_with("/people/v2/people/123", params=None)


def test_create_person(people_module, sample_person_data):
    """Test creating a person."""
    with patch.object(people_module.client, "post") as mock_post:
        mock_post.return_value = sample_person_data
        data = {"data": {"type": "Person", "attributes": {"first_name": "John"}}}
        result = people_module.create_person(data)
        assert result == sample_person_data
        mock_post.assert_called_once_with("/people/v2/people", json=data, params=None)


def test_update_person(people_module, sample_person_data):
    """Test updating a person."""
    with patch.object(people_module.client, "patch") as mock_patch:
        mock_patch.return_value = sample_person_data
        data = {"data": {"attributes": {"first_name": "Jane"}}}
        result = people_module.update_person("123", data)
        assert result == sample_person_data
        mock_patch.assert_called_once_with("/people/v2/people/123", json=data, params=None)


def test_delete_person(people_module):
    """Test deleting a person."""
    with patch.object(people_module.client, "delete") as mock_delete:
        people_module.delete_person("123")
        mock_delete.assert_called_once_with("/people/v2/people/123", params=None)


def test_list_households(people_module):
    """Test listing households."""
    households_data = {"data": [{"id": "1", "type": "Household"}]}
    with patch.object(people_module.client, "get") as mock_get:
        mock_get.return_value = households_data
        result = people_module.list_households()
        assert result == households_data
        mock_get.assert_called_once_with("/people/v2/households", params=None)


def test_get_person_households(people_module):
    """Test getting households for a person."""
    households_data = {"data": [{"id": "1", "type": "Household"}]}
    with patch.object(people_module.client, "get") as mock_get:
        mock_get.return_value = households_data
        result = people_module.get_person_households("123")
        assert result == households_data
        mock_get.assert_called_once_with("/people/v2/people/123/households", params=None)
