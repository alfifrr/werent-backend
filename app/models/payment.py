import enum
import json
from datetime import datetime
from app.extensions import db


class PaymentMethod(enum.Enum):
    CC = "CC"
    QRIS = "QRIS"
    TRANSFER = "TRANSFER"
    CASH = "Cash"


class PaymentType(enum.Enum):
    RENT = "RENT"
    FINE = "FINE"


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.JSON, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethod), nullable=False)
    payment_type = db.Column(db.Enum(PaymentType), nullable=False, default=PaymentType.RENT)
    payment_date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    user = db.relationship('User', back_populates='payments')

    def __repr__(self):
        return f'<Payment {self.id} - {self.payment_method.value} - {self.total_price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'total_price': self.total_price,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'payment_type': self.payment_type.value if self.payment_type else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'user_id': self.user_id
        }

    @property
    def booking_ids_list(self):
        if isinstance(self.booking_id, list):
            return self.booking_id
        return []

    def add_booking_id(self, booking_id):
        current_ids = self.booking_ids_list
        if booking_id not in current_ids:
            current_ids.append(booking_id)
            self.booking_id = current_ids

    def remove_booking_id(self, booking_id):
        current_ids = self.booking_ids_list
        if booking_id in current_ids:
            current_ids.remove(booking_id)
            self.booking_id = current_ids

    @classmethod
    def find_by_id(cls, payment_id):
        return db.session.get(cls, payment_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_booking_id(cls, booking_id):
        return cls.query.filter(cls.booking_id.contains([booking_id])).all()

    @classmethod
    def find_by_payment_type(cls, payment_type):
        return cls.query.filter_by(payment_type=payment_type).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
