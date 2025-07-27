from app.models.payment import Payment, PaymentMethod, PaymentType
from app.extensions import db
from typing import List, Optional

class PaymentService:
    @staticmethod
    def create_payment(booking_id: List[int], total_price: float, payment_method: PaymentMethod, payment_type: PaymentType, user_id: Optional[int] = None) -> Payment:
        payment = Payment(
            booking_id=booking_id,
            total_price=total_price,
            payment_method=payment_method,
            payment_type=payment_type,
            user_id=user_id
        )
        db.session.add(payment)
        db.session.commit()
        return payment

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