"""
Base schemas for common validation patterns.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        str_strip_whitespace=True
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    created_at: datetime


class ResponseSchema(BaseSchema):
    """Base response schema."""

    success: bool = True
    message: Optional[str] = None


class PaginationSchema(BaseSchema):
    """Pagination parameters schema."""

    page: int = 1
    limit: int = 20

    @field_validator('page')
    @classmethod
    def validate_page(cls, v):
        if v < 1:
            raise ValueError('Page must be >= 1')
        return v

    @field_validator('limit')
    @classmethod
    def validate_limit(cls, v):
        if v < 1:
            raise ValueError('Limit must be >= 1')
        if v > 100:
            raise ValueError('Limit must be <= 100')
        return v


class PaginatedResponseSchema(ResponseSchema):
    """Paginated response schema."""

    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool
