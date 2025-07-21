"""
Booking model for CamRent Backend API.
Handles rental bookings between users and items.
"""

from datetime import datetime
from app.extensions import db


class Booking(db.Model):
    """Booking model for rental transactions."""

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, completed, cancelled
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Foreign keys
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    item = db.relationship('Item', back_populates='bookings')
    renter = db.relationship('User', foreign_keys=[renter_id], back_populates='rented_items')

    def __repr__(self):
        """String representation of Booking object."""
        return f'<Booking {self.id}: {self.item.title} by {self.renter.name}>'

    def to_dict(self):
        """Convert booking object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat(),
            'item_id': self.item_id,
            'renter_id': self.renter_id
        }
