"""
Swagger-documented authentication routes for CamRent Backend API.
Enhanced authentication endpoints with comprehensive OpenAPI documentation.
"""

from flask import request
from flask_restx import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.models import User
from app.extensions import db
from app.utils import (
    validate_email, validate_password, validate_name, validate_phone,
    sanitize_string, success_response, error_response, validation_error_response,
    not_found_response, unauthorized_response, internal_error_response
)
from app.swagger import auth_ns
from app.swagger.models import create_swagger_models


def register_auth_routes(api):
    """Register authentication routes with Swagger documentation."""
    
    # Create Swagger models
    models = create_swagger_models(api)
    
    @auth_ns.route('/signup')
    class SignupResource(Resource):
        @auth_ns.doc(
            'user_signup',
            description='''
            Register a new user account with email and password.
            
            **Password Requirements:**
            - Minimum 8 characters
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one number
            
            **Email Requirements:**
            - Valid email format
            - Must be unique (not already registered)
            
            **Name Requirements:**
            - 1-50 characters
            - Letters, spaces, hyphens, and apostrophes only
            
            **Phone Requirements (Optional):**
            - Valid international phone number format
            - Can include country code
            ''',
            responses={
                201: ('User created successfully', models['auth_success_response']),
                400: ('Bad request - missing or invalid data', models['error_response']),
                409: ('Conflict - email already registered', models['error_response']),
                422: ('Validation error', models['validation_error_response']),
                500: ('Internal server error', models['error_response'])
            }
        )
        @auth_ns.expect(models['signup_request'], validate=True)
        def post(self):
            """Register a new user account."""
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
                
                # Create access token
                access_token = create_access_token(identity=str(user.id))
                
                return success_response(
                    message="User created successfully",
                    data={
                        'user': user.to_dict(),
                        'access_token': access_token
                    },
                    status_code=201
                )
                
            except Exception as e:
                db.session.rollback()
                return internal_error_response()

    @auth_ns.route('/login')
    class LoginResource(Resource):
        @auth_ns.doc(
            'user_login',
            description='''
            Authenticate user with email and password.
            
            Returns a JWT access token that expires in 24 hours.
            Use this token in the Authorization header for protected endpoints.
            
            **Usage:**
            ```
            Authorization: Bearer <access_token>
            ```
            
            **Account Status:**
            - Account must be active to login
            - Deactivated accounts will be rejected
            ''',
            responses={
                200: ('Login successful', models['auth_success_response']),
                400: ('Bad request - missing credentials', models['error_response']),
                401: ('Unauthorized - invalid credentials or inactive account', models['error_response']),
                500: ('Internal server error', models['error_response'])
            }
        )
        @auth_ns.expect(models['login_request'], validate=True)
        def post(self):
            """Authenticate user and return JWT token."""
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
                
                # Create access token
                access_token = create_access_token(identity=str(user.id))
                
                return success_response(
                    message="Login successful",
                    data={
                        'user': user.to_dict(),
                        'access_token': access_token
                    }
                )
                
            except Exception as e:
                return internal_error_response()

    @auth_ns.route('/profile')
    class ProfileResource(Resource):
        @auth_ns.doc(
            'get_user_profile',
            description='''
            Retrieve current user's profile information.
            
            **Authentication Required:**
            This endpoint requires a valid JWT token in the Authorization header.
            
            **Response includes:**
            - User ID and email
            - Personal information (name, phone)
            - Account timestamps (created, updated)
            - Account status
            ''',
            security='JWT',
            responses={
                200: ('Profile retrieved successfully', models['profile_response']),
                401: ('Unauthorized - invalid or missing token', models['error_response']),
                404: ('User not found', models['error_response']),
                500: ('Internal server error', models['error_response'])
            }
        )
        @jwt_required()
        def get(self):
            """Get current user's profile information."""
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

        @auth_ns.doc(
            'update_user_profile',
            description='''
            Update current user's profile information.
            
            **Authentication Required:**
            This endpoint requires a valid JWT token in the Authorization header.
            
            **Updatable Fields:**
            - first_name: User's first name (1-50 characters)
            - last_name: User's last name (1-50 characters)
            - phone: Phone number (optional, valid format)
            
            **Note:**
            - All fields are optional in the request
            - Only provided fields will be updated
            - Email cannot be updated via this endpoint
            - updated_at timestamp will be automatically set
            ''',
            security='JWT',
            responses={
                200: ('Profile updated successfully', models['profile_response']),
                400: ('Bad request - invalid data', models['error_response']),
                401: ('Unauthorized - invalid or missing token', models['error_response']),
                404: ('User not found', models['error_response']),
                422: ('Validation error', models['validation_error_response']),
                500: ('Internal server error', models['error_response'])
            }
        )
        @auth_ns.expect(models['profile_update_request'], validate=False)
        @jwt_required()
        def put(self):
            """Update current user's profile information."""
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

    @auth_ns.route('/logout')
    class LogoutResource(Resource):
        @auth_ns.doc(
            'user_logout',
            description='''
            Logout current user session.
            
            **Authentication Required:**
            This endpoint requires a valid JWT token in the Authorization header.
            
            **Note:**
            In the current implementation, this endpoint returns a success message.
            In a production environment, you would implement token blacklisting
            to invalidate the JWT token server-side.
            
            **Best Practice:**
            Client applications should remove the JWT token from storage
            (localStorage, sessionStorage, etc.) after calling this endpoint.
            ''',
            security='JWT',
            responses={
                200: ('Logout successful', models['logout_response']),
                401: ('Unauthorized - invalid or missing token', models['error_response']),
                500: ('Internal server error', models['error_response'])
            }
        )
        @jwt_required()
        def post(self):
            """Logout current user session."""
            try:
                # In the future, implement token blacklisting here
                return success_response("Logout successful")
                
            except Exception as e:
                return internal_error_response()

    return auth_ns
