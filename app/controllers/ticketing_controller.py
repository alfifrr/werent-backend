"""
Controller for ticketing endpoints.
Clean, readable controller following DRY principles with proper validation.
"""

from flask import request, jsonify
from pydantic import ValidationError
from app.services.ticketing_service import TicketingService
from app.utils.responses import error_response
from app.schemas.ticketing_schema import (
    CreateTicketRequest,
    AddMessageRequest,
    TicketResponse,
    TicketListResponse
)


class TicketingController:
    """
    Controller for handling ticketing endpoints.

    Handles all ticket-related operations including creation, messaging,
    resolution, and retrieval with proper validation and error handling.
    """

    def __init__(self):
        self.ticketing_service = TicketingService()

    def _validate_request_data(self, schema_class, data=None):
        """
        Helper method to validate request data using Pydantic schemas.

        Args:
            schema_class: Pydantic schema class to validate against
            data: Request data (if None, gets from request.get_json())

        Returns:
            Validated data object

        Raises:
            ValueError: If validation fails
        """
        if data is None:
            data = request.get_json()

        if not data:
            raise ValueError("Request body is required")

        try:
            return schema_class(**data)
        except ValidationError as e:
            # Convert Pydantic validation errors to readable format
            error_messages = []
            for error in e.errors():
                field = ".".join(str(loc) for loc in error['loc']) if error['loc'] else 'unknown'
                message = error['msg']
                error_messages.append(f"{field}: {message}")
            raise ValueError(f"Validation error: {'; '.join(error_messages)}")
        except Exception as e:
            raise ValueError(f"Invalid request data: {str(e)}")

    def _serialize_ticket(self, ticket):
        """
        Helper method to serialize ticket object to response format.

        Args:
            ticket: Ticket model instance

        Returns:
            Serialized ticket data
        """
        return TicketResponse.model_validate(ticket).model_dump()

    def create_ticket(self):
        """
        Create a new support ticket.

        Expected JSON payload:
        {
            "user_id": int,
            "message": str,
            "booking_id": int (optional)
        }

        Returns:
            201: Ticket created successfully
            400: Validation error or bad request
            500: Internal server error
        """
        try:
            # Validate request data using Pydantic schema
            validated_data = self._validate_request_data(CreateTicketRequest)

            # Create ticket through service layer
            ticket = self.ticketing_service.create_ticket(
                user_id=validated_data.user_id,
                initial_message=validated_data.message,
                booking_id=validated_data.booking_id
            )

            # Return serialized response
            return jsonify(self._serialize_ticket(ticket)), 201

        except ValueError as e:
            return error_response(str(e)), 400
        except Exception as e:
            return error_response(f"Failed to create ticket: {str(e)}"), 500

    def get_ticket(self, ticket_id):
        """
        Get a specific ticket by ID.

        Args:
            ticket_id: ID of the ticket to retrieve

        Returns:
            200: Ticket found and returned
            400: Invalid ticket ID
            404: Ticket not found
            500: Internal server error
        """
        try:
            # Validate ticket_id parameter
            if not isinstance(ticket_id, int) or ticket_id <= 0:
                return error_response("Invalid ticket ID: must be a positive integer"), 400

            # Get ticket through service layer
            ticket = self.ticketing_service.get_by_id(ticket_id)
            if not ticket:
                return error_response("Ticket not found"), 404

            # Return serialized response
            return jsonify(self._serialize_ticket(ticket)), 200

        except Exception as e:
            return error_response(f"Failed to retrieve ticket: {str(e)}"), 500

    def add_message(self, ticket_id):
        """
        Add a message to an existing ticket.

        Args:
            ticket_id: ID of the ticket to add message to

        Expected JSON payload:
        {
            "message": str
        }

        Returns:
            200: Message added successfully
            400: Validation error or invalid ticket ID
            404: Ticket not found
            500: Internal server error
        """
        try:
            # Validate ticket_id parameter
            if not isinstance(ticket_id, int) or ticket_id <= 0:
                return error_response("Invalid ticket ID: must be a positive integer"), 400

            # Validate request data using Pydantic schema
            validated_data = self._validate_request_data(AddMessageRequest)

            # Add message through service layer
            ticket = self.ticketing_service.add_message(
                ticket_id=ticket_id,
                message=validated_data.message
            )

            # Return serialized response
            return jsonify(self._serialize_ticket(ticket)), 200

        except ValueError as e:
            return error_response(str(e)), 400
        except Exception as e:
            return error_response(f"Failed to add message: {str(e)}"), 500

    def resolve_ticket(self, ticket_id):
        """
        Mark a ticket as resolved.

        Args:
            ticket_id: ID of the ticket to resolve

        Returns:
            200: Ticket resolved successfully
            400: Invalid ticket ID
            404: Ticket not found
            500: Internal server error
        """
        try:
            # Validate ticket_id parameter
            if not isinstance(ticket_id, int) or ticket_id <= 0:
                return error_response("Invalid ticket ID: must be a positive integer"), 400

            # Resolve ticket through service layer
            ticket = self.ticketing_service.resolve_ticket(ticket_id)

            # Return serialized response
            return jsonify(self._serialize_ticket(ticket)), 200

        except ValueError as e:
            return error_response(str(e)), 400
        except Exception as e:
            return error_response(f"Failed to resolve ticket: {str(e)}"), 500

    def reopen_ticket(self, ticket_id):
        """
        Reopen a resolved ticket.

        Args:
            ticket_id: ID of the ticket to reopen

        Returns:
            200: Ticket reopened successfully
            400: Invalid ticket ID
            404: Ticket not found
            500: Internal server error
        """
        try:
            # Validate ticket_id parameter
            if not isinstance(ticket_id, int) or ticket_id <= 0:
                return error_response("Invalid ticket ID: must be a positive integer"), 400

            # Reopen ticket through service layer
            ticket = self.ticketing_service.reopen_ticket(ticket_id)

            # Return serialized response
            return jsonify(self._serialize_ticket(ticket)), 200

        except ValueError as e:
            return error_response(str(e)), 400
        except Exception as e:
            return error_response(f"Failed to reopen ticket: {str(e)}"), 500

    def get_user_tickets(self, user_id):
        """
        Get all tickets for a specific user.

        Args:
            user_id: ID of the user whose tickets to retrieve

        Returns:
            200: Tickets retrieved successfully
            400: Invalid user ID
            500: Internal server error
        """
        try:
            # Validate user_id parameter
            if not isinstance(user_id, int) or user_id <= 0:
                return error_response("Invalid user ID: must be a positive integer"), 400

            # Get tickets through service layer
            tickets = self.ticketing_service.get_user_tickets(user_id)

            # Serialize response using Pydantic schema
            serialized_tickets = [self._serialize_ticket(ticket) for ticket in tickets]
            response_data = TicketListResponse(
                tickets=serialized_tickets,
                total_count=len(tickets)
            ).model_dump()

            return jsonify(response_data), 200

        except Exception as e:
            return error_response(f"Failed to retrieve tickets: {str(e)}"), 500

    def get_open_tickets(self):
        """
        Get all open (unresolved) tickets.

        Returns:
            200: Open tickets retrieved successfully
            500: Internal server error
        """
        try:
            # Get open tickets through service layer
            tickets = self.ticketing_service.get_open_tickets()

            # Serialize response using Pydantic schema
            serialized_tickets = [self._serialize_ticket(ticket) for ticket in tickets]
            response_data = TicketListResponse(
                tickets=serialized_tickets,
                total_count=len(tickets)
            ).model_dump()

            return jsonify(response_data), 200

        except Exception as e:
            return error_response(f"Failed to retrieve open tickets: {str(e)}"), 500

    def get_resolved_tickets(self):
        """
        Get all resolved tickets.

        Returns:
            200: Resolved tickets retrieved successfully
            500: Internal server error
        """
        try:
            # Get resolved tickets through service layer
            tickets = self.ticketing_service.get_resolved_tickets()

            # Serialize response using Pydantic schema
            serialized_tickets = [self._serialize_ticket(ticket) for ticket in tickets]
            response_data = TicketListResponse(
                tickets=serialized_tickets,
                total_count=len(tickets)
            ).model_dump()

            return jsonify(response_data), 200

        except Exception as e:
            return error_response(f"Failed to retrieve resolved tickets: {str(e)}"), 500