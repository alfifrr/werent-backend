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
    COMPLETED = "COMPLETED"
    CONFIRMED = "CONFIRMED"
    EXPIRED = "EXPIRED"


class Booking(db.Model):
    """Booking model for rental bookings."""

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.Enum(BookingStatus), nullable=False, default=BookingStatus.PENDING)
    is_paid = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)  # When PENDING booking expires

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
            'quantity': self.quantity,
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

    @classmethod
    def check_item_availability(cls, item_id, start_date, end_date, requested_quantity=1, exclude_booking_id=None):
        """
        Check if an item is available for booking in the given date range with quantity support.
        
        Best Practice Implementation:
        - PENDING bookings have a time limit (30 minutes by default)
        - Only PAID, CONFIRMED bookings permanently block availability
        - Expired PENDING bookings are automatically excluded
        - Supports multiple quantities per booking
        
        Args:
            item_id: ID of the item to check
            start_date: Start date of the requested booking
            end_date: End date of the requested booking
            requested_quantity: Number of items requested (default: 1)
            exclude_booking_id: Optional booking ID to exclude from check (for updates)
            
        Returns:
            dict: Enhanced availability information with quantity details
        """
        from app.models.item import Item
        from datetime import datetime, timedelta
        
        # Get the item to check its total quantity
        item = Item.query.get(item_id)
        if not item:
            return {
                'available': False,
                'available_quantity': 0,
                'total_quantity': 0,
                'requested_quantity': requested_quantity,
                'can_fulfill': False,
                'error': 'Item not found'
            }
        
        current_time = datetime.utcnow()
        
        # Calculate total quantity reserved by confirmed bookings (PAID/CONFIRMED)
        confirmed_reserved_query = db.session.query(
            db.func.coalesce(db.func.sum(cls.quantity), 0)
        ).filter(
            cls.item_id == item_id,
            cls.status.in_([BookingStatus.PAID, BookingStatus.CONFIRMED]),
            cls.start_date <= end_date,
            cls.end_date >= start_date
        )
        
        # Calculate total quantity reserved by active pending bookings
        pending_reserved_query = db.session.query(
            db.func.coalesce(db.func.sum(cls.quantity), 0)
        ).filter(
            cls.item_id == item_id,
            cls.status == BookingStatus.PENDING,
            cls.start_date <= end_date,
            cls.end_date >= start_date,
            # Only include PENDING bookings that haven't expired
            db.or_(
                cls.expires_at.is_(None),  # No expiration set (legacy bookings)
                cls.expires_at > current_time  # Not yet expired
            )
        )
        
        # Exclude specific booking if provided (for updates)
        if exclude_booking_id:
            confirmed_reserved_query = confirmed_reserved_query.filter(cls.id != exclude_booking_id)
            pending_reserved_query = pending_reserved_query.filter(cls.id != exclude_booking_id)
        
        confirmed_reserved = confirmed_reserved_query.scalar() or 0
        pending_reserved = pending_reserved_query.scalar() or 0
        
        total_reserved = confirmed_reserved + pending_reserved
        available_quantity = max(0, item.quantity - total_reserved)
        
        # Count PENDING bookings expiring soon (within 5 minutes)
        expiring_soon_quantity = db.session.query(
            db.func.coalesce(db.func.sum(cls.quantity), 0)
        ).filter(
            cls.item_id == item_id,
            cls.status == BookingStatus.PENDING,
            cls.expires_at.isnot(None),
            cls.expires_at > current_time,
            cls.expires_at <= current_time + timedelta(minutes=5)
        ).scalar() or 0
        
        return {
            'available': available_quantity >= requested_quantity,
            'available_quantity': available_quantity,
            'total_quantity': item.quantity,
            'requested_quantity': requested_quantity,
            'can_fulfill': available_quantity >= requested_quantity,
            'reserved_quantity': total_reserved,
            'confirmed_reserved': confirmed_reserved,
            'pending_reserved': pending_reserved,
            'pending_expiring_soon': expiring_soon_quantity
        }
    
    @classmethod
    def get_availability_calendar(cls, item_id, start_date, end_date):
        """
        Get a calendar view of item availability for a date range.
        
        Args:
            item_id: ID of the item
            start_date: Start date for calendar
            end_date: End date for calendar
            
        Returns:
            dict: Date-wise availability information
        """
        from app.models.item import Item
        from datetime import timedelta
        
        item = Item.query.get(item_id)
        if not item:
            return {'error': 'Item not found'}
        
        calendar = {}
        current_date = start_date
        
        while current_date <= end_date:
            availability = cls.check_item_availability(
                item_id, 
                current_date, 
                current_date
            )
            
            calendar[current_date.isoformat()] = {
                'available_quantity': availability['available_quantity'],
                'total_quantity': availability['total_quantity'],
                'is_available': availability['available']
            }
            
            current_date += timedelta(days=1)
        
        return calendar
    
    @classmethod
    def expire_pending_bookings(cls):
        """
        Mark expired PENDING bookings as EXPIRED.
        This should be called periodically (e.g., via a background job).
        
        Returns:
            int: Number of bookings that were expired
        """
        from datetime import datetime
        
        current_time = datetime.utcnow()
        
        # Find expired PENDING bookings
        expired_bookings = cls.query.filter(
            cls.status == BookingStatus.PENDING,
            cls.expires_at.isnot(None),
            cls.expires_at <= current_time
        ).all()
        
        expired_count = len(expired_bookings)
        
        # Mark them as expired
        for booking in expired_bookings:
            booking.status = BookingStatus.EXPIRED
            booking.updated_at = current_time
        
        if expired_count > 0:
            db.session.commit()
        
        return expired_count
    
    def set_expiration(self, minutes=30):
        """
        Set expiration time for PENDING booking.
        
        Args:
            minutes: Minutes until expiration (default 30)
        """
        from datetime import datetime, timedelta
        
        if self.status == BookingStatus.PENDING:
            self.expires_at = datetime.utcnow() + timedelta(minutes=minutes)
            db.session.commit()
    
    def is_expired(self):
        """Check if a PENDING booking has expired."""
        from datetime import datetime
        
        if self.status != BookingStatus.PENDING or not self.expires_at:
            return False
        
        return datetime.utcnow() > self.expires_at
