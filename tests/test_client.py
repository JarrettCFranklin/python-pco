"""Tests for PCOClient."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from pco.client import PCOClient
from pco.exceptions import PCONotFoundError, PCORateLimitError, PCOValidationError


def test_client_initialization_with_oauth(mock_oauth_client):
    """Test PCOClient initialization with OAuth client."""
    client = PCOClient(oauth_client=mock_oauth_client)
    assert client.oauth_client == mock_oauth_client
    assert client.base_url == "https://api.planningcenteronline.com"


def test_client_initialization_with_token(mock_token):
    """Test PCOClient initialization with token."""
    client = PCOClient(token=mock_token)
    assert client._token == mock_token


def test_client_initialization_error_both_auth():
    """Test that providing both oauth_client and token raises error."""
    mock_oauth = MagicMock()
    mock_token = MagicMock()
    with pytest.raises(ValueError, match="Cannot provide both"):
        PCOClient(oauth_client=mock_oauth, token=mock_token)


def test_get_request_success(pco_client, sample_person_data):
    """Test successful GET request."""
    with patch.object(pco_client._http_client, "request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.json.return_value = sample_person_data
        mock_response.content = b'{"data": {}}'
        mock_request.return_value = mock_response

        result = pco_client.get("/people/v2/people/123")
        assert result == sample_person_data


def test_get_request_not_found(pco_client):
    """Test GET request with 404 error."""
    with patch.object(pco_client._http_client, "request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.is_success = False
        mock_response.json.return_value = {"error": "Not found"}
        mock_response.content = b'{"error": "Not found"}'
        mock_request.return_value = mock_response

        with pytest.raises(PCONotFoundError):
            pco_client.get("/people/v2/people/999")


def test_get_request_rate_limit(pco_client):
    """Test GET request with rate limit error."""
    with patch.object(pco_client._http_client, "request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.is_success = False
        mock_response.json.return_value = {"error": "Rate limit exceeded"}
        mock_response.content = b'{"error": "Rate limit exceeded"}'
        mock_request.return_value = mock_response

        with pytest.raises(PCORateLimitError):
            pco_client.get("/people/v2/people")


def test_post_request_success(pco_client, sample_person_data):
    """Test successful POST request."""
    with patch.object(pco_client._http_client, "request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.is_success = True
        mock_response.json.return_value = sample_person_data
        mock_response.content = b'{"data": {}}'
        mock_request.return_value = mock_response

        data = {"data": {"type": "Person", "attributes": {"first_name": "John"}}}
        result = pco_client.post("/people/v2/people", json=data)
        assert result == sample_person_data


def test_client_context_manager(pco_client):
    """Test PCOClient as context manager."""
    with pco_client as client:
        assert client == pco_client
    # Verify close was called
    pco_client._http_client.close.assert_called_once()
