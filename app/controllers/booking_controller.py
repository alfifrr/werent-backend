from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from app.models import Booking, User, Item
from app.extensions import db
from app.services.booking_service import BookingService
from app.services.user_service import UserService
from app.schemas.booking_schema import BookingCreate, BookingOut
from app.utils import (
    success_response,
    error_response,
    validation_error_response,
    not_found_response,
    unauthorized_response,
    internal_error_response
)
from typing import List, Optional
from datetime import date, datetime


def _get_user_id_from_jwt(jwt_identity):
    """Helper function to ensure JWT identity is an integer user ID."""
    if isinstance(jwt_identity, int):
        return jwt_identity
    try:
        return int(jwt_identity)
    except (ValueError, TypeError):
        return None


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

        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Validate using BookingCreate schema
        try:
            booking_data = BookingCreate(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        # Create booking using service
        try:
            booking = BookingService.create_booking(
                user_id=current_user_id,
                item_id=booking_data.item_id,
                start_date=booking_data.start_date,
                end_date=booking_data.end_date,
                quantity=booking_data.quantity
            )
        except ValueError as ve:
            error_msg = str(ve)
            if "Email verification required" in error_msg:
                return error_response(
                    "Email verification is required to create bookings. Please check your email for a verification link.",
                    403
                )
            elif "not available" in error_msg:
                return error_response("The selected item is not available for the chosen dates.", 409)
            elif "not found" in error_msg:
                return not_found_response("Item not found")
            else:
                return error_response(error_msg, 400)

        return success_response(
            message="Booking created successfully",
            data=BookingOut.from_orm(booking).dict(),
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def get_all_bookings_controller(current_user_id):
    """Controller to get all bookings (admin only)."""
    try:
        current_user_id = _get_user_id_from_jwt(current_user_id)
        
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)
        
        if not user or not user.is_admin:
            return error_response(
                message="Admin access required",
                error_code="INSUFFICIENT_PRIVILEGES",
                status_code=403
            )
        
        bookings = BookingService.get_all_bookings()
        
        return success_response(
            data=[booking.to_dict() for booking in bookings],
            message="All bookings retrieved successfully"
        )
    except Exception as e:
        return internal_error_response(
            message="Failed to retrieve bookings"
        )


def get_booking_controller(booking_id, current_user_id):
    """Handle getting a specific booking."""
    try:
        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Check if user is admin for access control
        user_id_for_check = current_user_id if not _is_admin(current_user_id) else None
        
        try:
            booking = BookingService.get_booking(booking_id, user_id_for_check)
        except ValueError as ve:
            error_msg = str(ve)
            if "Email verification required" in error_msg:
                return error_response(
                    "Email verification is required to access bookings. Please check your email for a verification link.",
                    403
                )
            elif "Access denied" in error_msg:
                return unauthorized_response("Access denied: You can only view your own bookings")
            elif "User not found" in error_msg:
                return unauthorized_response("Invalid user authentication")
            else:
                return error_response(error_msg, 400)
        
        if not booking:
            return not_found_response("Booking not found")

        return success_response(
            message="Booking retrieved successfully",
            data=BookingOut.from_orm(booking).dict()
        )

    except Exception as e:
        return internal_error_response()


def get_bookings_by_user_controller(user_id, current_user_id):
    """Handle getting bookings by user ID."""
    try:
        # Convert JWT identity (string) to int for comparison with route parameter
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")
        
        # Check if current user is requesting their own bookings or is admin
        if user_id != current_user_id and not _is_admin(current_user_id):
            return unauthorized_response("Access denied: You can only view your own bookings")

        try:
            bookings = BookingService.get_user_bookings(user_id)
        except ValueError as ve:
            error_msg = str(ve)
            if "Email verification required" in error_msg:
                return error_response(
                    "Email verification is required to access bookings. Please check your email for a verification link.",
                    403
                )
            elif "User not found" in error_msg:
                return not_found_response("User not found")
            else:
                return error_response(error_msg, 400)

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


def check_availability_controller(item_id, start_date, end_date, quantity=None):
    """Handle comprehensive availability check with quantity information."""
    try:
        if not (item_id and start_date and end_date):
            return error_response("item_id, start_date, and end_date are required", 400)

        # Default quantity to 1 if not provided
        requested_quantity = 1
        if quantity is not None:
            try:
                requested_quantity = int(quantity)
                if requested_quantity < 1 or requested_quantity > 10:
                    return error_response("Quantity must be between 1 and 10", 400)
            except (ValueError, TypeError):
                return error_response("Invalid quantity format", 400)

        try:
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
        except ValueError:
            return error_response("Invalid date format, use YYYY-MM-DD", 400)

        if start > end:
            return error_response("start_date must be before or equal to end_date", 400)

        try:
            # Expire old PENDING bookings before checking availability
            Booking.expire_pending_bookings()
            
            availability = BookingService.check_availability(item_id, start, end, requested_quantity)
            
            # Remove sensitive information like specific booking IDs for external API
            response_data = {
                'available': availability['available'],
                'available_quantity': availability['available_quantity'],
                'total_quantity': availability['total_quantity'],
                'requested_quantity': availability['requested_quantity'],
                'can_fulfill': availability['can_fulfill'],
                'booked_quantity': availability.get('booked_quantity', 0),
                'confirmed_reserved': availability.get('confirmed_reserved', 0),
                'pending_reserved': availability.get('pending_reserved', 0),
                'date_range': {
                    'start_date': start_date,
                    'end_date': end_date
                }
            }
            
            # Add error information if present
            if 'error' in availability:
                response_data['error'] = availability['error']
            
            return success_response(
                message="Availability check completed",
                data=response_data
            )
        except Exception as service_error:
            print(f"Service error: {service_error}")
            return error_response("Failed to check availability", 500)

    except Exception as e:
        print(f"Availability check error: {e}")  # Debug log
        return internal_error_response()


def get_availability_calendar_controller(item_id, start_date, end_date):
    """Handle availability calendar request for date range."""
    try:
        if not (item_id and start_date and end_date):
            return error_response("item_id, start_date, and end_date are required", 400)

        try:
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
        except ValueError:
            return error_response("Invalid date format, use YYYY-MM-DD", 400)

        if start > end:
            return error_response("start_date must be before or equal to end_date", 400)

        # Limit the range to prevent excessive queries (max 90 days)
        if (end - start).days > 90:
            return error_response("Date range cannot exceed 90 days", 400)

        try:
            calendar = Booking.get_availability_calendar(item_id, start, end)
            
            if 'error' in calendar:
                return error_response(calendar['error'], 404)
            
            return success_response(
                message="Availability calendar retrieved successfully",
                data={
                    'item_id': item_id,
                    'date_range': {
                        'start_date': start_date,
                        'end_date': end_date
                    },
                    'calendar': calendar
                }
            )
        except Exception as service_error:
            print(f"Calendar service error: {service_error}")
            return error_response("Failed to retrieve availability calendar", 500)

    except Exception as e:
        print(f"Availability calendar error: {e}")
        return internal_error_response()


def get_bookings_by_status_controller(status, current_user_id):
    """Handle getting bookings by status."""
    try:
        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Check if user is admin (status filtering is typically admin-only)
        if not _is_admin(current_user_id):
            return unauthorized_response("Admin access required to filter bookings by status")

        try:
            # Convert string status to enum
            from app.models.booking import BookingStatus
            status_enum = BookingStatus(status.upper())
        except ValueError:
            return error_response(f"Invalid status '{status}'. Valid statuses are: {[s.value for s in BookingStatus]}", 400)

        bookings = BookingService.get_bookings_by_status(status_enum)
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
        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        booking_service = BookingService()
        try:
            bookings = booking_service.get_booking_history(current_user_id, limit)
        except ValueError as ve:
            error_msg = str(ve)
            if "Email verification required" in error_msg:
                return error_response(
                    "Email verification is required to access booking history. Please check your email for a verification link.",
                    403
                )
            elif "User not found" in error_msg:
                return unauthorized_response("Invalid user authentication")
            else:
                return error_response(error_msg, 400)

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


def get_booking_statistics_controller(start_date_str, end_date_str, current_user_id):
    """Handle getting booking statistics."""
    try:
        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Check if user is admin (statistics are typically admin-only)
        if not _is_admin(current_user_id):
            return unauthorized_response("Admin access required to view booking statistics")

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


def get_bookings_by_item_controller(item_id, current_user_id):
    """Handle getting bookings for a specific item."""
    try:
        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Check if user is admin (item booking history is typically admin-only)
        if not _is_admin(current_user_id):
            return unauthorized_response("Admin access required to view item booking history")

        bookings = BookingService.get_bookings_by_item(item_id)
        booking_data = [BookingOut.from_orm(b).dict() for b in bookings]

        return success_response(
            message=f"Bookings for item {item_id} retrieved successfully",
            data=booking_data
        )

    except Exception as e:
        return internal_error_response()


def get_booking_duration_controller(booking_id, current_user_id):
    """Handle getting booking duration."""
    try:
        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Check if user is admin for access control
        user_id_for_check = current_user_id if not _is_admin(current_user_id) else None
        
        try:
            booking = BookingService.get_booking(booking_id, user_id_for_check)
        except ValueError as ve:
            error_msg = str(ve)
            if "Email verification required" in error_msg:
                return error_response(
                    "Email verification is required to access bookings. Please check your email for a verification link.",
                    403
                )
            elif "Access denied" in error_msg:
                return unauthorized_response("Access denied: You can only view your own bookings")
            elif "User not found" in error_msg:
                return unauthorized_response("Invalid user authentication")
            else:
                return error_response(error_msg, 400)
        
        if not booking:
            return not_found_response("Booking not found")

        booking_service = BookingService()
        duration = booking_service.calculate_duration_days(booking_id)

        return success_response(
            message="Booking duration calculated successfully",
            data={"duration_days": duration}
        )

    except Exception as e:
        return internal_error_response()


def get_revenue_controller(current_user_id, owner_id=None):
    """Handle getting revenue data."""
    try:
        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Check if user is admin (revenue data is typically admin-only)
        if not _is_admin(current_user_id):
            return unauthorized_response("Admin access required to view revenue data")

        target_owner_id = owner_id or current_user_id
        booking_service = BookingService()
        revenue = booking_service.calculate_total_revenue(target_owner_id)

        return success_response(
            message="Revenue data retrieved successfully",
            data={"total_revenue": revenue, "owner_id": target_owner_id}
        )

    except Exception as e:
        return internal_error_response()