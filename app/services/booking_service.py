from datetime import datetime, timedelta
from app.services.base_service import BaseService
from app.models.booking import Booking, BookingStatus
from app.models.item import Item
from app.models.user import User
from app.extensions import db
from typing import List, Optional
from datetime import date


class BookingService(BaseService):

    def __init__(self):
        super().__init__(Booking)

    @staticmethod
    def check_availability(item_id: int, start_date: date, end_date: date) -> bool:
        overlapping = Booking.query.filter(
            Booking.item_id == item_id,
            Booking.end_date >= start_date,
            Booking.start_date <= end_date,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.PAID])
        ).first()
        return overlapping is None

    @staticmethod
    def create_booking(user_id: int, item_id: int, start_date: date, end_date: date) -> Optional[Booking]:
        # Check user exists and is verified
        user = User.query.get(user_id)
        if not user or not getattr(user, 'is_verified', False):
            return None
            
        if not BookingService.check_availability(item_id, start_date, end_date):
            return None
        item = Item.query.get(item_id)
        if not item:
            return None
        duration = (end_date - start_date).days + 1
        total_price = item.price_per_day * duration
        booking = Booking(
            user_id=user_id,
            item_id=item_id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status=BookingStatus.PENDING,
            is_paid=False
        )
        db.session.add(booking)
        db.session.commit()
        return booking

    @staticmethod
    def get_user_bookings(user_id: int) -> List[Booking]:
        # Check user exists and is verified
        user = User.query.get(user_id)
        if not user or not getattr(user, 'is_verified', False):
            return []
        return Booking.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_booking(booking_id: int, user_id: Optional[int] = None) -> Optional[Booking]:
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
        # If user_id is provided, verify user and check if booking belongs to them
        if user_id is not None:
            user = User.query.get(user_id)
            if not user or not getattr(user, 'is_verified', False):
                return None
            if booking.user_id != user_id:
                return None
                
        return booking

    @staticmethod
    def update_booking(booking_id: int, user_id: Optional[int] = None, **kwargs) -> Optional[Booking]:
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
            
        # If user_id is provided, verify user and check if booking belongs to them
        if user_id is not None:
            user = User.query.get(user_id)
            if not user or not getattr(user, 'is_verified', False):
                return None
            if booking.user_id != user_id:
                return None
                
        # Convert date strings to date objects
        for key, value in kwargs.items():
            if key in ['start_date', 'end_date'] and isinstance(value, str):
                try:
                    value = date.fromisoformat(value)
                except ValueError:
                    continue  # skip invalid date
            # Ensure start_date is not before booking creation date
            if key == 'start_date' and value is not None:
                created_date = booking.__dict__.get('created_at')
                if created_date:
                    if hasattr(created_date, 'date'):
                        created_date = created_date.date()
                    if value < created_date:
                        return None  # Invalid: start_date before booking creation
            # Ensure end_date is not before start_date
            if key == 'end_date' and value is not None:
                start_date = kwargs.get('start_date', booking.start_date)
                if isinstance(start_date, str):
                    try:
                        start_date = date.fromisoformat(start_date)
                    except ValueError:
                        continue
                if value < start_date:
                    return None  # Invalid: end_date before start_date
            if hasattr(booking, key) and value is not None:
                setattr(booking, key, value)
        # Recalculate total_price if start_date or end_date changed
        if 'start_date' in kwargs or 'end_date' in kwargs:
            start_date = booking.start_date
            end_date = booking.end_date
            if start_date and end_date and booking.item:
                duration = (end_date - start_date).days + 1
                booking.total_price = booking.item.price_per_day * duration
        db.session.commit()
        return booking

    @staticmethod
    def get_all_bookings() -> List[Booking]:
        """Get all bookings in the system with pagination."""
        return Booking.query.order_by(Booking.created_at.desc()).all()

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

    def get_bookings_by_renter(self, renter_id):
        """Get all bookings made by a specific renter."""
        # Check user exists and is verified
        user = User.query.get(renter_id)
        if not user or not getattr(user, 'is_verified', False):
            return []
        return Booking.query.filter_by(user_id=renter_id).order_by(Booking.created_at.desc()).all()

    def get_bookings_by_item(self, item_id):
        """Get all bookings for a specific item."""
        return Booking.query.filter_by(item_id=item_id).order_by(Booking.created_at.desc()).all()

    def get_bookings_by_status(self, status):
        """Get all bookings with a specific status."""
        # Accept both Enum and string
        if isinstance(status, str):
            status = status.upper()
        return Booking.query.filter_by(status=status).order_by(Booking.created_at.desc()).all()

    def get_booking_history(self, user_id, limit=20):
        """Get booking history for a user."""
        # Check user exists and is verified
        user = User.query.get(user_id)
        if not user or not getattr(user, 'is_verified', False):
            return []
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

        # Check user exists and is verified
        user = User.query.get(owner_id)
        if not user or not getattr(user, 'is_verified', False):
            return 0

        completed_bookings = Booking.query.join(Item).filter(
            Item.user_id == owner_id,
            Booking.status == 'COMPLETED'
        ).all()

        return sum(booking.total_price for booking in completed_bookings)

    def get_booking_statistics(self, start_date=None, end_date=None):
        query = Booking.query

        if start_date:
            query = query.filter(Booking.created_at >= start_date)
        if end_date:
            query = query.filter(Booking.created_at <= end_date)

        bookings = query.all()

        # Debug print
        print("Booking statuses in statistics:")
        for b in bookings:
            print(f"Booking ID: {b.id}, Status: {b.status} ({type(b.status)})")

        return {
            'total_bookings': len(bookings),
            'pending_bookings': len([b for b in bookings if b.status and (b.status.value.upper() if hasattr(b.status, 'value') else str(b.status).upper()) == 'PENDING']),
            'confirmed_bookings': len([b for b in bookings if b.status and (b.status.value.upper() if hasattr(b.status, 'value') else str(b.status).upper()) == 'CONFIRMED']),
            'completed_bookings': len([b for b in bookings if b.status and (b.status.value.upper() if hasattr(b.status, 'value') else str(b.status).upper()) == 'COMPLETED']),
            'cancelled_bookings': len([b for b in bookings if b.status and (b.status.value.upper() if hasattr(b.status, 'value') else str(b.status).upper()) == 'CANCELLED']),
            'pastdue_bookings': len([b for b in bookings if b.status and (b.status.value.upper() if hasattr(b.status, 'value') else str(b.status).upper()) == 'PASTDUE']),
            'returned_bookings': len([b for b in bookings if b.status and (b.status.value.upper() if hasattr(b.status, 'value') else str(b.status).upper()) == 'RETURNED']),
            'total_revenue': sum(b.total_price for b in bookings if b.status and (b.status.value.upper() if hasattr(b.status, 'value') else str(b.status).upper()) == 'COMPLETED')
        }