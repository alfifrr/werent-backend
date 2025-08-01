from app.models.payment import Payment, PaymentMethod, PaymentType
from app.extensions import db
from typing import List, Optional
from app.models.booking import Booking
from app.models.user import User

class PaymentService:
    @staticmethod
    def create_payment(booking_id: List[int], total_price: float, payment_method: PaymentMethod, payment_type: PaymentType, user_id: Optional[int] = None) -> Optional[Payment]:
        # Check user exists and is verified
        if user_id is not None:
            user = User.query.get(user_id)
            if not user or not getattr(user, 'is_verified', False):
                return None

        # Check all booking_ids exist and belong to user (if user_id provided)
        for bid in booking_id:
            booking = Booking.query.get(bid)
            if not booking:
                return None
            if user_id is not None and str(booking.user_id) != str(user_id):
                return None

        try:
            # Create payment record
            payment = Payment(
                booking_id=booking_id,
                total_price=total_price,
                payment_method=payment_method,
                payment_type=payment_type,
                user_id=user_id
            )
            db.session.add(payment)
            
            # Update all associated bookings based on payment type
            for bid in booking_id:
                booking = Booking.query.get(bid)
                if booking:
                    # For FINE payments, set status to RETURNED but keep is_paid as True
                    if payment_type == PaymentType.FINE:
                        booking.status = 'RETURNED'
                    else:
                        booking.status = 'PAID'
                    booking.is_paid = True
                    db.session.add(booking)
            
            db.session.commit()
            return payment
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating payment: {str(e)}")
            return None

    @staticmethod
    def get_payment(payment_id: int) -> Optional[Payment]:
        return db.session.get(Payment, payment_id)

    @staticmethod
    def get_all_payments() -> List[Payment]:
        return Payment.query.all()

    @staticmethod
    def update_payment(payment_id: int, **kwargs) -> Optional[Payment]:
        payment = db.session.get(Payment, payment_id)
        if not payment:
            return None
        for key, value in kwargs.items():
            if hasattr(payment, key) and value is not None:
                setattr(payment, key, value)
        db.session.commit()
        return payment

    @staticmethod
    def delete_payment(payment_id: int) -> bool:
        payment = db.session.get(Payment, payment_id)
        if not payment:
            return False
        db.session.delete(payment)
        db.session.commit()
        return True

    @staticmethod
    def get_payments_by_user_id(user_id: int) -> list[Payment]:
        return Payment.query.filter_by(user_id=user_id).all()