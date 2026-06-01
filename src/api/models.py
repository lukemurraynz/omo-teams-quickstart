"""LinkSnap Pydantic models for request/response contracts."""

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class CreateLinkRequest(BaseModel):
    """Request body for creating a shortened URL."""

    destination_url: HttpUrl
    tenant_id: str = Field(default="default", max_length=64)
    created_by: str | None = Field(default=None, max_length=128)


class LinkResponse(BaseModel):
    """Response body for a short link."""

    short_code: str
    destination_url: str
    created_at: str
    click_count: int = 0


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    error: str
    message: str
