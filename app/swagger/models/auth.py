"""
Authentication models for WeRent Backend API Swagger documentation.
Authentication-related request and response models.
"""

from flask_restx import fields

def create_auth_models(api, user_model):
    """Create authentication-related models."""
    
    # Authentication request models
    signup_request = api.model('SignupRequest', {
        'email': fields.String(
            required=True,
            description='Valid email address',
            example='john.doe@werent.com',
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
            description='First name (1-50 characters)',
            example='John',
            min_length=1,
            max_length=50
        ),
        'last_name': fields.String(
            required=True,
            description='Last name (1-50 characters)',
            example='Doe',
            min_length=1,
            max_length=50
        ),
        'phone_number': fields.String(
            required=False,
            description='Optional phone number (international format)',
            example='+1234567890'
        )
    })
    
    login_request = api.model('LoginRequest', {
        'email': fields.String(
            required=True,
            description='Registered email address',
            example='john.doe@werent.com'
        ),
        'password': fields.String(
            required=True,
            description='User password',
            example='SecurePass123'
        )
    })
    
    # Authentication response models
    auth_success_response = api.model('AuthSuccessResponse', {
        'success': fields.Boolean(
            required=True,
            description='Authentication success status',
            example=True
        ),
        'message': fields.String(
            required=True,
            description='Authentication response message',
            example='Login successful'
        ),
        'data': fields.Nested(api.model('AuthData', {
            'access_token': fields.String(
                required=True,
                description='JWT access token for API authentication',
                example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
            ),
            'refresh_token': fields.String(
                required=False,
                description='JWT refresh token for token renewal',
                example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
            ),
            'user': fields.Nested(user_model, description='Authenticated user information')
        }))
    })
    
    logout_response = api.model('LogoutResponse', {
        'success': fields.Boolean(
            required=True,
            description='Logout success status',
            example=True
        ),
        'message': fields.String(
            required=True,
            description='Logout response message',
            example='Logout successful'
        )
    })
    
    return {
        'signup_request': signup_request,
        'login_request': login_request,
        'auth_success_response': auth_success_response,
        'logout_response': logout_response
    }
