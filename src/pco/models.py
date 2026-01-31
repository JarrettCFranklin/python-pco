"""Pydantic models for PCO API requests and responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PCOData(BaseModel):
    """Base model for PCO API data objects."""

    id: str
    type: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    relationships: dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class PCOResponse(BaseModel):
    """Base model for PCO API responses."""

    data: PCOData | list[PCOData] | None = None
    included: list[PCOData] = Field(default_factory=list)
    meta: dict[str, Any] = Field(default_factory=dict)
    links: dict[str, str] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class PCOPerson(BaseModel):
    """Model for PCO Person resource."""

    id: str
    first_name: str | None = None
    last_name: str | None = None
    name: str | None = None
    given_name: str | None = None
    middle_name: str | None = None
    nickname: str | None = None
    email_addresses: list[dict[str, Any]] = Field(default_factory=list)
    phone_numbers: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        extra = "allow"


class PCOHousehold(BaseModel):
    """Model for PCO Household resource."""

    id: str
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        extra = "allow"


class PCOServicePlan(BaseModel):
    """Model for PCO Service Plan resource."""

    id: str
    series_title: str | None = None
    title: str | None = None
    dates: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        extra = "allow"


class PCOCheckInEvent(BaseModel):
    """Model for PCO Check-In Event resource."""

    id: str
    name: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        extra = "allow"


class PCOGivingFund(BaseModel):
    """Model for PCO Giving Fund resource."""

    id: str
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        extra = "allow"


class PCOResourceItem(BaseModel):
    """Model for PCO Resource Item resource."""

    id: str
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        extra = "allow"


def parse_pco_response(response: dict[str, Any] | list[Any]) -> PCOResponse:
    """Parse PCO API response into PCOResponse model."""
    if isinstance(response, list):
        return PCOResponse(data=response)
    return PCOResponse(**response)


def extract_attributes(data: PCOData | dict[str, Any]) -> dict[str, Any]:
    """Extract attributes from PCO data object."""
    if isinstance(data, dict):
        return data.get("attributes", {})
    return data.attributes


def parse_datetime(value: str | None) -> datetime | None:
    """Parse ISO 8601 datetime string."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
