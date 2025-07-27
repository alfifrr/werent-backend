from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from pydantic import ValidationError
from app.models import User
from app.extensions import db
from app.services import UserService
from app.services.email_service import EmailService
from app.schemas.user_schema import UserUpdateSchema, UserResponseSchema
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.utils import (
    success_response,
    error_response,
    validation_error_response,
    not_found_response,
    unauthorized_response,
    internal_error_response,
)


def _format_validation_errors(e: ValidationError):
    """Helper to format Pydantic validation errors for consistent API response."""
    field_errors = {}
    for error in e.errors():
        field_name = error["loc"][0] if error["loc"] else "unknown"
        if field_name not in field_errors:
            field_errors[field_name] = []
        field_errors[field_name].append(error["msg"])
    return validation_error_response(field_errors)


def signup_controller(data):
    """Handle user registration with validation using RegisterSchema."""
    try:
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using RegisterSchema (from auth_schema)
        try:
            user_data = RegisterSchema(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        # Check if user already exists
        user_service = UserService()
        if user_service.find_by_email(user_data.email):
            return error_response("Email already registered", 409)
        
        # Create new user using service
        user = user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone_number,
        )

        # Send verification email
        email_service = EmailService()
        email_sent = email_service.send_verification_email(
            user_email=user.email,
            user_name=user.full_name,
            verification_uuid=user.uuid
        )

        response_message = "User created successfully. Please check your email to verify your account."
        if not email_sent:
            response_message += " (Note: Verification email could not be sent)"

        return success_response(
            message=response_message,
            data={
                'user': UserResponseSchema.model_validate(user).model_dump(),
                'verification_email_sent': email_sent
            },
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        # Optionally log the exception here
        return internal_error_response()


def login_controller(data):
    """Handle user login with validation using LoginSchema."""
    try:
        if not data:
            return error_response("JSON payload required", 400)

        # Validate using LoginSchema (from auth_schema)
        try:
            login_data = LoginSchema(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        # Find user using service
        user_service = UserService()
        user = user_service.authenticate_user(login_data.email, login_data.password)

        if not user:
            return unauthorized_response("Invalid email or password")

        if not user.is_active:
            return unauthorized_response("Account is deactivated")

        # Optional: Check if email is verified (uncomment to require email verification for login)
        # if not user.is_verified:
        #     return error_response(
        #         "Please verify your email address before logging in. Check your inbox for a verification link.",
        #         403
        #     )

        # Create access and refresh tokens with string identity for Flask-JWT-Extended compatibility
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return success_response(
            message="Login successful",
            data={
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        )

    except Exception as e:
        # Optionally log the exception here
        return internal_error_response()


def get_profile_controller(current_user_id):
    try:
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)

        if not user:
            return not_found_response("User")

        return success_response(
            message="Profile retrieved successfully",
            data={"user": UserResponseSchema.model_validate(user).model_dump()},
        )

    except ValueError:
        return error_response("Invalid user ID in token", 400)
    except Exception as e:
        return internal_error_response()


def update_profile_controller(current_user_id, data):
    """Handle profile update with validation using UserUpdateSchema."""
    try:
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)

        if not user:
            return not_found_response("User")

        if not data:
            return error_response("JSON payload required", 400)

        # Validate using Pydantic schema
        try:
            update_data = UserUpdateSchema(**data)
        except ValidationError as e:
            return _format_validation_errors(e)

        # Update user using service
        # Convert update_data to dict and ensure phone_number is used
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_user = user_service.update_profile(
            user_id=current_user_id, **update_dict
        )

        return success_response(
            message="Profile updated successfully",
            data={"user": UserResponseSchema.model_validate(updated_user).model_dump()},
        )

    except ValueError:
        return error_response("Invalid user ID in token", 400)
    except Exception as e:
        db.session.rollback()
        # Optionally log the exception here
        return internal_error_response()


def refresh_controller(current_user_id):
    try:
        user_service = UserService()
        user = user_service.get_by_id(current_user_id)

        if not user:
            return not_found_response("User")

        if not user.is_active:
            return unauthorized_response("Account is deactivated")

        # Create new access token
        # Create new access token with string identity for Flask-JWT-Extended compatibility
        access_token = create_access_token(identity=str(user.id))

        return success_response(
            message="Access token refreshed successfully",
            data={"access_token": access_token},
        )

    except ValueError:
        return error_response("Invalid user ID in token", 400)
    except Exception as e:
        return internal_error_response()


def verify_email_controller(uuid):
    """Handle email verification using UUID."""
    try:
        if not uuid:
            return error_response("Verification UUID required", 400)

        # Find user by UUID
        user_service = UserService()
        user = user_service.find_by_uuid(uuid)

        if not user:
            return error_response("Invalid or expired verification link", 404)

        if user.is_verified:
            return success_response(
                message="Email already verified",
                data={'verified': True}
            )

        # Update user verification status
        user.is_verified = True
        db.session.commit()

        # Send welcome email
        email_service = EmailService()
        email_service.send_welcome_email(
            user_email=user.email,
            user_name=user.full_name
        )

        return success_response(
            message="Email verified successfully! Welcome to WeRent.",
            data={'verified': True}
        )

    except Exception as e:
        db.session.rollback()
        return internal_error_response()


def resend_verification_controller():
    """Handle resending verification email for the current logged-in user."""
    try:
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return error_response("Authentication required", 401)
        
        # Convert to integer if it's a string
        try:
            user_id = int(current_user_id)
        except (ValueError, TypeError):
            return error_response("Invalid user ID in token", 400)
        
        # Find user by ID from token
        user_service = UserService()
        user = user_service.get_by_id(user_id)

        if not user:
            return error_response("User not found", 404)

        if user.is_verified:
            return error_response("Email already verified", 400)

        if not user.is_active:
            return error_response("Account is deactivated", 403)

        # Send verification email
        email_service = EmailService()
        email_sent = email_service.send_verification_email(
            user_email=user.email,
            user_name=user.full_name,
            verification_uuid=user.uuid
        )
        if email_sent:
            return success_response(
                message="Verification email sent successfully. Please check your inbox.",
                data={'email_sent': True}
            )
        else:
            return error_response("Failed to send verification email. Please try again later.", 500)

    except Exception as e:
        return internal_error_response()
