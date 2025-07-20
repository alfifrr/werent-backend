"""
User schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.base_schema import BaseSchema, TimestampMixin, ResponseSchema


class UserCreateSchema(BaseSchema):
    """Schema for creating a new user."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    name: str = Field(..., min_length=2, max_length=100, description="User full name")
    phone: Optional[str] = Field(None, max_length=20, description="User phone number")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            # Remove spaces and special characters
            cleaned = ''.join(filter(str.isdigit, v))
            if len(cleaned) < 10 or len(cleaned) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
        return v


class UserLoginSchema(BaseSchema):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserUpdateSchema(BaseSchema):
    """Schema for updating user profile."""

    name: Optional[str] = Field(None, min_length=2, max_length=100, description="User full name")
    phone: Optional[str] = Field(None, max_length=20, description="User phone number")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            cleaned = ''.join(filter(str.isdigit, v))
            if len(cleaned) < 10 or len(cleaned) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
        return v


class UserPasswordUpdateSchema(BaseSchema):
    """Schema for updating user password."""

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'new_password' in values.data and v != values.data['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserResponseSchema(BaseSchema, TimestampMixin):
    """Schema for user response."""

    id: int
    email: EmailStr
    name: str
    phone: Optional[str]
    is_verified: bool
    avg_rating: float


class UserProfileResponseSchema(UserResponseSchema):
    """Extended user profile response with statistics."""

    total_items: Optional[int] = None
    total_bookings: Optional[int] = None
    total_reviews: Optional[int] = None
    member_since: Optional[str] = None


class UserListResponseSchema(ResponseSchema):
    """Schema for user list response."""

    users: list[UserResponseSchema]
    total: int


class UserStatsSchema(BaseSchema):
    """Schema for user statistics."""

    total_items: int
    total_bookings_made: int
    total_reviews_written: int
    avg_rating: float
    is_verified: bool
    member_since: str


class UserSearchSchema(BaseSchema):
    """Schema for user search parameters."""

    query: str = Field(..., min_length=2, max_length=100, description="Search query")
    verified_only: bool = Field(False, description="Search only verified users")


class UserVerificationSchema(BaseSchema):
    """Schema for user verification."""

    user_id: int = Field(..., description="User ID to verify")
    verify: bool = Field(..., description="Verification status")
