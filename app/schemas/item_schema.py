"""
Item schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from app.schemas.base_schema import BaseSchema, TimestampMixin, ResponseSchema


class ItemCreateSchema(BaseSchema):
    """Schema for creating a new item."""

    @field_validator('type')
    @classmethod
    def uppercase_type(cls, v):
        if v is not None:
            return v.upper()
        return v

    @field_validator('size')
    @classmethod
    def uppercase_size(cls, v):
        if v is not None:
            return v.upper()
        return v

    @field_validator('gender')
    @classmethod
    def uppercase_gender(cls, v):
        if v is not None:
            return v.upper()
        return v

    """Schema for creating a new item."""

    name: str = Field(..., min_length=3, max_length=100, description="Item name")
    type: str = Field(..., min_length=2, max_length=50, description="Item type (category)")
    size: str = Field(..., min_length=1, max_length=20, description="Item size")
    gender: str = Field(..., min_length=1, max_length=20, description="Item gender")
    brand: Optional[str] = Field(None, max_length=100, description="Item brand")
    color: Optional[str] = Field(None, max_length=50, description="Item color")
    quantity: int = Field(1, gt=0, description="Quantity available")
    product_code: str = Field(..., min_length=1, max_length=50, description="Unique product code")
    description: str = Field(..., min_length=10, max_length=1000, description="Item description")
    price_per_day: float = Field(..., gt=0, description="Price per day in currency")

    @field_validator('price_per_day')
    @classmethod
    def validate_price(cls, v):
        """Validate price format."""
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        if v > 10000:  # Max price limit
            raise ValueError('Price cannot exceed 10,000 per day')
        return round(v, 2)  # Round to 2 decimal places


class ItemUpdateSchema(BaseSchema):
    """Schema for updating an item."""

    @field_validator('type')
    @classmethod
    def uppercase_type(cls, v):
        if v is not None:
            return v.upper()
        return v

    @field_validator('size')
    @classmethod
    def uppercase_size(cls, v):
        if v is not None:
            return v.upper()
        return v

    @field_validator('gender')
    @classmethod
    def uppercase_gender(cls, v):
        if v is not None:
            return v.upper()
        return v

    """Schema for updating an item."""

    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Item name")
    type: Optional[str] = Field(None, min_length=2, max_length=50, description="Item type (category)")
    size: Optional[str] = Field(None, min_length=1, max_length=20, description="Item size")
    gender: Optional[str] = Field(None, min_length=1, max_length=20, description="Item gender")
    brand: Optional[str] = Field(None, max_length=100, description="Item brand")
    color: Optional[str] = Field(None, max_length=50, description="Item color")
    quantity: Optional[int] = Field(None, gt=0, description="Quantity available")
    product_code: Optional[str] = Field(None, min_length=1, max_length=50, description="Unique product code")
    description: Optional[str] = Field(None, min_length=10, max_length=1000, description="Item description")
    price_per_day: Optional[float] = Field(None, gt=0, description="Price per day in currency")

    @field_validator('price_per_day')
    @classmethod
    def validate_price(cls, v):
        """Validate price format."""
        if v is not None:
            if v <= 0:
                raise ValueError('Price must be greater than 0')
            if v > 10000:
                raise ValueError('Price cannot exceed 10,000 per day')
            return round(v, 2)
        return v


class ItemResponseSchema(BaseSchema, TimestampMixin):
    """Schema for item response."""

    id: int
    name: str
    type: str
    size: str
    gender: str
    brand: Optional[str] = None
    color: Optional[str] = None
    quantity: int
    product_code: str
    description: str
    price_per_day: float
    rating: float
    created_at: str
    updated_at: str
    user_id: int
    images: Optional[List[dict]] = None


class ItemDetailResponseSchema(ItemResponseSchema):
    """Extended item response with related data."""

    owner: Optional[dict] = None
    reviews_count: Optional[int] = None
    avg_rating: Optional[float] = None
    total_bookings: Optional[int] = None


class ItemListResponseSchema(ResponseSchema):
    """Schema for item list response."""

    items: List[ItemResponseSchema]
    total: int


class ItemSearchSchema(BaseSchema):
    """Schema for item search parameters."""

    query: Optional[str] = Field(None, min_length=2, max_length=100, description="Search query")
    category: Optional[str] = Field(None, description="Filter by category")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price per day")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price per day")

    @field_validator('max_price')
    @classmethod
    def validate_price_range(cls, v, values):
        """Validate price range."""
        if v is not None and 'min_price' in values.data and values.data['min_price'] is not None:
            if v < values.data['min_price']:
                raise ValueError('Maximum price must be greater than minimum price')
        return v



class ItemFilterSchema(BaseSchema):
    """Schema for advanced item filtering."""

    categories: Optional[List[str]] = Field(None, description="List of categories to filter")
    price_range: Optional[dict] = Field(None, description="Price range filter")
    rating_min: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    owner_verified: Optional[bool] = Field(None, description="Filter by verified owners")
    has_images: Optional[bool] = Field(None, description="Filter items with images")


class ItemStatsSchema(BaseSchema):
    """Schema for item statistics."""

    total_bookings: int
    total_reviews: int
    average_rating: float
    total_images: int
    created_at: str


class ItemAvailabilitySchema(BaseSchema):
    """Schema for checking item availability."""

    start_date: datetime = Field(..., description="Start date for availability check")
    end_date: datetime = Field(..., description="End date for availability check")

    @field_validator('end_date')
    @classmethod
    def validate_date_range(cls, v, values):
        """Validate date range."""
        if 'start_date' in values.data and v <= values.data['start_date']:
            raise ValueError('End date must be after start date')
        return v

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        """Validate start date is not in the past."""
        if v.date() < datetime.now().date():
            raise ValueError('Start date cannot be in the past')
        return v


class ItemAvailabilityResponseSchema(BaseSchema):
    """Schema for item availability response."""

    item_id: int
    is_available: bool
    conflicting_bookings: Optional[List[dict]] = None


class CategoryStatsSchema(BaseSchema):
    """Schema for category statistics."""

    category: str
    count: int
