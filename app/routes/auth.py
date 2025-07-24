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
from app.controllers.auth import signup_controller, login_controller, get_profile_controller, update_profile_controller, refresh_controller, verify_email_controller, resend_verification_controller

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User registration endpoint.
    """
    data = request.get_json()
    return signup_controller(data)



@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User authentication endpoint.
    """
    data = request.get_json()
    return login_controller(data)



@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user's profile information.
    """
    current_user_id = int(get_jwt_identity())
    return get_profile_controller(current_user_id)



@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update current user's profile information.
    """
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    return update_profile_controller(current_user_id, data)



@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token endpoint.
    """
    current_user_id = int(get_jwt_identity())
    return refresh_controller(current_user_id)


@auth_bp.route('/verify-email/<uuid>', methods=['GET'])
def verify_email(uuid):
    """
    Email verification endpoint using UUID.
    Users click the verification link in their email to verify their account.
    """
    return verify_email_controller(uuid)


@auth_bp.route('/resend-verification', methods=['POST'])
@jwt_required()
def resend_verification():
    """
    Resend verification email endpoint.
    Allows authenticated users to request a new verification email for their own account.
    """
    return resend_verification_controller()

