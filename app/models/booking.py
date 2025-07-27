"""
Booking model for WeRent Backend API.
Handles rental bookings and their details.
"""

import enum
from datetime import datetime
from app.extensions import db


class BookingStatus(enum.Enum):
    """Enum for booking status."""
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    PASTDUE = "PASTDUE"
    RETURNED = "RETURNED"


class Booking(db.Model):
    """Booking model for rental bookings."""

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(BookingStatus), nullable=False, default=BookingStatus.PENDING)
    is_paid = db.Column(db.Boolean, default=False, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='bookings')
    item = db.relationship('Item', foreign_keys=[item_id], back_populates='bookings')
    tickets = db.relationship('Ticketing', back_populates='booking')

    def __repr__(self):
        """String representation of Booking object."""
        return f'<Booking {self.id} - User {self.user_id} - Item {self.item_id}>'

    def to_dict(self):
        """Convert booking object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'total_price': self.total_price,
            'status': self.status.value if self.status else None,
            'is_paid': self.is_paid
        }

    @property
    def duration_days(self):
        """Calculate booking duration in days."""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    def calculate_total_price(self):
        """Calculate total price based on duration and item price."""
        if self.item and self.duration_days > 0:
            return self.item.price_per_day * self.duration_days
        return 0.0

    @classmethod
    def find_by_id(cls, booking_id):
        """Find booking by ID."""
        return db.session.get(cls, booking_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        """Find all bookings for a user."""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_item_id(cls, item_id):
        """Find all bookings for an item."""
        return cls.query.filter_by(item_id=item_id).all()

    def save(self):
        """Save booking to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete booking from database."""
        db.session.delete(self)
        db.session.commit()
