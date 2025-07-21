"""
Authentication routes for WeRent Backend API.
Handles user registration, login, profile management, and token refresh.
Updated to use Pydantic schemas with @field_validator.
"""

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.models import User
from app.extensions import db
from app.services import UserService
from app.schemas import (
    UserCreateSchema, LoginSchema, UserUpdateSchema,
    UserResponseSchema, LoginResponseSchema, TokenResponseSchema,
    ValidationErrorSchema, NotFoundErrorSchema, UnauthorizedErrorSchema
)
from app.utils import (
    validate_email, validate_password, validate_name, validate_phone,
    sanitize_string, success_response, error_response, validation_error_response,
    not_found_response, unauthorized_response, internal_error_response
)

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User registration endpoint.

    Expected JSON payload validated by UserCreateSchema:
    {
        "email": "user@example.com",
        "password": "SecurePass123",
        "name": "John Doe",
        "phone": "+1234567890"  // optional
    }
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using Pydantic schema
        try:
            user_data = UserCreateSchema(**data)
        except ValidationError as e:
            field_errors = {}
            for error in e.errors():
                field_name = error['loc'][0] if error['loc'] else 'unknown'
                if field_name not in field_errors:
                    field_errors[field_name] = []
                field_errors[field_name].append(error['msg'])
            return validation_error_response(field_errors)

        # Check if user already exists
        user_service = UserService()
        if user_service.find_by_email(user_data.email):
            return error_response("Email already registered", 409)

        # Create new user using service
        user = user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name,
            phone=user_data.phone
        )

        return success_response(
            message="User created successfully",
            data={'user': UserResponseSchema.model_validate(user).model_dump()},
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User authentication endpoint.

    Expected JSON payload validated by LoginSchema:
    {
        "email": "user@example.com",
        "password": "SecurePass123"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using Pydantic schema
        try:
            login_data = LoginSchema(**data)
        except ValidationError as e:
            field_errors = {}
            for error in e.errors():
                field_name = error['loc'][0] if error['loc'] else 'unknown'
                if field_name not in field_errors:
                    field_errors[field_name] = []
                field_errors[field_name].append(error['msg'])
            return validation_error_response(field_errors)

        # Find user using service
        user_service = UserService()
        user = user_service.authenticate_user(login_data.email, login_data.password)

        if not user:
            return unauthorized_response("Invalid email or password")

        if not user.is_active:
            return unauthorized_response("Account is deactivated")

        # Create access and refresh tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return success_response(
            message="Login successful",
            data={
                'user': UserResponseSchema.model_validate(user).model_dump(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        )

    except Exception as e:
        return internal_error_response()


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user's profile information.
    Requires valid JWT token in Authorization header.
    """
    try:
        current_user_id = int(get_jwt_identity())
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)

        if not user:
            return not_found_response("User")

        return success_response(
            message="Profile retrieved successfully",
            data={'user': UserResponseSchema.model_validate(user).model_dump()}
        )

    except ValueError:
        return error_response("Invalid user ID in token", 400)
    except Exception as e:
        return internal_error_response()


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update current user's profile information.
    Requires valid JWT token in Authorization header.

    Expected JSON payload validated by UserUpdateSchema (all fields optional):
    {
        "name": "John Doe",
        "phone": "+1234567890"
    }
    """
    try:
        current_user_id = int(get_jwt_identity())
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)

        if not user:
            return not_found_response("User")

        data = request.get_json()
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using Pydantic schema
        try:
            update_data = UserUpdateSchema(**data)
        except ValidationError as e:
            field_errors = {}
            for error in e.errors():
                field_name = error['loc'][0] if error['loc'] else 'unknown'
                if field_name not in field_errors:
                    field_errors[field_name] = []
                field_errors[field_name].append(error['msg'])
            return validation_error_response(field_errors)

        # Update user using service
        updated_user = user_service.update_user(
            user_id=current_user_id,
            **update_data.model_dump(exclude_unset=True)
        )

        return success_response(
            message="Profile updated successfully",
            data={'user': UserResponseSchema.model_validate(updated_user).model_dump()}
        )

    except ValueError:
        return error_response("Invalid user ID in token", 400)
    except Exception as e:
        db.session.rollback()
        return internal_error_response()


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token endpoint.
    Requires valid refresh token in Authorization header.

    Returns a new access token while keeping the same refresh token.
    """
    try:
        current_user_id = int(get_jwt_identity())
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)

        if not user:
            return not_found_response("User")

        if not user.is_active:
            return unauthorized_response("Account is deactivated")

        # Create new access token
        access_token = create_access_token(identity=str(user.id))

        return success_response(
            message="Access token refreshed successfully",
            data={'access_token': access_token}
        )

    except ValueError:
        return error_response("Invalid user ID in token", 400)
    except Exception as e:
        return internal_error_response()
