from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum

class PaymentMethod(str, Enum):
    CC = "CC"  # Credit Card
    QRIS = "QRIS"
    TRANSFER = "TRANSFER"
    CASH = "Cash"

class PaymentType(str, Enum):
    RENT = "RENT"
    FINE = "FINE"

class PaymentBase(BaseModel):
    booking_id: List[int] = Field(..., description="Array of booking IDs")
    total_price: float
    payment_method: PaymentMethod
    payment_type: PaymentType = PaymentType.RENT
    user_id: Optional[int] = None

class PaymentCreate(BaseModel):
    """Schema for creating a new payment."""
    booking_id: List[int] = Field(
        ...,
        description="List of booking IDs associated with this payment",
        example=[1, 2, 3],
        min_length=1
    )
    total_price: float = Field(
        ...,
        gt=0,
        description="Total amount to be paid",
        example=150000.0
    )
    payment_method: PaymentMethod = Field(
        ...,
        description="Method used for the payment"
    )
    payment_type: PaymentType = Field(
        default=PaymentType.RENT,
        description="Type of payment (RENT for rental payments, FINE for late fees)"
    )
    user_id: Optional[int] = Field(
        default=None,
        description="ID of the user making the payment. Typically set by the system.",
        exclude=True  # This field is typically set by the system, not the client
    )

class PaymentUpdate(BaseModel):
    total_price: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None
    payment_type: Optional[PaymentType] = None
    booking_id: Optional[List[int]] = None
    user_id: Optional[int] = None

class PaymentOut(PaymentBase):
    id: int
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)