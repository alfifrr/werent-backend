"""
Message schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import Field, field_validator
from app.schemas.base_schema import BaseSchema, ResponseSchema


class MessageCreateSchema(BaseSchema):
    """Schema for creating a new message."""

    receiver_id: int = Field(..., description="ID of the message receiver")
    content: str = Field(..., min_length=1, max_length=1000, description="Message content")

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate message content."""
        if not v.strip():
            raise ValueError('Message content cannot be empty')
        return v.strip()


class MessageUpdateSchema(BaseSchema):
    """Schema for updating message (mark as read/unread)."""

    is_read: bool = Field(..., description="Read status")


class MessageResponseSchema(BaseSchema):
    """Schema for message response."""

    id: int
    content: str
    sent_at: datetime
    is_read: bool
    sender_id: int
    receiver_id: int


class MessageDetailResponseSchema(MessageResponseSchema):
    """Extended message response with user details."""

    sender: Optional[dict] = None
    receiver: Optional[dict] = None


class MessageListResponseSchema(ResponseSchema):
    """Schema for message list response."""

    messages: List[MessageResponseSchema]
    total: int


class ConversationSchema(BaseSchema):
    """Schema for conversation between two users."""

    partner_id: int = Field(..., description="ID of conversation partner")
    limit: Optional[int] = Field(50, ge=1, le=100, description="Number of messages to retrieve")


class ConversationResponseSchema(BaseSchema):
    """Schema for conversation response."""

    partner_id: int
    partner: Optional[dict] = None
    messages: List[MessageResponseSchema]
    unread_count: int
    total_messages: int


class ConversationListResponseSchema(ResponseSchema):
    """Schema for user's conversations list."""

    conversations: List[dict]
    total: int


class MessageSearchSchema(BaseSchema):
    """Schema for message search parameters."""

    query: str = Field(..., min_length=2, max_length=100, description="Search query")
    partner_id: Optional[int] = Field(None, description="Search within specific conversation")
    limit: Optional[int] = Field(20, ge=1, le=100, description="Number of results")


class MessageStatsSchema(BaseSchema):
    """Schema for message statistics."""

    messages_sent: int
    messages_received: int
    unread_messages: int
    total_conversations: int


class UnreadMessageCountSchema(BaseSchema):
    """Schema for unread message count."""

    count: int


class MessageMarkReadSchema(BaseSchema):
    """Schema for marking multiple messages as read."""

    message_ids: List[int] = Field(..., description="List of message IDs to mark as read")

    @field_validator('message_ids')
    @classmethod
    def validate_message_ids(cls, v):
        """Validate message IDs list."""
        if len(v) == 0:
            raise ValueError('At least one message ID is required')
        if len(v) > 100:
            raise ValueError('Cannot mark more than 100 messages at once')
        return v
