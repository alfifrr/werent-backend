"""
Item model for CamRent Backend API.
Handles rental items and their details.
"""

from datetime import datetime
from app.extensions import db


class Item(db.Model):
    """Item model for rental items management."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')  # available, rented, maintenance
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Foreign key
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id], back_populates='owned_items')
    images = db.relationship('Image', back_populates='item', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='item')
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        """String representation of Item object."""
        return f'<Item {self.title}>'

    def to_dict(self):
        """Convert item object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price_per_day': self.price_per_day,
            'status': self.status,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'owner_id': self.owner_id
        }
