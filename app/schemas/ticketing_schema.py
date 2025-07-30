"""
Pydantic schemas for ticketing endpoints validation and serialization.
Following clean code principles with clear, beginner-friendly validation.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CreateTicketRequest(BaseModel):
    """
    Schema for creating a new support ticket.

    This validates that we have all required information to create a ticket:
    - user_id: Who is creating the ticket
    - message: What is the issue/question
    - booking_id: Optional - if related to a specific booking
    """
    user_id: int = Field(..., gt=0, description="Valid user ID who is creating the ticket")
    message: str = Field(..., min_length=1, max_length=5000, description="Initial ticket message describing the issue")
    booking_id: Optional[int] = Field(default=None, description="Optional booking ID if ticket is booking-related")

    @field_validator('message')
    @classmethod
    def validate_message_content(cls, value):
        """Ensure message is not just empty or whitespace."""
        if not value or not value.strip():
            raise ValueError('Message cannot be empty or contain only whitespace')
        return value.strip()

    @field_validator('booking_id')
    @classmethod
    def validate_booking_id_positive(cls, value):
        """Ensure booking ID is positive if provided."""
        if value is not None and value <= 0:
            raise ValueError('Booking ID must be a positive integer')
        return value


class AddMessageRequest(BaseModel):
    """
    Schema for adding a new message to an existing ticket.

    Used when customer or support adds a reply to the conversation.
    """
    message: str = Field(..., min_length=1, max_length=2000, description="Message content to add to the ticket conversation")

    @field_validator('message')
    @classmethod
    def validate_message_content(cls, value):
        """Ensure message is meaningful and not empty."""
        if not value or not value.strip():
            raise ValueError('Message cannot be empty or contain only whitespace')
        return value.strip()


class TicketIdRequest(BaseModel):
    """Schema for validating ticket ID parameters in URLs."""
    ticket_id: int = Field(..., gt=0, description="Valid ticket ID")

    @field_validator('ticket_id')
    @classmethod
    def validate_ticket_id_positive(cls, value):
        """Ensure ticket ID is a positive integer."""
        if value <= 0:
            raise ValueError('Ticket ID must be a positive integer')
        return value


class UserIdRequest(BaseModel):
    """Schema for validating user ID parameters in URLs."""
    user_id: int = Field(..., gt=0, description="Valid user ID")

    @field_validator('user_id')
    @classmethod
    def validate_user_id_positive(cls, value):
        """Ensure user ID is a positive integer."""
        if value <= 0:
            raise ValueError('User ID must be a positive integer')
        return value


class TicketResponse(BaseModel):
    """
    Schema for ticket response data.

    This represents how a ticket looks when returned from the API.
    Matches the database model structure but ensures safe serialization.
    """
    id: int
    user_id: int
    booking_id: Optional[int] = None
    chat_content: str
    is_resolved: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def serialize_datetime_safely(cls, value):
        """
        Safe datetime serialization for schema validation.
        Prevents fromisoformat errors by handling various input types.
        """
        if value is None:
            return None

        # If already a string, validate it's a proper ISO format
        if isinstance(value, str):
            try:
                # Try to parse it to ensure it's valid
                from datetime import datetime
                datetime.fromisoformat(value.replace('Z', '+00:00'))
                return value
            except ValueError:
                # If invalid string format, return None
                return None

        # If it's a datetime object, convert to ISO string
        if hasattr(value, 'isoformat'):
            try:
                return value.isoformat()
            except Exception:
                return None

        # For any other type, try string conversion
        return str(value) if value is not None else None

class TicketListResponse(BaseModel):
    """
    Schema for returning multiple tickets with metadata.

    Used by endpoints that return lists of tickets (user tickets, open tickets, etc.)
    """
    tickets: List[TicketResponse]
    total_count: int

    @field_validator('total_count')
    @classmethod
    def validate_count_non_negative(cls, value):
        """Ensure total count makes sense."""
        if value < 0:
            raise ValueError('Total count cannot be negative')
        return value


class TicketStatsResponse(BaseModel):
    """
    Schema for ticket statistics data.

    Used by the stats endpoint to show ticket counts.
    """
    total_tickets: int
    open_tickets: int
    resolved_tickets: int

    @field_validator('total_tickets', 'open_tickets', 'resolved_tickets')
    @classmethod
    def validate_counts_non_negative(cls, value):
        """Ensure all counts are non-negative."""
        if value < 0:
            raise ValueError('Ticket counts must be non-negative')
        return value


# Legacy compatibility schemas - keeping these for backward compatibility
class TicketCreateRequest(CreateTicketRequest):
    """Alias for backward compatibility with existing code."""
    pass


class TicketUpdateRequest(AddMessageRequest):
    """Alias for backward compatibility with existing code."""
    pass


class UpdateTicketStatusRequest(BaseModel):
    """Schema for updating ticket resolution status."""
    is_resolved: bool = Field(..., description="Set ticket resolution status")


class ResolveTicketRequest(BaseModel):
    """Schema for resolving tickets - currently no additional data needed."""
    pass


class ReopenTicketRequest(BaseModel):
    """Schema for reopening tickets - currently no additional data needed."""
    pass