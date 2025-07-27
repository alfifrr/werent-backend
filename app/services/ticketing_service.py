"""
Ticketing service for WeRent Backend API.
Handles all support ticket business logic with clean, readable code.
"""

from datetime import datetime, UTC
from app.models.ticketing import Ticketing
from app.services.base_service import BaseService
from app.services.user_service import UserService
from app.services.booking_service import BookingService


class TicketingService(BaseService):
    """
    Service for handling all ticketing operations.

    This service manages the business logic for support tickets,
    keeping the controller thin and focused on HTTP concerns.
    """

    def __init__(self):
        """Initialize the service with required dependencies."""
        super().__init__(Ticketing)
        self.user_service = UserService()
        self.booking_service = BookingService()

    def _validate_user_exists(self, user_id):
        """
        Helper method to validate that a user exists.

        Args:
            user_id: ID of the user to validate

        Raises:
            ValueError: If user doesn't exist

        Returns:
            User object if found
        """
        user = self.user_service.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user

    def _validate_booking_exists_and_belongs_to_user(self, booking_id, user_id):
        """
        Helper method to validate booking exists and belongs to the user.

        Args:
            booking_id: ID of the booking to validate
            user_id: ID of the user who should own the booking

        Raises:
            ValueError: If booking doesn't exist or doesn't belong to user

        Returns:
            Booking object if valid
        """
        booking = self.booking_service.get_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found")

        if booking.user_id != user_id:
            raise ValueError("Booking does not belong to this user")

        return booking

    def _format_chat_message(self, message):
        """
        Helper method to format a chat message with timestamp.

        Args:
            message: The message content

        Returns:
            Formatted message string with timestamp
        """
        timestamp = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')
        return f"[{timestamp}] {message}"

    def create_ticket(self, user_id, initial_message, booking_id=None):
        """
        Create a new support ticket.

        Args:
            user_id: ID of the user creating the ticket
            initial_message: The initial message/description of the issue
            booking_id: Optional ID of related booking

        Returns:
            Created ticket object

        Raises:
            ValueError: If validation fails
        """
        # Step 1: Validate that user exists
        self._validate_user_exists(user_id)

        # Step 2: If booking is provided, validate it exists and belongs to user
        if booking_id:
            self._validate_booking_exists_and_belongs_to_user(booking_id, user_id)

        # Step 3: Create the ticket with formatted initial message
        ticket = Ticketing()
        ticket.user_id = user_id
        ticket.booking_id = booking_id
        ticket.chat_content = self._format_chat_message(initial_message)
        ticket.is_resolved = False

        # Step 4: Save and return the ticket
        return self.save(ticket)

    def add_message(self, ticket_id, message):
        """
        Add a new message to an existing ticket.

        Args:
            ticket_id: ID of the ticket to add message to
            message: The message content to add

        Returns:
            Updated ticket object

        Raises:
            ValueError: If ticket not found
        """
        # Step 1: Get the ticket
        ticket = self.get_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket with ID {ticket_id} not found")

        # Step 2: Append the new message to existing chat content
        current_content = ticket.chat_content or ""
        new_message = self._format_chat_message(message)
        ticket.chat_content = current_content + "\n" + new_message
        ticket.updated_at = datetime.now(UTC)

        # Step 3: Save and return updated ticket
        return self.save(ticket)

    def resolve_ticket(self, ticket_id):
        """
        Mark a ticket as resolved.

        Args:
            ticket_id: ID of the ticket to resolve

        Returns:
            Updated ticket object

        Raises:
            ValueError: If ticket not found or already resolved
        """
        # Step 1: Get the ticket
        ticket = self.get_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket with ID {ticket_id} not found")

        # Step 2: Check if already resolved
        if ticket.is_resolved:
            raise ValueError("Ticket is already resolved")

        # Step 3: Mark as resolved and update timestamp
        ticket.is_resolved = True
        ticket.updated_at = datetime.now(UTC)

        # Step 4: Save and return updated ticket
        return self.save(ticket)

    def reopen_ticket(self, ticket_id):
        """
        Reopen a resolved ticket.

        Args:
            ticket_id: ID of the ticket to reopen

        Returns:
            Updated ticket object

        Raises:
            ValueError: If ticket not found or already open
        """
        # Step 1: Get the ticket
        ticket = self.get_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket with ID {ticket_id} not found")

        # Step 2: Check if already open
        if not ticket.is_resolved:
            raise ValueError("Ticket is already open")

        # Step 3: Mark as open and update timestamp
        ticket.is_resolved = False
        ticket.updated_at = datetime.now(UTC)

        # Step 4: Save and return updated ticket
        return self.save(ticket)

    def get_user_tickets(self, user_id):
        """
        Get all tickets for a specific user.

        Args:
            user_id: ID of the user whose tickets to retrieve

        Returns:
            List of ticket objects

        Raises:
            ValueError: If user not found
        """
        # Step 1: Validate user exists
        self._validate_user_exists(user_id)

        # Step 2: Get tickets ordered by creation date (newest first)
        return Ticketing.query.filter_by(user_id=user_id).order_by(Ticketing.created_at.desc()).all()

    def get_booking_tickets(self, booking_id):
        """
        Get all tickets related to a specific booking.

        Args:
            booking_id: ID of the booking

        Returns:
            List of ticket objects

        Raises:
            ValueError: If booking not found
        """
        # Step 1: Validate booking exists
        booking = self.booking_service.get_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found")

        # Step 2: Get tickets for this booking
        return Ticketing.query.filter_by(booking_id=booking_id).order_by(Ticketing.created_at.desc()).all()

    def get_open_tickets(self):
        """
        Get all open (unresolved) tickets.

        Returns:
            List of open ticket objects ordered by creation date
        """
        return Ticketing.query.filter_by(is_resolved=False).order_by(Ticketing.created_at.desc()).all()

    def get_resolved_tickets(self):
        """
        Get all resolved tickets.

        Returns:
            List of resolved ticket objects ordered by update date
        """
        return Ticketing.query.filter_by(is_resolved=True).order_by(Ticketing.updated_at.desc()).all()

    def get_ticket_stats(self):
        """
        Get ticket statistics for dashboard/reporting.

        Returns:
            Dictionary with ticket counts
        """
        total_tickets = Ticketing.query.count()
        open_tickets = Ticketing.query.filter_by(is_resolved=False).count()
        resolved_tickets = Ticketing.query.filter_by(is_resolved=True).count()

        return {
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'resolved_tickets': resolved_tickets
        }