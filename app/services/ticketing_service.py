"""
Ticketing service for WeRent Backend API.
Handles support tickets business logic.
"""

from datetime import datetime
from app.models.ticketing import Ticketing
from app.services.base_service import BaseService
from app.services.user_service import UserService
from app.services.booking_service import BookingService


class TicketingService(BaseService):
    """Service for handling ticketing operations."""

    def __init__(self):
        super().__init__(Ticketing)
        self.user_service = UserService()
        self.booking_service = BookingService()

    def create_ticket(self, user_id, initial_message, booking_id=None):
        """Create a new support ticket."""
        # Validate user exists
        user = self.user_service.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Validate booking if provided
        if booking_id:
            booking = self.booking_service.get_by_id(booking_id)
            if not booking:
                raise ValueError("Booking not found")

            # Validate that booking belongs to the user
            if booking.user_id != user_id:
                raise ValueError("Booking does not belong to this user")

        ticket = Ticketing()
        ticket.user_id = user_id
        ticket.booking_id = booking_id
        ticket.chat_content = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {initial_message}"
        ticket.is_resolved = False

        return self.save(ticket)

    def add_message(self, ticket_id, message):
        """Add a message to an existing ticket."""
        ticket = self.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        current_content = ticket.chat_content or ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = f"\n[{timestamp}] {message}"
        ticket.chat_content = current_content + new_message
        ticket.updated_at = datetime.now()

        return self.save(ticket)

    def resolve_ticket(self, ticket_id):
        """Mark a ticket as resolved."""
        ticket = self.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        ticket.is_resolved = True
        ticket.updated_at = datetime.now()

        return self.save(ticket)

    def reopen_ticket(self, ticket_id):
        """Reopen a resolved ticket."""
        ticket = self.get_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")

        ticket.is_resolved = False
        ticket.updated_at = datetime.now()

        return self.save(ticket)

    def get_user_tickets(self, user_id):
        """Get all tickets for a specific user."""
        return Ticketing.query.filter_by(user_id=user_id).all()

    def get_booking_tickets(self, booking_id):
        """Get all tickets related to a specific booking."""
        return Ticketing.query.filter_by(booking_id=booking_id).all()

    def get_open_tickets(self):
        """Get all open (unresolved) tickets."""
        return Ticketing.query.filter_by(is_resolved=False).all()

    def get_resolved_tickets(self):
        """Get all resolved tickets."""
        return Ticketing.query.filter_by(is_resolved=True).all()