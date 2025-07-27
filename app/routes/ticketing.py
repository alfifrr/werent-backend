"""
Routes for ticketing endpoints with proper authentication and authorization.
Following clean architecture with role-based access control.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.ticketing_controller import (
    create_ticket_controller,
    get_ticket_controller,
    add_message_controller,
    resolve_ticket_controller,
    reopen_ticket_controller,
    get_user_tickets_controller,
    get_open_tickets_controller,
    get_resolved_tickets_controller,
    get_ticket_stats_controller
)

ticketing_bp = Blueprint('ticketing', __name__, url_prefix='/api/tickets')

# User routes - authenticated users only
@ticketing_bp.route('', methods=['POST'])
@jwt_required()
def create_ticket():
    """
    Create a new ticket.

    Access: Authenticated users can create tickets for themselves.
    The user_id will be extracted from JWT token for security.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    # Ensure the ticket is created by the authenticated user
    data['user_id'] = current_user_id
    return create_ticket_controller(data)

@ticketing_bp.route('/<int:ticket_id>', methods=['GET'])
@jwt_required()
def get_ticket(ticket_id):
    """
    Get a specific ticket by ID.

    Access Control:
    - Users: Can only view tickets they created
    - Admin: Can view any ticket
    """
    current_user_id = get_jwt_identity()
    # Pass current_user_id to controller for authorization
    return get_ticket_controller(ticket_id, current_user_id)

@ticketing_bp.route('/<int:ticket_id>/message', methods=['POST'])
@jwt_required()
def add_message(ticket_id):
    """
    Add a message to an existing ticket.

    Access Control:
    - Users: Can only add messages to their own tickets
    - Admin: Can add messages to any ticket
    """
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    # Add current_user_id to data for authorization in controller
    data['current_user_id'] = current_user_id
    return add_message_controller(ticket_id, data)

@ticketing_bp.route('/<int:ticket_id>/resolve', methods=['PATCH'])
@jwt_required()
def resolve_ticket(ticket_id):
    """
    Mark a ticket as resolved.

    Access Control:
    - Users: Cannot resolve tickets
    - Admin: Can resolve any ticket
    """
    current_user_id = get_jwt_identity()
    # Pass current_user_id to controller for authorization
    return resolve_ticket_controller(ticket_id, current_user_id)

@ticketing_bp.route('/<int:ticket_id>/reopen', methods=['PATCH'])
@jwt_required()
def reopen_ticket(ticket_id):
    """
    Reopen a resolved ticket.

    Access Control:
    - Users: Can only reopen their own tickets
    - Admin: Can reopen any ticket
    """
    current_user_id = get_jwt_identity()
    # Pass current_user_id to controller for authorization
    return reopen_ticket_controller(ticket_id, current_user_id)

@ticketing_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_tickets(user_id):
    """
    Get all tickets for a specific user.

    Access Control:
    - Users: Can only get their own tickets (user_id must match JWT identity)
    - Admin: Can get tickets for any user
    """
    current_user_id = get_jwt_identity()
    # Pass current_user_id to controller for authorization
    return get_user_tickets_controller(user_id, current_user_id)

@ticketing_bp.route('/open', methods=['GET'])
@jwt_required()
def get_open_tickets():
    """
    Get all open (unresolved) tickets across all users.

    Access Control:
    - Users: Cannot access (will get 403 Forbidden)
    - Admin: Can view all open tickets
    """
    current_user_id = get_jwt_identity()
    # Pass current_user_id to controller for authorization
    return get_open_tickets_controller(current_user_id)

@ticketing_bp.route('/resolved', methods=['GET'])
@jwt_required()
def get_resolved_tickets():
    """
    Get all resolved tickets across all users.

    Access Control:
    - Users: Cannot access (will get 403 Forbidden)
    - Admin: Can view all resolved tickets
    """
    current_user_id = get_jwt_identity()
    # Pass current_user_id to controller for authorization
    return get_resolved_tickets_controller(current_user_id)

@ticketing_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_ticket_stats():
    """
    Get ticket statistics for admin dashboard.

    Access Control:
    - Users: Cannot access (will get 403 Forbidden)
    - Admin: Can view ticket statistics
    """
    current_user_id = get_jwt_identity()
    # Pass current_user_id to controller for authorization
    return get_ticket_stats_controller(current_user_id)