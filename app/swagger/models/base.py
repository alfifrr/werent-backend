"""
Base response models for WeRent Backend API Swagger documentation.
Common response structures used across all endpoints.
"""

from flask_restx import fields

def create_base_models(api):
    """Create base response models."""
    
    # Base response models
    base_response = api.model('BaseResponse', {
        'success': fields.Boolean(
            required=True,
            description='Indicates if the request was successful',
            example=True
        ),
        'message': fields.String(
            required=True,
            description='Human-readable response message',
            example='Operation completed successfully'
        )
    })
    
    error_response = api.model('ErrorResponse', {
        'success': fields.Boolean(
            required=True,
            description='Always false for error responses',
            example=False
        ),
        'error': fields.String(
            required=True,
            description='Error message describing what went wrong',
            example='Invalid email format'
        ),
        'error_code': fields.String(
            required=False,
            description='Machine-readable error code',
            example='VALIDATION_ERROR'
        ),
        'details': fields.Raw(
            required=False,
            description='Additional error details and context',
            example={'field_errors': {'email': 'Invalid format'}}
        )
    })
    
    validation_error_response = api.model('ValidationErrorResponse', {
        'success': fields.Boolean(
            required=True,
            description='Always false for validation errors',
            example=False
        ),
        'error': fields.String(
            required=True,
            description='Validation error message',
            example='Validation failed'
        ),
        'error_code': fields.String(
            required=True,
            description='Validation error code',
            example='VALIDATION_ERROR'
        ),
        'details': fields.Nested(api.model('ValidationDetails', {
            'field_errors': fields.Raw(
                description='Field-specific validation errors',
                example={
                    'email': ['Invalid email format'],
                    'password': ['Password must be at least 8 characters long'],
                    'first_name': ['Field required'],
                    'last_name': ['Field required'],
                    'phone': ['Phone number must be between 10-15 digits']
                }
            )
        }))
    })
    
    # Common fields
    success_field = fields.Boolean(
        required=True,
        description='Indicates if the request was successful',
        example=True
    )
    
    message_field = fields.String(
        required=True,
        description='Human-readable response message',
        example='Operation completed successfully'
    )
    
    return {
        'base_response': base_response,
        'error_response': error_response,
        'validation_error_response': validation_error_response,
        'success_field': success_field,
        'message_field': message_field
    }
