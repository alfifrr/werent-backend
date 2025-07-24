"""
Routes for ticketing endpoints.
"""

from flask import Blueprint
from app.controllers.ticketing_controller import TicketingController

ticketing_bp = Blueprint('ticketing', __name__, url_prefix='/api/tickets')
controller = TicketingController()

# Ticket routes
@ticketing_bp.route('', methods=['POST'])
def create_ticket():
    """Create a new ticket."""
    return controller.create_ticket()

@ticketing_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket by ID."""
    return controller.get_ticket(ticket_id)

@ticketing_bp.route('/<int:ticket_id>/message', methods=['POST'])
def add_message(ticket_id):
    """Add a message to an existing ticket."""
    return controller.add_message(ticket_id)

@ticketing_bp.route('/<int:ticket_id>/resolve', methods=['PATCH'])
def resolve_ticket(ticket_id):
    """Mark a ticket as resolved."""
    return controller.resolve_ticket(ticket_id)

@ticketing_bp.route('/<int:ticket_id>/reopen', methods=['PATCH'])
def reopen_ticket(ticket_id):
    """Reopen a resolved ticket."""
    return controller.reopen_ticket(ticket_id)

@ticketing_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_tickets(user_id):
    """Get all tickets for a specific user."""
    return controller.get_user_tickets(user_id)

@ticketing_bp.route('/open', methods=['GET'])
def get_open_tickets():
    """Get all open (unresolved) tickets."""
    return controller.get_open_tickets()

@ticketing_bp.route('/resolved', methods=['GET'])
def get_resolved_tickets():
    """Get all resolved tickets."""
    return controller.get_resolved_tickets()