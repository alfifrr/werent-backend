from pydantic import BaseModel, Field
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

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    total_price: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None
    payment_type: Optional[PaymentType] = None
    booking_id: Optional[List[int]] = None
    user_id: Optional[int] = None

class PaymentOut(PaymentBase):
    id: int
    payment_date: datetime

    class Config:
        from_attributes = True 