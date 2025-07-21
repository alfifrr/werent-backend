"""
Authentication schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.base_schema import BaseSchema


class LoginSchema(BaseSchema):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class LoginResponseSchema(BaseSchema):
    """Schema for login response."""

    success: bool
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[dict] = None
    expires_in: Optional[int] = None


class RegisterSchema(BaseSchema):
    """Schema for user registration."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    confirm_password: str = Field(..., description="Confirm password")
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
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'password' in values.data and v != values.data['password']:
            raise ValueError('Passwords do not match')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            cleaned = ''.join(filter(str.isdigit, v))
            if len(cleaned) < 10 or len(cleaned) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
        return v


class RegisterResponseSchema(BaseSchema):
    """Schema for registration response."""

    success: bool
    message: str
    user: Optional[dict] = None


class TokenRefreshSchema(BaseSchema):
    """Schema for token refresh."""

    refresh_token: str = Field(..., description="Refresh token")


class TokenResponseSchema(BaseSchema):
    """Schema for token response."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class PasswordResetRequestSchema(BaseSchema):
    """Schema for password reset request."""

    email: EmailStr = Field(..., description="User email address")


class PasswordResetSchema(BaseSchema):
    """Schema for password reset."""

    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'new_password' in values.data and v != values.data['new_password']:
            raise ValueError('Passwords do not match')
        return v


class EmailVerificationSchema(BaseSchema):
    """Schema for email verification."""

    token: str = Field(..., description="Email verification token")


class EmailVerificationRequestSchema(BaseSchema):
    """Schema for requesting email verification."""

    email: EmailStr = Field(..., description="User email address")


class ChangePasswordSchema(BaseSchema):
    """Schema for changing password (authenticated user)."""

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'new_password' in values.data and v != values.data['new_password']:
            raise ValueError('Passwords do not match')
        return v


class LogoutSchema(BaseSchema):
    """Schema for user logout."""

    refresh_token: Optional[str] = Field(None, description="Refresh token to invalidate")


class AuthStatusSchema(BaseSchema):
    """Schema for authentication status."""

    is_authenticated: bool
    user: Optional[dict] = None
    permissions: Optional[list] = None


class TwoFactorAuthSchema(BaseSchema):
    """Schema for two-factor authentication."""

    code: str = Field(..., min_length=6, max_length=6, description="2FA code")

    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        """Validate 2FA code format."""
        if not v.isdigit():
            raise ValueError('2FA code must contain only digits')
        return v


class TwoFactorSetupSchema(BaseSchema):
    """Schema for setting up two-factor authentication."""

    enable: bool = Field(..., description="Enable or disable 2FA")
    code: Optional[str] = Field(None, min_length=6, max_length=6, description="Verification code")

    @field_validator('code')
    @classmethod
    def validate_code(cls, v, values):
        """Validate code when enabling 2FA."""
        if values.data.get('enable') and not v:
            raise ValueError('Verification code is required when enabling 2FA')
        if v and not v.isdigit():
            raise ValueError('Code must contain only digits')
        return v
