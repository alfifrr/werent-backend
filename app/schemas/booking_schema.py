"""
Booking schemas for request/response validation.
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.schemas.base_schema import BaseSchema, TimestampMixin, ResponseSchema
from enum import Enum


class BookingStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    PASTDUE = "PASTDUE"
    RETURNED = "RETURNED"
    COMPLETED = "COMPLETED"
    CONFIRMED = "CONFIRMED"

class BookingBase(BaseModel):
    item_id: int
    start_date: date
    end_date: date
    quantity: int = Field(default=1, ge=1, le=10, description="Number of items to book (1-10)")

    @field_validator('end_date')
    def end_date_after_start(cls, v, info):
        start_date = info.data.get('start_date')
        if start_date and v < start_date:
            raise ValueError('end_date must be after start_date')
        return v

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    user_id: int
    total_price: float
    status: BookingStatus
    is_paid: bool

    model_config = ConfigDict(from_attributes=True)



class BookingCreateSchema(BaseSchema):
    """Schema for creating a new booking."""

    item_id: int = Field(..., description="ID of the item to book")
    start_date: date = Field(..., description="Booking start date")
    end_date: date = Field(..., description="Booking end date")
    quantity: int = Field(default=1, ge=1, le=10, description="Number of items to book (1-10)")

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        """Validate start date is not in the past."""
        if v < date.today():
            raise ValueError('Start date cannot be in the past')
        return v

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, values):
        """Validate end date is after start date."""
        if 'start_date' in values.data and v <= values.data['start_date']:
            raise ValueError('End date must be after start date')
        return v

    @field_validator('end_date')
    @classmethod
    def validate_booking_duration(cls, v, values):
        """Validate booking duration (max 30 days)."""
        if 'start_date' in values.data:
            duration = (v - values.data['start_date']).days
            if duration > 30:
                raise ValueError('Booking duration cannot exceed 30 days')
            if duration < 1:
                raise ValueError('Minimum booking duration is 1 day')
        return v


class BookingUpdateSchema(BaseSchema):
    """Schema for updating booking dates."""

    start_date: Optional[date] = Field(None, description="New start date")
    end_date: Optional[date] = Field(None, description="New end date")

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        """Validate start date is not in the past."""
        if v is not None and v < date.today():
            raise ValueError('Start date cannot be in the past')
        return v

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, values):
        """Validate end date is after start date."""
        if v is not None and 'start_date' in values.data and values.data['start_date'] is not None:
            if v <= values.data['start_date']:
                raise ValueError('End date must be after start date')
        return v


class BookingStatusUpdateSchema(BaseSchema):
    """Schema for updating booking status."""

    status: str = Field(..., description="New booking status")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Validate status value."""
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled', 'pastdue', 'returned']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {valid_statuses}')
        return v


class BookingExtendSchema(BaseSchema):
    """Schema for extending booking."""

    new_end_date: date = Field(..., description="New end date for extension")

    @field_validator('new_end_date')
    @classmethod
    def validate_new_end_date(cls, v):
        """Validate new end date is in the future."""
        if v <= date.today():
            raise ValueError('New end date must be in the future')
        return v


class BookingResponseSchema(BaseSchema, TimestampMixin):
    """Schema for booking response."""

    id: int
    start_date: date
    end_date: date
    status: str
    total_price: float
    item_id: int
    user_id: int
    duration_days: Optional[int] = None


class BookingDetailResponseSchema(BookingResponseSchema):
    """Extended booking response with related data."""

    item: Optional[dict] = None
    renter: Optional[dict] = None
    owner: Optional[dict] = None


class BookingListResponseSchema(ResponseSchema):
    """Schema for booking list response."""

    bookings: List[BookingResponseSchema]
    total: int


class BookingSearchSchema(BaseSchema):
    """Schema for booking search parameters."""

    status: Optional[str] = Field(None, description="Filter by status")
    start_date_from: Optional[date] = Field(None, description="Filter bookings starting from this date")
    start_date_to: Optional[date] = Field(None, description="Filter bookings starting before this date")
    item_id: Optional[int] = Field(None, description="Filter by item ID")
    user_id: Optional[int] = Field(None, description="Filter by user ID")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Validate status value."""
        if v is not None:
            valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled', 'pastdue', 'returned', 'all']
            if v not in valid_statuses:
                raise ValueError(f'Status must be one of: {valid_statuses}')
        return v

    @field_validator('start_date_to')
    @classmethod
    def validate_date_range(cls, v, values):
        """Validate date range."""
        if v is not None and 'start_date_from' in values.data and values.data['start_date_from'] is not None:
            if v < values.data['start_date_from']:
                raise ValueError('End date must be after start date')
        return v


class BookingStatsSchema(BaseSchema):
    """Schema for booking statistics."""

    total_bookings: int
    pending_bookings: int
    confirmed_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    pastdue_bookings: int
    returned_bookings: int
    total_revenue: float


class BookingCalendarSchema(BaseSchema):
    """Schema for booking calendar view."""

    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: int = Field(..., ge=2020, le=2030, description="Year")
    item_id: Optional[int] = Field(None, description="Filter by specific item")


class BookingCalendarResponseSchema(BaseSchema):
    """Schema for booking calendar response."""

    month: int
    year: int
    bookings: List[dict]
    available_dates: List[date]
    booked_dates: List[date]


class BookingAvailabilityCheckSchema(BaseSchema):
    """Schema for checking booking availability."""

    item_id: int = Field(..., description="Item ID to check")
    start_date: date = Field(..., description="Start date")
    end_date: date = Field(..., description="End date")
    exclude_booking_id: Optional[int] = Field(None, description="Exclude specific booking from check")

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        """Validate start date."""
        if v < date.today():
            raise ValueError('Start date cannot be in the past')
        return v

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, values):
        """Validate end date."""
        if 'start_date' in values.data and v <= values.data['start_date']:
            raise ValueError('End date must be after start date')
        return v


class BookingAvailabilityResponseSchema(BaseSchema):
    """Schema for booking availability response."""

    is_available: bool
    conflicting_bookings: Optional[List[dict]] = None
    suggested_dates: Optional[List[dict]] = None


class BookingRevenueSchema(BaseSchema):
    """Schema for booking revenue calculation."""

    owner_id: int = Field(..., description="Owner ID")
    start_date: Optional[date] = Field(None, description="Start date for revenue calculation")
    end_date: Optional[date] = Field(None, description="End date for revenue calculation")


class BookingRevenueResponseSchema(BaseSchema):
    """Schema for booking revenue response."""

    owner_id: int
    total_revenue: float
    completed_bookings: int
    period_start: Optional[date]
    period_end: Optional[date]
    revenue_breakdown: Optional[List[dict]] = None
