"""
User schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.base_schema import BaseSchema, TimestampMixin, ResponseSchema


class UserCreateSchema(BaseSchema):
    """Schema for creating a new user, aligned with User model."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=8, max_length=128, description="User password"
    )
    first_name: str = Field(
        ..., min_length=1, max_length=50, description="User first name"
    )
    last_name: str = Field(
        ..., min_length=1, max_length=50, description="User last name"
    )
    phone_number: Optional[str] = Field(
        None, max_length=20, description="User phone number"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            cleaned = "".join(filter(str.isdigit, v))
            if len(cleaned) < 10 or len(cleaned) > 15:
                raise ValueError("Phone number must be between 10-15 digits")
        return v


class UserLoginSchema(BaseSchema):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserUpdateSchema(BaseSchema):
    """Schema for updating user profile, aligned with User model."""

    first_name: Optional[str] = Field(
        None, min_length=1, max_length=50, description="User first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=50, description="User last name"
    )
    phone_number: Optional[str] = Field(
        None, max_length=20, description="User phone number"
    )
    profile_image: Optional[str] = Field(
        None, description="Base64 encoded profile image with data URI prefix (e.g., data:image/jpeg;base64,...)"
    )

    @field_validator("profile_image")
    @classmethod
    def validate_profile_image(cls, v):
        """Validate Base64 profile image format and size using the shared validator."""
        if v is not None:
            from app.utils.validators import validate_base64_image
            
            # Check data URI format
            if not v.startswith('data:image/'):
                raise ValueError("Profile image must be a valid data URI (data:image/...)")
            
            # Extract MIME type
            import re
            match = re.match(r'data:image/(jpeg|jpg|png|gif);base64,', v)
            if not match:
                raise ValueError("Invalid image format. Supported: JPEG, PNG, GIF")
            
            # Validate the image using the shared validator
            if not validate_base64_image(v):
                raise ValueError("Invalid or corrupted image file")
            
            # Check file size (limit to 2MB)
            base64_data = v.split(',', 1)[-1]
            import base64
            decoded_data = base64.b64decode(base64_data, validate=True)
            max_size = 2 * 1024 * 1024  # 2MB
            if len(decoded_data) > max_size:
                raise ValueError("Image size must be less than 2MB")
        
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            cleaned = "".join(filter(str.isdigit, v))
            if len(cleaned) < 10 or len(cleaned) > 15:
                raise ValueError("Phone number must be between 10-15 digits")
        return v


class UserPasswordUpdateSchema(BaseSchema):
    """Schema for updating user password."""

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ..., min_length=8, max_length=128, description="New password"
    )
    confirm_password: str = Field(..., description="Confirm new password")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if "new_password" in values.data and v != values.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class UserResponseSchema(BaseSchema, TimestampMixin):
    """Schema for user response, aligned with User model."""

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    is_verified: bool
    is_admin: bool
    is_active: bool
    uuid: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



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
