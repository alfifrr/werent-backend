from datetime import date, datetime
from pydantic import ValidationError
from app.models import Booking, User
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
        print(f"Error in create_booking_controller: {str(e)}")
        db.session.rollback()
        return internal_error_response()


def get_all_bookings_controller(current_user_id):
    """
    Controller to get bookings based on user role:
    - Admin users: Get all bookings from all users
    - Regular users: Get only their own bookings
    """
    try:
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")
        
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)
        
        if not user:
            return not_found_response("User not found")
        
        # Check if user has admin privileges
        if user.is_admin:
            # Admin can see all bookings
            bookings = BookingService.get_all_bookings()
            message = "All bookings retrieved successfully"
        else:
            # Regular user can only see their own bookings
            bookings = BookingService.get_user_bookings(current_user_id)
            message = "Your bookings retrieved successfully"
        
        # Convert bookings to dict and add item_name
        bookings_data = []
        for booking in bookings:
            booking_dict = BookingOut.model_validate(booking).model_dump()
            booking_dict['item_name'] = booking.item.name
            bookings_data.append(booking_dict)
        
        return success_response(
            data=bookings_data,
            message=message
        )
    except Exception as e:
        print(f"Error in get_all_bookings_controller: {str(e)}")
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
        print(f"Error in get_booking_controller: {str(e)}")
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

        # Convert bookings to dict and include item_name
        booking_data = []
        for booking in bookings:
            booking_dict = BookingOut.model_validate(booking).model_dump()
            # Add item_name from the relationship
            booking_dict['item_name'] = booking.item.name if booking.item else None
            booking_data.append(booking_dict)

        return success_response(
            message="User bookings retrieved successfully",
            data=booking_data
        )

    except Exception as e:
        print(f"Error in get_bookings_by_user_controller: {str(e)}")
        return internal_error_response()


def update_booking_controller(booking_id, data, current_user_id):
    """
    Handle booking status update.
    
    This endpoint only allows updating the booking status, not the dates.
    Users can only cancel their own bookings (if status is PENDING or CONFIRMED).
    Admins can update to any status.
    """
    try:
        if not data or 'status' not in data:
            return error_response("Status field is required in the payload", 400)

        # Convert JWT identity to int
        current_user_id = _get_user_id_from_jwt(current_user_id)
        if current_user_id is None:
            return unauthorized_response("Invalid user authentication")

        # Get the booking
        booking = BookingService.get_booking(booking_id)
        if not booking:
            return not_found_response("Booking not found")

        # Get current status, handling both enum and string statuses
        current_status = booking.status.value if hasattr(booking.status, 'value') else str(booking.status).upper()
        new_status = data['status'].upper()

        # Check if user owns the booking or is admin
        is_owner = booking.user_id == current_user_id
        is_admin = _is_admin(current_user_id)
        
        if not is_owner and not is_admin:
            return unauthorized_response("Access denied")

        # Define allowed status transitions
        user_allowed_transitions = {
            'PENDING': ['CANCELLED'],
            'CONFIRMED': ['CANCELLED', 'RETURNED']
        }
        
        # Admin can change any status, but we still validate it's a valid status
        if not is_admin:
            # For non-admin users, check if the status transition is allowed
            if current_status not in user_allowed_transitions:
                return error_response(
                    f"Cannot update status from {current_status}",
                    400
                )
                
            if new_status not in user_allowed_transitions[current_status]:
                return error_response(
                    f"Status change from {current_status} to {new_status} is not allowed. "
                    f"You can only cancel PENDING or CONFIRMED bookings.",
                    403
                )

        # Update only the status field
        update_data = {'status': new_status}
        
        # Update booking using service
        updated_booking = BookingService.update_booking(booking_id, current_user_id, **update_data)
        
        if not updated_booking:
            return error_response("Failed to update booking status", 400)

        return success_response(
            message="Booking status updated successfully",
            data=BookingOut.from_orm(updated_booking).dict()
        )

    except Exception as e:
        print(f"Error in update_booking_controller: {str(e)}")
        db.session.rollback()
        return internal_error_response(str(e))


def cancel_booking_controller(booking_id, current_user_id):
    """
    Dedicated endpoint to cancel a booking with RBAC.
    Industry best practice for better UX and security.
    
    Business Rules:
    - Users can cancel their own PENDING or CONFIRMED bookings
    - Admins can cancel any booking regardless of status
    - Provides clear, single-purpose action
    - More secure than general PUT endpoint
    """
    try:
        # Convert JWT string to integer
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        # Get booking and verify it exists
        booking = BookingService.get_booking(booking_id, 
                                           None if _is_admin(current_user_id) else current_user_id)
        
        if not booking:
            return error_response("Booking not found", 404)
        
        # Check current status to provide better error messages
        current_status = booking.status.value if hasattr(booking.status, 'value') else str(booking.status)
        
        # Admin can cancel any booking
        if _is_admin(current_user_id):
            # Admin can cancel any status, but provide warnings for business logic
            if current_status in ['COMPLETED', 'RETURNED']:
                return error_response(
                    f"Cannot cancel {current_status} booking. "
                    "Consider creating a refund/return process instead.",
                    403
                )
        else:
            # Regular users have restrictions
            if current_status not in ['PENDING', 'CONFIRMED']:
                if current_status == 'CANCELLED':
                    return error_response("Booking is already cancelled", 400)
                elif current_status in ['PAID', 'COMPLETED', 'RETURNED']:
                    return error_response(
                        f"Cannot cancel {current_status} booking. Please contact support for assistance.",
                        403
                    )
                elif current_status == 'PASTDUE':
                    return error_response(
                        "Cannot cancel overdue booking. Please contact support to resolve.",
                        403
                    )
        
        # Perform the cancellation using the existing update service
        cancelled_booking = BookingService.update_booking(
            booking_id, 
            None if _is_admin(current_user_id) else current_user_id,
            status='CANCELLED'
        )
        
        if not cancelled_booking:
            return error_response("Failed to cancel booking", 400)
        
        # Calculate potential refund info (for future implementation)
        from datetime import datetime
        refund_info = {
            'cancellation_reason': 'User requested',
            'cancelled_at': datetime.utcnow().isoformat(),
            'original_total': float(cancelled_booking.total_price),
            'refund_eligible': current_status in ['PENDING', 'CONFIRMED'],
            'refund_amount': float(cancelled_booking.total_price) if current_status == 'PENDING' else 0.0
        }
        
        response_data = BookingOut.from_orm(cancelled_booking).dict()
        response_data['refund_info'] = refund_info
        
        return success_response(
            message=f"Booking cancelled successfully. Status changed from {current_status} to CANCELLED.",
            data=response_data
        )
        
    except ValueError as e:
        return error_response(f"Invalid booking ID: {str(e)}", 400)
    except Exception as e:
        print(f"Error in cancel_booking_controller: {str(e)}")
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
            # Availability checking now uses time-based expiration logic
            # No need to explicitly expire bookings - done at query time
            
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
        print(f"Availability check error: {e}")
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
        print(f"Error in get_bookings_by_status_controller: {str(e)}")
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
        print(f"Error in get_booking_history_controller: {str(e)}")
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
        print(f"Error in get_booking_statistics_controller: {str(e)}")
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
        print(f"Error in get_bookings_by_item_controller: {str(e)}")
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
        print(f"Error in get_booking_duration_controller: {str(e)}")
        return internal_error_response()


def get_revenue_controller(current_user_id, owner_id=None):
    """Handle getting revenue data.
    
    Args:
        current_user_id: The ID of the current user (from JWT)
        owner_id: Optional owner ID to get revenue for (admin only)
    """
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
        print(f"Error in get_revenue_controller: {str(e)}")
        return internal_error_response()