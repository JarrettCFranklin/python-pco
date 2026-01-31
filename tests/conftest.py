"""Pytest configuration and fixtures."""

from unittest.mock import MagicMock

import pytest

from pco.auth import OAuth2Client, OAuth2Token
from pco.client import PCOClient


@pytest.fixture
def mock_token():
    """Create a mock OAuth2Token."""
    return OAuth2Token(
        access_token="test_access_token",
        token_type="Bearer",
        expires_in=3600,
        refresh_token="test_refresh_token",
    )


@pytest.fixture
def mock_oauth_client(mock_token):
    """Create a mock OAuth2Client."""
    client = MagicMock(spec=OAuth2Client)
    client.get_authorization_header.return_value = {"Authorization": "Bearer test_access_token"}
    client.get_token.return_value = mock_token
    return client


@pytest.fixture
def mock_http_client():
    """Create a mock httpx.Client."""
    return MagicMock()


@pytest.fixture
def pco_client(mock_oauth_client):
    """Create a PCOClient instance for testing."""
    return PCOClient(oauth_client=mock_oauth_client)


@pytest.fixture
def sample_person_data():
    """Sample person data for testing."""
    return {
        "data": {
            "id": "123",
            "type": "Person",
            "attributes": {
                "first_name": "John",
                "last_name": "Doe",
                "name": "John Doe",
            },
        }
    }


@pytest.fixture
def sample_people_list():
    """Sample people list for testing."""
    return {
        "data": [
            {
                "id": "123",
                "type": "Person",
                "attributes": {
                    "first_name": "John",
                    "last_name": "Doe",
                },
            },
            {
                "id": "456",
                "type": "Person",
                "attributes": {
                    "first_name": "Jane",
                    "last_name": "Smith",
                },
            },
        ]
    }
