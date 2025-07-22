from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from pydantic import ValidationError
from app.models import User
from app.extensions import db
from app.services import UserService
from app.schemas import (
    UserCreateSchema, LoginSchema, UserUpdateSchema,
    UserResponseSchema
)
from app.utils import (
    success_response, error_response, validation_error_response,
    not_found_response, unauthorized_response, internal_error_response
)

def signup_controller(data):
    try:
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
            first_name=user_data.first_name,
            last_name=user_data.last_name,
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

def login_controller(data):
    try:
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

def get_profile_controller(current_user_id):
    try:
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

def update_profile_controller(current_user_id, data):
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
            field_errors = {}
            for error in e.errors():
                field_name = error['loc'][0] if error['loc'] else 'unknown'
                if field_name not in field_errors:
                    field_errors[field_name] = []
                field_errors[field_name].append(error['msg'])
            return validation_error_response(field_errors)

        # Update user using service
        updated_user = user_service.update_profile(
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

def refresh_controller(current_user_id):
    try:
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
