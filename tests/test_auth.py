"""Tests for OAuth2Client."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from pco.auth import OAuth2Client, OAuth2Token
from pco.exceptions import PCOAuthError


def test_oauth2_token_initialization():
    """Test OAuth2Token initialization."""
    token = OAuth2Token(
        access_token="test_token",
        token_type="Bearer",
        expires_in=3600,
        refresh_token="refresh_token",
    )
    assert token.access_token == "test_token"
    assert token.token_type == "Bearer"
    assert token.refresh_token == "refresh_token"


def test_oauth2_token_to_header():
    """Test OAuth2Token to_header method."""
    token = OAuth2Token(access_token="test_token", token_type="Bearer")
    header = token.to_header()
    assert header == {"Authorization": "Bearer test_token"}


def test_oauth2_token_expiration():
    """Test OAuth2Token expiration checking."""
    import time

    token = OAuth2Token(access_token="test_token", expires_in=1)
    assert not token.is_expired()
    time.sleep(2)
    assert token.is_expired()


def test_oauth2_client_initialization():
    """Test OAuth2Client initialization."""
    client = OAuth2Client(
        client_id="test_id",
        client_secret="test_secret",
        redirect_uri="http://localhost:8000/callback",
    )
    assert client.client_id == "test_id"
    assert client.client_secret == "test_secret"
    assert client.redirect_uri == "http://localhost:8000/callback"


def test_get_authorization_url():
    """Test getting authorization URL."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    url = client.get_authorization_url()
    assert "client_id=test_id" in url
    assert "response_type=code" in url
    assert "api.planningcenteronline.com/oauth/authorize" in url


def test_get_authorization_url_with_state():
    """Test getting authorization URL with state parameter."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    url = client.get_authorization_url(state="test_state")
    assert "state=test_state" in url


def test_exchange_code_for_token():
    """Test exchanging code for token."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    with patch.object(client._http_client, "post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh",
        }
        mock_post.return_value = mock_response

        token = client.exchange_code_for_token("auth_code")
        assert token.access_token == "new_token"
        assert token.refresh_token == "new_refresh"


def test_refresh_access_token():
    """Test refreshing access token."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    token = OAuth2Token(
        access_token="old_token",
        refresh_token="refresh_token",
        expires_in=3600,
    )
    client.set_token(token)

    with patch.object(client._http_client, "post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_token",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        mock_post.return_value = mock_response

        new_token = client.refresh_access_token()
        assert new_token.access_token == "new_token"


def test_refresh_access_token_no_refresh_token():
    """Test refreshing token without refresh token raises error."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    token = OAuth2Token(access_token="token", expires_in=3600)
    client.set_token(token)

    with pytest.raises(ValueError, match="No refresh token"):
        client.refresh_access_token()


def test_get_authorization_header():
    """Test getting authorization header."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    token = OAuth2Token(access_token="test_token")
    client.set_token(token)

    header = client.get_authorization_header()
    assert header == {"Authorization": "Bearer test_token"}


def test_get_authorization_header_no_token():
    """Test getting authorization header without token raises error."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    with pytest.raises(ValueError, match="No token available"):
        client.get_authorization_header()


def test_oauth2_client_context_manager():
    """Test OAuth2Client as context manager."""
    client = OAuth2Client(client_id="test_id", client_secret="test_secret")
    with client as c:
        assert c == client
    # Verify close was called
    client._http_client.close.assert_called_once()
