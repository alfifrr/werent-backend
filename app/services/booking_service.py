"""
Booking service for business logic operations.
Handles booking management, availability checking, and booking-related operations.
"""

from datetime import datetime, timedelta
from app.services.base_service import BaseService
from app.models.booking import Booking


class BookingService(BaseService):
    """Service class for Booking model business logic."""

    def __init__(self):
        """Initialize BookingService."""
        super().__init__(Booking)

    def create_booking(self, item_id, user_id, start_date, end_date):
        """Create a new booking with validation."""
        # Check if item is available for the requested dates
        if not self.is_available_for_dates(item_id, start_date, end_date):
            raise ValueError("Item is not available for the requested dates")

        # Calculate total price
        from app.services.item_service import ItemService
        item_service = ItemService()
        item = item_service.get_by_id(item_id)

        if not item:
            raise ValueError("Item not found")

        duration_days = (end_date - start_date).days + 1
        total_price = duration_days * item.price_per_day

        booking = Booking()
        booking.item_id = item_id
        booking.user_id = user_id
        booking.start_date = start_date
        booking.end_date = end_date
        booking.total_price = total_price
        booking.status = 'pending'

        return self.save(booking)

    def is_available_for_dates(self, item_id, start_date, end_date):
        """Check if item is available for the specified date range."""
        # Check if item exists and is available
        from app.services.item_service import ItemService
        item_service = ItemService()

        if not item_service.is_item_available(item_id):
            return False

        # Check for conflicting bookings
        conflicting_bookings = Booking.query.filter(
            Booking.item_id == item_id,
            Booking.status.in_(['confirmed', 'pending']),
            Booking.start_date <= end_date,
            Booking.end_date >= start_date
        ).count()

        return conflicting_bookings == 0

    def confirm_booking(self, booking_id):
        """Confirm a pending booking."""
        booking = self.get_by_id(booking_id)
        if not booking:
            return None

        if booking.status != 'pending':
            raise ValueError("Only pending bookings can be confirmed")

        # Double-check availability
        if not self.is_available_for_dates(booking.item_id, booking.start_date, booking.end_date):
            raise ValueError("Item is no longer available for these dates")

        booking.status = 'confirmed'

        # Update item status to rented
        from app.services.item_service import ItemService
        item_service = ItemService()
        item_service.mark_as_rented(booking.item_id)

        return self.save(booking)

    def complete_booking(self, booking_id):
        """Mark booking as completed."""
        booking = self.get_by_id(booking_id)
        if not booking:
            return None

        if booking.status != 'confirmed':
            raise ValueError("Only confirmed bookings can be completed")

        booking.status = 'completed'

        # Update item status back to available
        from app.services.item_service import ItemService
        item_service = ItemService()
        item_service.mark_as_available(booking.item_id)

        return self.save(booking)

    def cancel_booking(self, booking_id):
        """Cancel a booking."""
        booking = self.get_by_id(booking_id)
        if not booking:
            return None

        if booking.status in ['completed', 'cancelled']:
            raise ValueError("Cannot cancel completed or already cancelled bookings")

        booking.status = 'cancelled'

        # If booking was confirmed, make item available again
        if booking.status == 'confirmed':
            from app.services.item_service import ItemService
            item_service = ItemService()
            item_service.mark_as_available(booking.item_id)

        return self.save(booking)

    def get_bookings_by_renter(self, user_id):
        """Get all bookings made by a specific renter."""
        return Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()

    def get_bookings_by_item(self, item_id):
        """Get all bookings for a specific item."""
        return Booking.query.filter_by(item_id=item_id).order_by(Booking.created_at.desc()).all()

    def get_bookings_by_status(self, status):
        """Get all bookings with a specific status."""
        return Booking.query.filter_by(status=status).order_by(Booking.created_at.desc()).all()

    def get_active_bookings(self):
        """Get all currently active bookings."""
        now = datetime.now()
        return Booking.query.filter(
            Booking.status == 'confirmed',
            Booking.start_date <= now,
            Booking.end_date >= now
        ).all()

    def get_upcoming_bookings(self, days_ahead=7):
        """Get bookings starting within the next specified days."""
        from datetime import timedelta

        now = datetime.now()
        future_date = now + timedelta(days=days_ahead)

        return Booking.query.filter(
            Booking.status == 'confirmed',
            Booking.start_date >= now,
            Booking.start_date <= future_date
        ).order_by(Booking.start_date).all()

    def get_booking_history(self, user_id, limit=20):
        """Get booking history for a user."""
        return Booking.query.filter_by(user_id=user_id).order_by(
            Booking.created_at.desc()
        ).limit(limit).all()

    def calculate_duration_days(self, booking_id):
        """Calculate booking duration in days."""
        booking = self.get_by_id(booking_id)
        if booking:
            return (booking.end_date - booking.start_date).days + 1
        return 0

    def calculate_total_revenue(self, owner_id):
        """Calculate total revenue from completed bookings for an owner's items."""
        from app.models.item import Item

        completed_bookings = Booking.query.join(Item).filter(
            Item.owner_id == owner_id,
            Booking.status == 'completed'
        ).all()

        return sum(booking.total_price for booking in completed_bookings)

    def get_booking_statistics(self, start_date=None, end_date=None):
        """Get booking statistics for a date range."""
        query = Booking.query

        if start_date:
            query = query.filter(Booking.created_at >= start_date)
        if end_date:
            query = query.filter(Booking.created_at <= end_date)

        bookings = query.all()

        return {
            'total_bookings': len(bookings),
            'pending_bookings': len([b for b in bookings if b.status == 'pending']),
            'confirmed_bookings': len([b for b in bookings if b.status == 'confirmed']),
            'completed_bookings': len([b for b in bookings if b.status == 'completed']),
            'cancelled_bookings': len([b for b in bookings if b.status == 'cancelled']),
            'total_revenue': sum(b.total_price for b in bookings if b.status == 'completed')
        }

    def get_owner_bookings(self, owner_id):
        """Get all bookings for items owned by a specific user."""
        from app.models.item import Item

        return Booking.query.join(Item).filter(Item.owner_id == owner_id).order_by(
            Booking.created_at.desc()
        ).all()

    def extend_booking(self, booking_id, new_end_date):
        """Extend booking end date if possible."""
        booking = self.get_by_id(booking_id)
        if not booking:
            return None

        if booking.status != 'confirmed':
            raise ValueError("Only confirmed bookings can be extended")

        # Check if extension is possible
        if not self.is_available_for_dates(booking.item_id, booking.end_date + timedelta(days=1), new_end_date):
            raise ValueError("Item is not available for the extended period")

        # Recalculate total price
        from app.services.item_service import ItemService
        item_service = ItemService()
        item = item_service.get_by_id(booking.item_id)

        new_duration = (new_end_date - booking.start_date).days + 1
        booking.total_price = new_duration * item.price_per_day
        booking.end_date = new_end_date

        return self.save(booking)
