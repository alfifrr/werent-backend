"""
Controller for ticketing endpoints.
Follows the same pattern as auth.py for consistent response handling.
"""

from flask import request
from pydantic import ValidationError
from app.services.ticketing_service import TicketingService
from app.schemas.ticketing_schema import (
    CreateTicketRequest,
    AddMessageRequest,
    TicketResponse,
    TicketListResponse,
    TicketStatsResponse
)
from app.utils import (
    success_response,
    error_response,
    validation_error_response,
    not_found_response,
    internal_error_response,
    forbidden_response,
)
from app.models.user import User


def _check_admin_access(current_user_id):
    """
    Check if current user has admin access.
    
    Args:
        current_user_id: ID of the current user from JWT
        
    Returns:
        tuple: (has_access: bool, user: User|None, error_response: dict|None)
    """
    try:
        # Convert to integer
        current_user_id = int(current_user_id)
        
        # Get current user
        user = User.find_by_id(current_user_id)
        if not user:
            return False, None, error_response("User not found", 404)
        
        # Check admin access
        is_admin = getattr(user, 'is_admin', False)
        if not is_admin:
            return False, user, forbidden_response('Admin access required')
            
        return True, user, None
        
    except Exception:
        return False, None, internal_error_response()


def _check_ticket_ownership_or_admin(current_user_id, ticket_id):
    """
    Check if current user can access a ticket (owner or admin).
    
    Args:
        current_user_id: ID of the current user from JWT
        ticket_id: ID of the ticket being accessed
        
    Returns:
        tuple: (has_access: bool, user: User|None, ticket: Ticketing|None, error_response: dict|None)
    """
    try:
        # Convert to integer
        current_user_id = int(current_user_id)
        
        # Get current user
        user = User.find_by_id(current_user_id)
        if not user:
            return False, None, None, error_response("User not found", 404)
            
        # Get ticket
        ticketing_service = TicketingService()
        ticket = ticketing_service.get_by_id(ticket_id)
        if not ticket:
            return False, user, None, error_response("Ticket not found", 404)
            
        # Check access: admin or ticket owner
        is_admin = getattr(user, 'is_admin', False)
        is_owner = ticket.user_id == current_user_id
        
        if not (is_admin or is_owner):
            return False, user, ticket, forbidden_response('Access denied - can only access own tickets')
            
        return True, user, ticket, None
        
    except Exception:
        return False, None, None, internal_error_response()


def _check_user_access_or_admin(current_user_id, target_user_id):
    """
    Check if current user can access target user's data (same user or admin).
    
    Args:
        current_user_id: ID of the current user from JWT
        target_user_id: ID of the user whose data is being accessed
        
    Returns:
        tuple: (has_access: bool, user: User|None, error_response: dict|None)
    """
    try:
        # Convert to integers for comparison
        current_user_id = int(current_user_id)
        target_user_id = int(target_user_id)
        
        # Get current user
        user = User.find_by_id(current_user_id)
        if not user:
            return False, None, error_response("User not found", 404)
        
        # Check access: admin or same user
        is_admin = getattr(user, 'is_admin', False)
        is_same_user = current_user_id == target_user_id
        
        if not (is_admin or is_same_user):
            return False, user, forbidden_response('Access denied - can only access own data')
            
        return True, user, None
        
    except Exception:
        return False, None, internal_error_response()


def _format_validation_errors(e: ValidationError):
    """Helper to format Pydantic validation errors for consistent API response."""
    field_errors = {}
    for error in e.errors():
        field_name = error["loc"][0] if error["loc"] else "unknown"
        if field_name not in field_errors:
            field_errors[field_name] = []
        field_errors[field_name].append(error["msg"])
    return validation_error_response(field_errors)


def _serialize_ticket(ticket):
    """
    Safely serialize ticket object to dictionary.

    Args:
        ticket: Ticket model instance

    Returns:
        Dictionary with serialized ticket data
    """
    if not ticket:
        return None

    try:
        return {
            'id': ticket.id,
            'user_id': ticket.user_id,
            'booking_id': ticket.booking_id,
            'chat_content': ticket.chat_content or '',
            'is_resolved': bool(ticket.is_resolved),
            'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
            'updated_at': ticket.updated_at.isoformat() if ticket.updated_at else None
        }
    except Exception:
        return {
            'id': getattr(ticket, 'id', None),
            'user_id': getattr(ticket, 'user_id', None),
            'booking_id': getattr(ticket, 'booking_id', None),
            'chat_content': getattr(ticket, 'chat_content', '') or '',
            'is_resolved': bool(getattr(ticket, 'is_resolved', False)),
            'created_at': None,
            'updated_at': None
        }


def _validate_id_parameter(id_value, id_name="ID"):
    """
    Validate ID parameters from URL.

    Args:
        id_value: ID value to validate
        id_name: Name of the ID for error messages

    Returns:
        Integer ID if valid

    Raises:
        ValueError: If ID is invalid
    """
    try:
        id_int = int(id_value)
        if id_int <= 0:
            raise ValueError(f"Invalid {id_name}: must be a positive integer")
        return id_int
    except (ValueError, TypeError):
        raise ValueError(f"Invalid {id_name}: must be a positive integer")



def create_ticket_controller(data):
    """Create a new support ticket."""
    try:
        print(f"DEBUG: Received data: {data}")  # Debug log

        if not data:
            return error_response("JSON payload required", 400)

        # Validate using Pydantic schema
        try:
            validated_data = CreateTicketRequest(**data)
            print(f"DEBUG: Validated data: {validated_data}")  # Debug log
        except ValidationError as e:
            print(f"DEBUG: Validation error: {e}")  # Debug log
            return _format_validation_errors(e)

        # Create ticket through service
        ticketing_service = TicketingService()
        ticket = ticketing_service.create_ticket(
            user_id=validated_data.user_id,
            initial_message=validated_data.message,
            booking_id=validated_data.booking_id
        )

        # Serialize and return response
        ticket_data = _serialize_ticket(ticket)
        return success_response(
            message="Ticket created successfully",
            data=ticket_data,
            status_code=201
        )

    except ValueError as e:
        print(f"DEBUG: ValueError: {e}")  # Debug log
        return error_response(str(e), 400)
    except Exception as e:
        print(f"DEBUG: Unexpected error: {e}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full traceback
        return internal_error_response()


def get_ticket_controller(ticket_id, current_user_id):
    """
    Get a specific ticket by ID.

    Args:
        ticket_id: ID of the ticket to retrieve
        current_user_id: ID of the current user from JWT token

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Validate ticket ID
        try:
            ticket_id = _validate_id_parameter(ticket_id, "ticket ID")
        except ValueError as e:
            return error_response(str(e), 400)

        # Check authorization (admin or ticket owner)
        has_access, user, ticket, auth_error = _check_ticket_ownership_or_admin(current_user_id, ticket_id)
        if not has_access:
            return auth_error

        # Return ticket data (ticket already retrieved in auth check)
        ticket_data = _serialize_ticket(ticket)
        return success_response(
            message="Ticket retrieved successfully",
            data=ticket_data
        )

    except Exception as e:
        return internal_error_response()


def add_message_controller(ticket_id, data):
    """
    Add a message to an existing ticket.

    Args:
        ticket_id: ID of the ticket to add message to
        data: Request data containing the message

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Validate ticket ID
        try:
            ticket_id = _validate_id_parameter(ticket_id, "ticket ID")
        except ValueError as e:
            return error_response(str(e), 400)

        if not data:
            return error_response("JSON payload required", 400)

        # Validate request data
        try:
            validated_data = AddMessageRequest(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        # Add message through service
        ticketing_service = TicketingService()
        ticket = ticketing_service.add_message(
            ticket_id=ticket_id,
            message=validated_data.message
        )

        # Return updated ticket
        ticket_data = _serialize_ticket(ticket)
        return success_response(
            message="Message added successfully",
            data=ticket_data
        )

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return internal_error_response()


def resolve_ticket_controller(ticket_id, current_user_id):
    """
    Mark a ticket as resolved (admin only).

    Args:
        ticket_id: ID of the ticket to resolve
        current_user_id: ID of the current user from JWT token

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Validate ticket ID
        try:
            ticket_id = _validate_id_parameter(ticket_id, "ticket ID")
        except ValueError as e:
            return error_response(str(e), 400)

        # Check admin authorization
        has_access, user, auth_error = _check_admin_access(current_user_id)
        if not has_access:
            return auth_error
        print("DEBUG: Admin access granted", user)
        # Resolve ticket through service
        ticketing_service = TicketingService()
        success = ticketing_service.resolve_ticket(ticket_id)
        print("DEBUG: Ticket resolved", success)
        if success:
            # Get updated ticket to return
            ticket = ticketing_service.get_by_id(ticket_id)
            print("DEBUG: Updated ticket", ticket)
            if ticket:
                serialized_ticket = _serialize_ticket(ticket)
                print("DEBUG: Serialized ticket", serialized_ticket)
                return success_response(
                    message="Ticket resolved successfully",
                    data={"ticket": serialized_ticket}
                )
            else:
                return error_response("Ticket not found after resolution", 404)
        else:
            return error_response("Failed to resolve ticket", 400)

    except Exception as e:
        return internal_error_response()


def reopen_ticket_controller(ticket_id, current_user_id):
    """
    Reopen a resolved ticket (admin or ticket owner).

    Args:
        ticket_id: ID of the ticket to reopen
        current_user_id: ID of the current user from JWT token

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Validate ticket ID
        try:
            ticket_id = _validate_id_parameter(ticket_id, "ticket ID")
        except ValueError as e:
            return error_response(str(e), 400)

        # Check authorization (admin or ticket owner)
        has_access, user, ticket, auth_error = _check_ticket_ownership_or_admin(current_user_id, ticket_id)
        if not has_access:
            return auth_error

        # Reopen ticket through service
        ticketing_service = TicketingService()
        success = ticketing_service.reopen_ticket(ticket_id)

        if success:
            # Get updated ticket to return
            updated_ticket = ticketing_service.get_by_id(ticket_id)
            if updated_ticket:
                serialized_ticket = _serialize_ticket(updated_ticket)
                return success_response(
                    message="Ticket reopened successfully",
                    data={"ticket": serialized_ticket}
                )
            else:
                return error_response("Ticket not found after reopening", 404)
        else:
            return error_response("Failed to reopen ticket", 400)

    except Exception as e:
        return internal_error_response()


def get_user_tickets_controller(user_id, current_user_id):
    """
    Get all tickets for a specific user.

    Args:
        user_id: ID of the user whose tickets to retrieve
        current_user_id: ID of the current user from JWT token

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Validate user ID
        try:
            user_id = _validate_id_parameter(user_id, "user ID")
        except ValueError as e:
            return error_response(str(e), 400)

        # Check authorization (admin or same user)
        has_access, user, auth_error = _check_user_access_or_admin(current_user_id, user_id)
        if not has_access:
            print("DEBUG: User access denied", user)
            return auth_error

        # Get tickets from service
        ticketing_service = TicketingService()
        tickets = ticketing_service.get_user_tickets(user_id)

        # Serialize all tickets
        serialized_tickets = [_serialize_ticket(ticket) for ticket in tickets]
        response_data = {
            "tickets": serialized_tickets,
            "total_count": len(tickets)
        }

        return success_response(
            message="User tickets retrieved successfully",
            data=response_data
        )

    except Exception as e:
        return internal_error_response()


def get_open_tickets_controller(current_user_id):
    """
    Get all open tickets (admin only).

    Args:
        current_user_id: ID of the current user from JWT token

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Check admin authorization
        has_access, user, auth_error = _check_admin_access(current_user_id)
        if not has_access:
            return auth_error

        # Get open tickets from service
        ticketing_service = TicketingService()
        tickets = ticketing_service.get_open_tickets()

        # Serialize all tickets
        serialized_tickets = [_serialize_ticket(ticket) for ticket in tickets]
        response_data = {
            "tickets": serialized_tickets,
            "total_count": len(tickets)
        }

        return success_response(
            message="Open tickets retrieved successfully",
            data=response_data
        )

    except Exception as e:
        return internal_error_response()


def get_resolved_tickets_controller(current_user_id):
    """
    Get all resolved tickets (admin only).

    Args:
        current_user_id: ID of the current user from JWT token

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Check admin authorization
        has_access, user, auth_error = _check_admin_access(current_user_id)
        if not has_access:
            return auth_error

        # Get resolved tickets from service
        ticketing_service = TicketingService()
        tickets = ticketing_service.get_resolved_tickets()

        # Serialize all tickets
        serialized_tickets = [_serialize_ticket(ticket) for ticket in tickets]
        response_data = {
            "tickets": serialized_tickets,
            "total_count": len(tickets)
        }

        return success_response(
            message="Resolved tickets retrieved successfully",
            data=response_data
        )

    except Exception as e:
        return internal_error_response()


def get_ticket_stats_controller(current_user_id):
    """
    Get ticket statistics (admin only).

    Args:
        current_user_id: ID of the current user from JWT token

    Returns:
        Flask response tuple: (response_dict, status_code)
    """
    try:
        # Check admin authorization
        has_access, user, auth_error = _check_admin_access(current_user_id)
        if not has_access:
            return auth_error

        # Get stats from service
        ticketing_service = TicketingService()
        stats = ticketing_service.get_ticket_stats()

        return success_response(
            message="Ticket statistics retrieved successfully",
            data=stats
        )

    except Exception as e:
        return internal_error_response()
