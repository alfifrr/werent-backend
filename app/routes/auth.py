"""
Authentication routes for CamRent Backend API.
Handles user registration, login, profile management, and token refresh.
"""

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from app.models import User
from app.extensions import db
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
    
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "SecurePass123",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890"  // optional
    }
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("JSON payload required", 400)
        
        # Extract and sanitize input data
        email = sanitize_string(data.get('email', ''))
        password = data.get('password', '')
        first_name = sanitize_string(data.get('first_name', ''))
        last_name = sanitize_string(data.get('last_name', ''))
        phone = sanitize_string(data.get('phone', '')) if data.get('phone') else None
        
        # Validation
        field_errors = {}
        
        # Validate required fields
        if not email:
            field_errors['email'] = 'Email is required'
        elif not validate_email(email):
            field_errors['email'] = 'Invalid email format'
        
        if not password:
            field_errors['password'] = 'Password is required'
        else:
            is_valid_password, password_error = validate_password(password)
            if not is_valid_password:
                field_errors['password'] = password_error
        
        is_valid_first_name, first_name_error = validate_name(first_name, "First name")
        if not is_valid_first_name:
            field_errors['first_name'] = first_name_error
            
        is_valid_last_name, last_name_error = validate_name(last_name, "Last name")
        if not is_valid_last_name:
            field_errors['last_name'] = last_name_error
        
        if phone and not validate_phone(phone):
            field_errors['phone'] = 'Invalid phone number format'
        
        if field_errors:
            return validation_error_response(field_errors)
        
        # Check if user already exists
        email = email.lower()
        if User.find_by_email(email):
            return error_response("Email already registered", 409)
        
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.set_password(password)
        user.save()
        
        return success_response(
            message="User created successfully",
            data={'user': user.to_dict()},
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response()


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User authentication endpoint.
    
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "SecurePass123"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("JSON payload required", 400)
        
        email = sanitize_string(data.get('email', ''))
        password = data.get('password', '')
        
        # Validate input
        if not email or not password:
            return error_response("Email and password are required", 400)
        
        if not validate_email(email):
            return error_response("Invalid email format", 400)
        
        # Find user
        user = User.find_by_email(email)
        
        if not user or not user.check_password(password):
            return unauthorized_response("Invalid email or password")
        
        if not user.is_active:
            return unauthorized_response("Account is deactivated")
        
        # Create access and refresh tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return success_response(
            message="Login successful",
            data={
                'user': user.to_dict(),
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
        user = User.find_by_id(current_user_id)
        
        if not user:
            return not_found_response("User")
        
        return success_response(
            message="Profile retrieved successfully",
            data={'user': user.to_dict()}
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
    
    Expected JSON payload (all fields optional):
    {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890"
    }
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = User.find_by_id(current_user_id)
        
        if not user:
            return not_found_response("User")
        
        data = request.get_json()
        if not data:
            return error_response("JSON payload required", 400)
        
        # Validation
        field_errors = {}
        
        # Update first name if provided
        if 'first_name' in data:
            first_name = sanitize_string(data['first_name'])
            is_valid, error_msg = validate_name(first_name, "First name")
            if not is_valid:
                field_errors['first_name'] = error_msg
            else:
                user.first_name = first_name
        
        # Update last name if provided
        if 'last_name' in data:
            last_name = sanitize_string(data['last_name'])
            is_valid, error_msg = validate_name(last_name, "Last name")
            if not is_valid:
                field_errors['last_name'] = error_msg
            else:
                user.last_name = last_name
        
        # Update phone if provided
        if 'phone' in data:
            phone = sanitize_string(data['phone']) if data['phone'] else None
            if phone and not validate_phone(phone):
                field_errors['phone'] = 'Invalid phone number format'
            else:
                user.phone = phone
        
        if field_errors:
            return validation_error_response(field_errors)
        
        user.save()
        
        return success_response(
            message="Profile updated successfully",
            data={'user': user.to_dict()}
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
        user = User.find_by_id(current_user_id)
        
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
