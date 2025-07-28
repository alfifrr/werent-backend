from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from app.models import Payment, User, Booking
from app.extensions import db
from app.services.payment_service import PaymentService
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentOut
from app.utils import (
    success_response,
    error_response,
    validation_error_response,
    not_found_response,
    unauthorized_response,
    internal_error_response,
)
from typing import List, Optional


def _format_validation_errors(e: ValidationError):
    """Helper to format Pydantic validation errors for consistent API response."""
    field_errors = {}
    for error in e.errors():
        field_name = error["loc"][0] if error["loc"] else "unknown"
        if field_name not in field_errors:
            field_errors[field_name] = []
        field_errors[field_name].append(error["msg"])
    return validation_error_response(field_errors)


def create_payment_controller(data, current_user_id):
    """Handle payment creation with validation."""
    try:
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using PaymentCreate schema
        try:
            payment_data = PaymentCreate(**data)
        except ValidationError as e:
            return _format_validation_errors(e)
        # Create payment using service
        payment = PaymentService.create_payment(
            booking_id=payment_data.booking_id,
            total_price=payment_data.total_price,
            payment_method=payment_data.payment_method,
            payment_type=payment_data.payment_type,
            user_id=current_user_id
        )

        if not payment:
            return error_response("Payment creation failed. Check if user is verified and bookings exist and belong to user.", 400)

        return success_response(
            message="Payment created successfully",
            data=PaymentOut.model_validate(payment).model_dump(),
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def get_payment_controller(payment_id, current_user_id):
    """Handle getting a specific payment."""
    try:
        payment = PaymentService.get_payment(payment_id)
        if not payment:
            return not_found_response("Payment not found")

        # Check if user owns the payment or is admin
        if str(payment.user_id) != str(current_user_id):
            user = User.query.get(current_user_id)
            # if user not payment owner and not admin, deny access
            if not getattr(user, 'is_admin'):
                return unauthorized_response("Access denied")
        return success_response(
            message="Payment retrieved successfully",
            data=PaymentOut.model_validate(payment).model_dump()
        )

    except Exception as e:
        return internal_error_response()


def get_all_payments_controller(current_user_id):
    """Handle getting all payments (admin only)."""
    try:
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or not getattr(user, 'is_admin', False):
            return unauthorized_response("Admin access required")

        payments = PaymentService.get_all_payments()
        payment_data = [PaymentOut.from_orm(p).dict() for p in payments]

        return success_response(
            message="All payments retrieved successfully",
            data=payment_data
        )

    except Exception as e:
        return internal_error_response()


def update_payment_controller(payment_id, data, current_user_id):
    """Handle payment update."""
    try:
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using PaymentUpdate schema
        try:
            payment_data = PaymentUpdate(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        # Check if payment exists
        payment = PaymentService.get_payment(payment_id)
        if not payment:
            return not_found_response("Payment not found")

        # Check if user owns the payment or is admin
        if str(payment.user_id) != str(current_user_id):
            user = User.query.get(current_user_id)
            # if user not payment owner and not admin, deny access
            if not getattr(user, "is_admin"):
                return unauthorized_response("Access denied")

        # Update payment using service
        updated_payment = PaymentService.update_payment(payment_id, **payment_data.model_dump(exclude_unset=True))
        if not updated_payment:
            return error_response("Payment update failed", 400)

        return success_response(
            message="Payment updated successfully",
            data=PaymentOut.from_orm(updated_payment).dict()
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def delete_payment_controller(payment_id, current_user_id):
    """Handle payment deletion."""
    try:
        # Check if payment exists
        payment = PaymentService.get_payment(payment_id)
        if not payment:
            return not_found_response("Payment not found")

        # Check if user owns the payment or is admin
        if str(payment.user_id) != str(current_user_id):
            user = User.query.get(current_user_id)
            # if user not payment owner and not admin, deny access
            if not getattr(user, "is_admin"):
                return unauthorized_response("Access denied")

        # Delete payment using service
        success = PaymentService.delete_payment(payment_id)
        if not success:
            return error_response("Payment deletion failed", 400)

        return success_response(
            message="Payment deleted successfully"
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def get_payments_by_user_controller(user_id, current_user_id):
    """Handle getting payments by user ID."""
    try:
        # Check if current user is requesting their own payments or is admin
        if str(user_id) != str(current_user_id):
            user = User.query.get(current_user_id)
            if not getattr(user, 'is_admin'):
                return unauthorized_response("Access denied")

        payments = PaymentService.get_payments_by_user_id(user_id)
        payment_data = [PaymentOut.model_validate(p).model_dump() for p in payments]

        return success_response(
            message="User payments retrieved successfully",
            data=payment_data
        )

    except Exception as e:
        return internal_error_response() 