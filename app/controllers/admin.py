"""
Admin controller for WeRent Backend API.
Handles admin-specific operations like user promotion/demotion.
"""

from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from app.models import User
from app.extensions import db
from app.services import UserService
from app.schemas.user_schema import AdminPromotionSchema, UserResponseSchema
from app.utils import (
    success_response, error_response, validation_error_response,
    not_found_response, unauthorized_response, internal_error_response,
    forbidden_response
)


def _format_validation_errors(e: ValidationError):
    """Helper to format Pydantic validation errors for consistent API response."""
    field_errors = {}
    for error in e.errors():
        field_name = error['loc'][0] if error['loc'] else 'unknown'
        if field_name not in field_errors:
            field_errors[field_name] = []
        field_errors[field_name].append(error['msg'])
    return validation_error_response(field_errors)


def _check_admin_permission():
    """Check if current user has admin permission."""
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return False, unauthorized_response("Authentication required")
    
    user_service = UserService()
    current_user = user_service.get_by_id(current_user_id)
    
    if not current_user:
        return False, not_found_response("Current user not found")
    
    if not current_user.is_admin:
        return False, forbidden_response("Admin access required")
    
    return True, current_user


def promote_user_controller(data):
    """Handle user promotion/demotion to/from admin status."""
    try:
        if not data:
            return error_response("JSON payload required", 400)

        # Check admin permission
        has_permission, response_or_user = _check_admin_permission()
        if not has_permission:
            return response_or_user
        
        current_admin = response_or_user

        # Validate input data
        try:
            admin_data = AdminPromotionSchema(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        user_service = UserService()
        target_user = user_service.get_by_id(admin_data.user_id)
        
        if not target_user:
            return not_found_response("Target user not found")

        # Prevent self-demotion
        if admin_data.action == 'demote' and target_user.id == current_admin.id:
            return error_response("Cannot demote yourself from admin status", 400)

        # Store previous status
        previous_admin_status = target_user.is_admin

        # Perform the action
        if admin_data.action == 'promote':
            result = user_service.promote_to_admin(admin_data.user_id)
            if result['already_admin']:
                return success_response(
                    message=f"User {target_user.email} is already an admin",
                    data={
                        'user': UserResponseSchema.model_validate(result['user']).model_dump(),
                        'previous_status': previous_admin_status,
                        'new_status': result['user'].is_admin,
                        'action_performed': False
                    }
                )
            else:
                return success_response(
                    message=f"User {target_user.email} has been promoted to admin",
                    data={
                        'user': UserResponseSchema.model_validate(result['user']).model_dump(),
                        'previous_status': previous_admin_status,
                        'new_status': result['user'].is_admin,
                        'action_performed': True
                    },
                    status_code=200
                )
        
        elif admin_data.action == 'demote':
            result = user_service.demote_from_admin(admin_data.user_id)
            if result['already_non_admin']:
                return success_response(
                    message=f"User {target_user.email} is already a regular user",
                    data={
                        'user': UserResponseSchema.model_validate(result['user']).model_dump(),
                        'previous_status': previous_admin_status,
                        'new_status': result['user'].is_admin,
                        'action_performed': False
                    }
                )
            else:
                return success_response(
                    message=f"User {target_user.email} has been demoted from admin",
                    data={
                        'user': UserResponseSchema.model_validate(result['user']).model_dump(),
                        'previous_status': previous_admin_status,
                        'new_status': result['user'].is_admin,
                        'action_performed': True
                    },
                    status_code=200
                )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def get_all_admins_controller():
    """Get all admin users."""
    try:
        # Check admin permission
        has_permission, response_or_user = _check_admin_permission()
        if not has_permission:
            return response_or_user

        user_service = UserService()
        admins = user_service.get_all_admins()

        admin_list = []
        for admin in admins:
            admin_data = UserResponseSchema.model_validate(admin).model_dump()
            admin_list.append(admin_data)

        return success_response(
            message="Admin users retrieved successfully",
            data={
                'admins': admin_list,
                'total_count': len(admin_list)
            }
        )

    except Exception as e:
        return internal_error_response()


def get_admin_by_id_controller(admin_id):
    """Get admin user by ID."""
    try:
        # Check admin permission
        has_permission, response_or_user = _check_admin_permission()
        if not has_permission:
            return response_or_user

        user_service = UserService()
        admin = user_service.get_admin_by_id(admin_id)

        if not admin:
            return not_found_response("Admin user not found")

        return success_response(
            message="Admin user retrieved successfully",
            data={'admin': UserResponseSchema.model_validate(admin).model_dump()}
        )

    except Exception as e:
        return internal_error_response()
