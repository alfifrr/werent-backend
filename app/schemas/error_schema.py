"""
Error schemas for API error responses.
"""

from typing import Optional, List, Dict, Any
from pydantic import Field
from app.schemas.base_schema import BaseSchema


class ErrorSchema(BaseSchema):
    """Base error schema."""

    error: str = Field(..., description="Error type/code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class ValidationErrorSchema(ErrorSchema):
    """Schema for validation errors."""

    error: str = "validation_error"
    field_errors: Optional[Dict[str, List[str]]] = Field(None, description="Field-specific validation errors")


class NotFoundErrorSchema(ErrorSchema):
    """Schema for resource not found errors."""

    error: str = "not_found"
    resource: Optional[str] = Field(None, description="Resource type that was not found")
    resource_id: Optional[int] = Field(None, description="ID of the resource that was not found")


class UnauthorizedErrorSchema(ErrorSchema):
    """Schema for unauthorized access errors."""

    error: str = "unauthorized"
    required_permission: Optional[str] = Field(None, description="Required permission for this action")


class ForbiddenErrorSchema(ErrorSchema):
    """Schema for forbidden access errors."""

    error: str = "forbidden"
    reason: Optional[str] = Field(None, description="Reason for forbidden access")


class ConflictErrorSchema(ErrorSchema):
    """Schema for conflict errors."""

    error: str = "conflict"
    conflicting_resource: Optional[str] = Field(None, description="Resource that conflicts")


class BusinessLogicErrorSchema(ErrorSchema):
    """Schema for business logic errors."""

    error: str = "business_logic_error"
    error_code: Optional[str] = Field(None, description="Specific business logic error code")


class BookingErrorSchema(BusinessLogicErrorSchema):
    """Schema for booking-specific errors."""

    error: str = "booking_error"
    booking_id: Optional[int] = Field(None, description="Related booking ID")
    item_id: Optional[int] = Field(None, description="Related item ID")


class ItemUnavailableErrorSchema(ErrorSchema):
    """Schema for item unavailability errors."""

    error: str = "item_unavailable"
    item_id: int = Field(..., description="ID of the unavailable item")
    reason: str = Field(..., description="Reason for unavailability")
    available_dates: Optional[List[str]] = Field(None, description="Next available dates")


class RateLimitErrorSchema(ErrorSchema):
    """Schema for rate limiting errors."""

    error: str = "rate_limit_exceeded"
    retry_after: Optional[int] = Field(None, description="Seconds to wait before retrying")
    limit: Optional[int] = Field(None, description="Rate limit threshold")


class InternalServerErrorSchema(ErrorSchema):
    """Schema for internal server errors."""

    error: str = "internal_server_error"
    error_id: Optional[str] = Field(None, description="Unique error identifier for tracking")
