"""
Pydantic schemas for ticketing endpoints validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class CreateTicketRequest(BaseModel):
    """Schema for creating a new ticket request."""
    user_id: int = Field(..., gt=0, description="User ID must be a positive integer")
    message: str = Field(..., min_length=1, max_length=1000, description="Initial message for the ticket")
    booking_id: Optional[int] = Field(None, gt=0, description="Optional booking ID")

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()


class AddMessageRequest(BaseModel):
    """Schema for adding a message to a ticket."""
    message: str = Field(..., min_length=1, max_length=1000, description="Message to add to the ticket")

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()


class TicketResponse(BaseModel):
    """Schema for ticket response serialization."""
    id: int
    user_id: int
    booking_id: Optional[int] = None
    chat_content: str
    is_resolved: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class TicketListResponse(BaseModel):
    """Schema for list of tickets response."""
    tickets: List[TicketResponse]
    total_count: int


class TicketIdRequest(BaseModel):
    """Schema for validating ticket ID."""
    ticket_id: int = Field(..., gt=0, description="Ticket ID must be a positive integer")


class UserIdRequest(BaseModel):
    """Schema for validating user ID."""
    user_id: int = Field(..., gt=0, description="User ID must be a positive integer")