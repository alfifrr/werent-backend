"""
Email verification schemas for WeRent Backend API.
Handles validation for email verification endpoints.
"""

from pydantic import BaseModel, Field, field_validator
import re


class ResendVerificationSchema(BaseModel):
    """Schema for resending verification email request."""
    
    email: str = Field(
        ..., 
        description="User's email address",
        min_length=5,
        max_length=120
    )

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if not v:
            raise ValueError('Email is required')
        
        v = v.strip().lower()
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        
        return v


class EmailVerificationResponseSchema(BaseModel):
    """Schema for email verification response."""
    
    verified: bool = Field(description="Whether the email was successfully verified")
    message: str = Field(description="Response message")


class ResendVerificationResponseSchema(BaseModel):
    """Schema for resend verification response."""
    
    email_sent: bool = Field(description="Whether the verification email was sent")
    message: str = Field(description="Response message")
