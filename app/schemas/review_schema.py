"""
Review schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from app.schemas.base_schema import BaseSchema, TimestampMixin, ResponseSchema


class ReviewCreateSchema(BaseSchema):
    """Schema for creating a new review."""

    item_id: int = Field(..., description="ID of the item being reviewed")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    review_message: str = Field(..., min_length=5, max_length=500, description="Review message")

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        """Validate rating value."""
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


class ReviewUpdateSchema(BaseSchema):
    """Schema for updating a review."""

    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5")
    review_message: Optional[str] = Field(None, min_length=5, max_length=500, description="Review message")

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        """Validate rating value."""
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v


class ReviewResponseSchema(BaseSchema, TimestampMixin):
    """Schema for review response."""

    id: int
    rating: int
    review_message: str
    item_id: int
    user_id: int


class ReviewDetailResponseSchema(ReviewResponseSchema):
    """Extended review response with related data."""

    item: Optional[dict] = None
    user: Optional[dict] = None


class ReviewListResponseSchema(ResponseSchema):
    """Schema for review list response."""

    reviews: List[ReviewResponseSchema]
    total: int


class ReviewSearchSchema(BaseSchema):
    """Schema for review search parameters."""

    item_id: Optional[int] = Field(None, description="Filter by item ID")
    reviewer_id: Optional[int] = Field(None, description="Filter by user ID")
    min_rating: Optional[int] = Field(None, ge=1, le=5, description="Minimum rating")
    max_rating: Optional[int] = Field(None, ge=1, le=5, description="Maximum rating")

    @field_validator('max_rating')
    @classmethod
    def validate_rating_range(cls, v, values):
        """Validate rating range."""
        if v is not None and 'min_rating' in values.data and values.data['min_rating'] is not None:
            if v < values.data['min_rating']:
                raise ValueError('Maximum rating must be greater than or equal to minimum rating')
        return v


class ReviewStatsSchema(BaseSchema):
    """Schema for review statistics."""

    total_reviews: int
    average_rating: float
    rating_distribution: dict


class ReviewRatingDistributionSchema(BaseSchema):
    """Schema for rating distribution."""

    rating_1: int = 0
    rating_2: int = 0
    rating_3: int = 0
    rating_4: int = 0
    rating_5: int = 0
    total_reviews: int
    average_rating: float
