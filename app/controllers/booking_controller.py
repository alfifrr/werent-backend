from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from app.models import Booking, User, Item
from app.extensions import db
from app.services.booking_service import BookingService
from app.schemas.booking_schema import BookingCreate, BookingOut
from app.utils import (
    success_response,
    error_response,
    validation_error_response,
    not_found_response,
    unauthorized_response,
    internal_error_response,
)
from typing import List, Optional
from datetime import date, datetime


def _format_validation_errors(e: ValidationError):
    """Helper to format Pydantic validation errors for consistent API response."""
    field_errors = {}
    for error in e.errors():
        field_name = error["loc"][0] if error["loc"] else "unknown"
        if field_name not in field_errors:
            field_errors[field_name] = []
        field_errors[field_name].append(error["msg"])
    return validation_error_response(field_errors)


def _is_admin(current_user_id):
    """Helper function to check if current user is admin."""
    user = User.query.get(current_user_id)
    return user and getattr(user, 'is_admin', False)


def create_booking_controller(data, current_user_id):
    """Handle booking creation with validation."""
    try:
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using BookingCreate schema
        try:
            booking_data = BookingCreate(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        # Create booking using service
        booking = BookingService.create_booking(
            user_id=current_user_id,
            item_id=booking_data.item_id,
            start_date=booking_data.start_date,
            end_date=booking_data.end_date
        )

        if not booking:
            return error_response("Booking creation failed. Check if item is available, exists, and user is verified.", 400)

        return success_response(
            message="Booking created successfully",
            data=BookingOut.from_orm(booking).dict(),
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def get_all_bookings_controller(current_user_id):
    """Handle getting all bookings (admin only)."""
    try:
        # Check if user is admin
        if not _is_admin(current_user_id):
            return unauthorized_response("Admin access required")

        bookings = BookingService.get_all_bookings()
        booking_data = [BookingOut.from_orm(b).dict() for b in bookings]

        return success_response(
            message="All bookings retrieved successfully",
            data=booking_data
        )

    except Exception as e:
        return internal_error_response()


def get_booking_controller(booking_id, current_user_id):
    """Handle getting a specific booking."""
    try:
        # Check if user is admin for access control
        user_id_for_check = current_user_id if not _is_admin(current_user_id) else None
        booking = BookingService.get_booking(booking_id, user_id_for_check)
        
        if not booking:
            return not_found_response("Booking not found or access denied")

        return success_response(
            message="Booking retrieved successfully",
            data=BookingOut.from_orm(booking).dict()
        )

    except Exception as e:
        return internal_error_response()


def get_bookings_by_user_controller(user_id, current_user_id):
    """Handle getting bookings by user ID."""
    try:
        # Check if current user is requesting their own bookings or is admin
        if user_id != current_user_id and not _is_admin(current_user_id):
            return unauthorized_response("Access denied")

        bookings = BookingService.get_user_bookings(user_id)
        booking_data = [BookingOut.from_orm(b).dict() for b in bookings]

        return success_response(
            message="User bookings retrieved successfully",
            data=booking_data
        )

    except Exception as e:
        return internal_error_response()


def update_booking_controller(booking_id, data, current_user_id):
    """Handle booking update."""
    try:
        if not data:
            return error_response("JSON payload required", 400)

        # Check if booking exists
        booking = BookingService.get_booking(booking_id)
        if not booking:
            return not_found_response("Booking not found")

        # Check if user owns the booking or is admin
        if booking.user_id != current_user_id and not _is_admin(current_user_id):
            return unauthorized_response("Access denied")

        # Update booking using service
        user_id_for_check = current_user_id if not _is_admin(current_user_id) else None
        updated_booking = BookingService.update_booking(booking_id, user_id_for_check, **data)
        
        if not updated_booking:
            return error_response("Booking update failed", 400)

        return success_response(
            message="Booking updated successfully",
            data=BookingOut.from_orm(updated_booking).dict()
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def check_availability_controller(item_id, start_date, end_date):
    """Handle availability check."""
    try:
        if not (item_id and start_date and end_date):
            return error_response("item_id, start_date, and end_date are required", 400)

        try:
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
        except ValueError:
            return error_response("Invalid date format, use YYYY-MM-DD", 400)

        available = BookingService.check_availability(item_id, start, end)
        return success_response(
            message="Availability check completed",
            data={"available": available}
        )

    except Exception as e:
        return internal_error_response()


def get_bookings_by_status_controller(status):
    """Handle getting bookings by status."""
    try:
        booking_service = BookingService()
        bookings = booking_service.get_bookings_by_status(status)
        booking_data = [BookingOut.from_orm(b).dict() for b in bookings]

        return success_response(
            message=f"Bookings with status '{status}' retrieved successfully",
            data=booking_data
        )

    except Exception as e:
        return internal_error_response()


def get_booking_history_controller(current_user_id, limit=20):
    """Handle getting booking history for current user."""
    try:
        booking_service = BookingService()
        bookings = booking_service.get_booking_history(current_user_id, limit)
        booking_data = [BookingOut.from_orm(b).dict() for b in bookings]

        return success_response(
            message="Booking history retrieved successfully",
            data=booking_data
        )

    except Exception as e:
        return internal_error_response()


def get_bookings_by_item_controller(item_id, current_user_id):
    """Handle getting bookings by item ID."""
    try:
        # Note: Currently returns all bookings for the item
        # You might want to add authorization check to ensure user owns the item
        booking_service = BookingService()
        bookings = booking_service.get_bookings_by_item(item_id)
        booking_data = [BookingOut.from_orm(b).dict() for b in bookings]

        return success_response(
            message="Item bookings retrieved successfully",
            data=booking_data
        )

    except Exception as e:
        return internal_error_response()


def get_booking_duration_controller(booking_id, current_user_id):
    """Handle getting booking duration."""
    try:
        # Check if user is admin for access control
        user_id_for_check = current_user_id if not _is_admin(current_user_id) else None
        booking = BookingService.get_booking(booking_id, user_id_for_check)
        
        if not booking:
            return not_found_response("Booking not found or access denied")

        booking_service = BookingService()
        duration = booking_service.calculate_duration_days(booking_id)

        return success_response(
            message="Booking duration calculated successfully",
            data={"duration_days": duration}
        )

    except Exception as e:
        return internal_error_response()


def get_revenue_controller(current_user_id):
    """Handle getting revenue statistics for current user's items."""
    try:
        booking_service = BookingService()
        total_revenue = booking_service.calculate_total_revenue(current_user_id)

        return success_response(
            message="Revenue calculated successfully",
            data={"total_revenue": total_revenue}
        )

    except Exception as e:
        return internal_error_response()


def get_booking_statistics_controller(start_date_str=None, end_date_str=None):
    """Handle getting booking statistics."""
    try:
        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str)
            except ValueError:
                return error_response("Invalid start_date format, use YYYY-MM-DD", 400)

        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str)
            except ValueError:
                return error_response("Invalid end_date format, use YYYY-MM-DD", 400)

        booking_service = BookingService()
        stats = booking_service.get_booking_statistics(start_date, end_date)

        return success_response(
            message="Booking statistics retrieved successfully",
            data=stats
        )

    except Exception as e:
        return internal_error_response() 