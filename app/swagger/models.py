"""
Swagger/OpenAPI models for CamRent Backend API.
Defines request/response models for API documentation.
"""

from flask_restx import fields, Model

def create_swagger_models(api):
    """Create and register Swagger models with the API instance."""
    
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
                    'email': 'Invalid email format',
                    'password': 'Password must be at least 8 characters'
                }
            )
        }))
    })
    
    # User models
    user_model = api.model('User', {
        'id': fields.Integer(
            required=True,
            description='Unique user identifier',
            example=1
        ),
        'email': fields.String(
            required=True,
            description='User email address',
            example='john.doe@camrent.com'
        ),
        'first_name': fields.String(
            required=True,
            description='User first name',
            example='John'
        ),
        'last_name': fields.String(
            required=True,
            description='User last name',
            example='Doe'
        ),
        'phone': fields.String(
            required=False,
            description='User phone number',
            example='+1234567890'
        ),
        'created_at': fields.DateTime(
            required=True,
            description='Account creation timestamp',
            example='2025-07-19T10:12:12.908589'
        ),
        'updated_at': fields.DateTime(
            required=True,
            description='Last profile update timestamp',
            example='2025-07-19T10:12:12.908589'
        ),
        'is_active': fields.Boolean(
            required=True,
            description='Account status',
            example=True
        )
    })
    
    # Authentication request models
    signup_request = api.model('SignupRequest', {
        'email': fields.String(
            required=True,
            description='Valid email address',
            example='john.doe@camrent.com',
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        ),
        'password': fields.String(
            required=True,
            description='Password (min 8 chars, uppercase, lowercase, number)',
            example='SecurePass123',
            min_length=8
        ),
        'first_name': fields.String(
            required=True,
            description='User first name',
            example='John',
            min_length=1,
            max_length=50
        ),
        'last_name': fields.String(
            required=True,
            description='User last name',
            example='Doe',
            min_length=1,
            max_length=50
        ),
        'phone': fields.String(
            required=False,
            description='Phone number (optional)',
            example='+1234567890'
        )
    })
    
    login_request = api.model('LoginRequest', {
        'email': fields.String(
            required=True,
            description='Registered email address',
            example='john.doe@camrent.com'
        ),
        'password': fields.String(
            required=True,
            description='User password',
            example='SecurePass123'
        )
    })
    
    profile_update_request = api.model('ProfileUpdateRequest', {
        'first_name': fields.String(
            required=False,
            description='Updated first name',
            example='John',
            min_length=1,
            max_length=50
        ),
        'last_name': fields.String(
            required=False,
            description='Updated last name',
            example='Doe',
            min_length=1,
            max_length=50
        ),
        'phone': fields.String(
            required=False,
            description='Updated phone number',
            example='+1234567890'
        )
    })
    
    # Authentication response models
    auth_success_response = api.model('AuthSuccessResponse', {
        'success': fields.Boolean(
            required=True,
            description='Operation success status',
            example=True
        ),
        'message': fields.String(
            required=True,
            description='Success message',
            example='Login successful'
        ),
        'data': fields.Nested(api.model('AuthData', {
            'user': fields.Nested(user_model, description='User information'),
            'access_token': fields.String(
                description='JWT access token',
                example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
            )
        }))
    })
    
    profile_response = api.model('ProfileResponse', {
        'success': fields.Boolean(
            required=True,
            description='Operation success status',
            example=True
        ),
        'message': fields.String(
            required=True,
            description='Success message',
            example='Profile retrieved successfully'
        ),
        'data': fields.Nested(api.model('ProfileData', {
            'user': fields.Nested(user_model, description='User profile information')
        }))
    })
    
    logout_response = api.model('LogoutResponse', {
        'success': fields.Boolean(
            required=True,
            description='Operation success status',
            example=True
        ),
        'message': fields.String(
            required=True,
            description='Logout message',
            example='Logout successful'
        )
    })
    
    # Future models (placeholders for gear, rentals, etc.)
    gear_model = api.model('Gear', {
        'id': fields.Integer(description='Gear ID', example=1),
        'name': fields.String(description='Gear name', example='Canon EOS R5'),
        'category': fields.String(description='Gear category', example='Camera'),
        'daily_rate': fields.Float(description='Daily rental rate', example=150.00),
        'status': fields.String(description='Availability status', example='available')
    })
    
    rental_model = api.model('Rental', {
        'id': fields.Integer(description='Rental ID', example=1),
        'user_id': fields.Integer(description='User ID', example=1),
        'gear_id': fields.Integer(description='Gear ID', example=1),
        'start_date': fields.DateTime(description='Rental start date'),
        'end_date': fields.DateTime(description='Rental end date'),
        'total_cost': fields.Float(description='Total rental cost', example=300.00),
        'status': fields.String(description='Rental status', example='active')
    })
    
    review_model = api.model('Review', {
        'id': fields.Integer(description='Review ID', example=1),
        'user_id': fields.Integer(description='User ID', example=1),
        'gear_id': fields.Integer(description='Gear ID', example=1),
        'rating': fields.Integer(description='Rating (1-5)', example=5),
        'comment': fields.String(description='Review comment', example='Excellent camera!')
    })
    
    return {
        'base_response': base_response,
        'error_response': error_response,
        'validation_error_response': validation_error_response,
        'user_model': user_model,
        'signup_request': signup_request,
        'login_request': login_request,
        'profile_update_request': profile_update_request,
        'auth_success_response': auth_success_response,
        'profile_response': profile_response,
        'logout_response': logout_response,
        'gear_model': gear_model,
        'rental_model': rental_model,
        'review_model': review_model
    }
