from datetime import datetime, timedelta, date
from app.services.base_service import BaseService
from app.models.booking import Booking, BookingStatus
from app.models.item import Item
from app.models.user import User
from app.extensions import db
from sqlalchemy.orm import joinedload
from typing import List, Optional


class BookingService(BaseService):

    def __init__(self):
        super().__init__(Booking)

    @staticmethod
    def check_availability(item_id: int, start_date: date, end_date: date, requested_quantity: int = 1) -> dict:
        """
        Check item availability using the comprehensive booking model method.
        
        Args:
            item_id: ID of the item to check
            start_date: Start date for booking
            end_date: End date for booking
            requested_quantity: Number of items requested (default: 1)
            
        Returns:
            dict: Detailed availability information
        """
        try:
            return Booking.check_item_availability(item_id, start_date, end_date, requested_quantity)
        except Exception as e:
            print(f"BookingService.check_availability error: {e}")
            # Return unavailable if there's an error to prevent double bookings
            return {
                'available': False,
                'available_quantity': 0,
                'total_quantity': 0,
                'requested_quantity': requested_quantity,
                'can_fulfill': False,
                'error': str(e)
            }

    @staticmethod
    def create_booking(user_id: int, item_id: int, start_date: date, end_date: date, quantity: int = 1) -> Optional[Booking]:
        # Check user exists and is verified
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if not getattr(user, 'is_verified', False):
            raise ValueError("Email verification is required to create bookings. Please check your email for a verification link.")
        
        # Validate quantity
        if quantity < 1 or quantity > 10:
            raise ValueError("Quantity must be between 1 and 10")
        
        # Check availability using the comprehensive method
        availability = BookingService.check_availability(item_id, start_date, end_date, quantity)
        if not availability['available'] or not availability['can_fulfill']:
            if 'error' in availability:
                raise ValueError(f"Availability check failed: {availability['error']}")
            else:
                available_qty = availability['available_quantity']
                total_qty = availability['total_quantity']
                raise ValueError(
                    f"Insufficient quantity available. "
                    f"Requested: {quantity}, Available: {available_qty}/{total_qty}"
                )
            
        item = Item.query.get(item_id)
        if not item:
            raise ValueError("Item not found")
            
        duration = (end_date - start_date).days + 1
        total_price = item.price_per_day * duration * quantity  # Price includes quantity
        booking = Booking(
            user_id=user_id,
            item_id=item_id,
            start_date=start_date,
            end_date=end_date,
            quantity=quantity,
            total_price=total_price,
            status=BookingStatus.PENDING,
            is_paid=False
        )
        
        # Set expiration for PENDING booking (30 minutes from creation)
        booking.expires_at = datetime.utcnow() + timedelta(minutes=30)
        
        db.session.add(booking)
        db.session.commit()
        return booking

    @staticmethod
    def get_user_bookings(user_id: int) -> List[Booking]:
        from sqlalchemy.orm import joinedload
        # Check user exists and is verified
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if not getattr(user, 'is_verified', False):
            raise ValueError("Email verification required to access bookings")
        return Booking.query.options(joinedload(Booking.item)).filter_by(user_id=user_id).all()

    @staticmethod
    def get_booking(booking_id: int, user_id: Optional[int] = None) -> Optional[Booking]:
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
        # If user_id is provided, verify user and check if booking belongs to them
        if user_id is not None:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
            if not getattr(user, 'is_verified', False):
                raise ValueError("Email verification required to access bookings")
            if booking.user_id != user_id:
                raise ValueError("Access denied: Booking does not belong to user")
                
        return booking

    @staticmethod
    def update_booking(booking_id: int, user_id: Optional[int] = None, **kwargs) -> Optional[Booking]:
        """
        Update booking status only. All other fields are not allowed to be updated.
        
        Args:
            booking_id: ID of the booking to update
            user_id: Optional user ID to verify ownership
            **kwargs: Should only contain 'status' field
            
        Returns:
            Updated booking if successful, None otherwise
        """
        # Only allow status updates
        if 'status' not in kwargs or len(kwargs) > 1:
            return None
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
        # If user_id is provided, verify user exists and is verified
        if user_id is not None:
            user = User.query.get(user_id)
            if not user or not getattr(user, 'is_verified', False):
                return None
            # Only check ownership if user is not an admin
            if not getattr(user, 'is_admin', False) and booking.user_id != user_id:
                return None

        # Only update the status field
        new_status = kwargs.get('status')
        if new_status and hasattr(booking, 'status'):
            booking.status = new_status
            db.session.commit()
            return booking

        return None

    @staticmethod
    def get_all_bookings() -> List[Booking]:
        """Get all bookings in the system with pagination."""
        return Booking.query.options(joinedload(Booking.item)).order_by(Booking.created_at.desc()).all()

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

    @staticmethod
    def get_bookings_by_item(item_id):
        """Get all bookings for a specific item."""
        return Booking.query.filter_by(item_id=item_id).order_by(Booking.created_at.desc()).all()

    @staticmethod
    def get_bookings_by_status(status):
        """Get all bookings with a specific status."""
        # Accept both Enum and string
        if isinstance(status, str):
            status = status.upper()
        return Booking.query.filter_by(status=status).order_by(Booking.created_at.desc()).all()

    def get_booking_history(self, user_id, limit=20):
        """Get booking history for a user."""
        # Check user exists and is verified
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if not getattr(user, 'is_verified', False):
            raise ValueError("Email verification required to access booking history")
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

