# Pydantic v2 Schemas Documentation - WeRent Backend

## Overview

Schemas telah diupdate menggunakan Pydantic v2 dengan `@field_validator` untuk validasi input/output data di API. Semua schemas menyediakan automatic validation, serialization, dan documentation untuk endpoints.

## Key Updates

### File Naming Convention

Semua schema files sekarang menggunakan suffix `_schema`:

- `base_schema.py` - Base schemas dan mixins
- `user_schema.py` - User-related schemas
- `auth_schema.py` - Authentication schemas
- `item_schema.py` - Item management schemas
- `booking_schema.py` - Booking process schemas
- `message_schema.py` - Messaging system schemas
- `review_schema.py` - Review and rating schemas
- `image_schema.py` - Image upload/management schemas
- `error_schema.py` - Error handling schemas

### Pydantic v2 Changes

#### 1. Validator Decorator Update

```python
# OLD (Pydantic v1)
@validator('password')
def validate_password(cls, v):
    return v

# NEW (Pydantic v2)
@field_validator('password')
@classmethod
def validate_password(cls, v):
    return v
```

#### 2. Cross-field Validation Update

```python
# OLD (Pydantic v1)
@validator('confirm_password')
def passwords_match(cls, v, values):
    if 'password' in values and v != values['password']:
        raise ValueError('Passwords do not match')
    return v

# NEW (Pydantic v2)
@field_validator('confirm_password')
@classmethod
def passwords_match(cls, v, values):
    if 'password' in values.data and v != values.data['password']:
        raise ValueError('Passwords do not match')
    return v
```

#### 3. Model Validation Methods

```python
# OLD (Pydantic v1)
user_response = UserResponseSchema.from_orm(user_model)
user_dict = user_response.dict()

# NEW (Pydantic v2)
user_response = UserResponseSchema.model_validate(user_model)
user_dict = user_response.model_dump()
```

## Updated Route Example

### Authentication Route with Pydantic v2

```python
from flask import Blueprint, request
from pydantic import ValidationError
from app.schemas import UserCreateSchema, UserResponseSchema

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Pydantic v2 validation
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

        # Create user using service layer
        user_service = UserService()
        user = user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name,
            phone=user_data.phone
        )

        # Return response using model_validate and model_dump
        return success_response(
            message="User created successfully",
            data={'user': UserResponseSchema.model_validate(user).model_dump()},
            status_code=201
        )

    except Exception as e:
        return internal_error_response()
```

## Schema Examples

### User Schema with Updated Validators

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.base_schema import BaseSchema

class UserCreateSchema(BaseSchema):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            cleaned = ''.join(filter(str.isdigit, v))
            if len(cleaned) < 10 or len(cleaned) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
        return v
```

### Booking Schema with Date Validation

```python
@field_validator('start_date')
@classmethod
def validate_start_date(cls, v):
    if v < date.today():
        raise ValueError('Start date cannot be in the past')
    return v

@field_validator('end_date')
@classmethod
def validate_end_date(cls, v, values):
    if 'start_date' in values.data and v <= values.data['start_date']:
        raise ValueError('End date must be after start date')
    return v
```

## Benefits of Pydantic v2

1. **Performance**: Significantly faster than v1
2. **Better Type Safety**: Enhanced type inference
3. **Improved Error Messages**: More detailed validation errors
4. **Modern Syntax**: Cleaner decorator approach with `@field_validator`
5. **Better IDE Support**: Enhanced auto-completion and type hints

## Import Structure

```python
# Updated __init__.py with _schema suffix imports
from .base_schema import BaseSchema, ResponseSchema
from .user_schema import UserCreateSchema, UserResponseSchema
from .auth_schema import LoginSchema, RegisterSchema
from .item_schema import ItemCreateSchema, ItemResponseSchema
from .booking_schema import BookingCreateSchema, BookingResponseSchema
# ... etc
```

## Error Handling

### Enhanced Validation Error Processing

```python
def handle_validation_error(e: ValidationError):
    field_errors = {}
    for error in e.errors():
        field_name = error['loc'][0] if error['loc'] else 'unknown'
        if field_name not in field_errors:
            field_errors[field_name] = []
        field_errors[field_name].append(error['msg'])
    return validation_error_response(field_errors)
```

### Error Response Format

```python
{
    "success": false,
    "error": "validation_error",
    "field_errors": {
        "email": ["Not a valid email address"],
        "password": [
            "Password must be at least 8 characters long",
            "Password must contain at least one digit"
        ]
    }
}
```

## Integration with Services

```python
def update_user_profile(user_id: int):
    try:
        # Validate input with Pydantic v2
        update_data = UserUpdateSchema(**request.get_json())

        # Use service layer
        user_service = UserService()
        updated_user = user_service.update_user(
            user_id=user_id,
            **update_data.model_dump(exclude_unset=True)
        )

        # Return validated response
        return success_response(
            data={'user': UserResponseSchema.model_validate(updated_user).model_dump()}
        )
    except ValidationError as e:
        return handle_validation_error(e)
```

## File Structure

```
app/schemas/
├── __init__.py                 # Updated imports
├── base_schema.py             # Base classes with v2 features
├── user_schema.py             # User management
├── auth_schema.py             # Authentication
├── item_schema.py             # Item management
├── booking_schema.py          # Booking system
├── message_schema.py          # Messaging
├── review_schema.py           # Reviews
├── image_schema.py            # Images
└── error_schema.py            # Error handling
```

## Migration Summary

✅ **Completed Updates:**

1. All schema files renamed with `_schema` suffix
2. `@validator` → `@field_validator` + `@classmethod`
3. `from_orm()` → `model_validate()`
4. `dict()` → `model_dump()`
5. Cross-field validation updated for v2 syntax
6. Route integration updated to use new validation patterns
7. Enhanced error handling with detailed field errors

The WeRent backend now uses modern Pydantic v2 for robust, performant API validation!
