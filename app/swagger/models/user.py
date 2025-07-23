"""
User models for WeRent Backend API Swagger documentation.
User-related request and response models.
"""

from flask_restx import fields

def create_user_models(api):
    """Create user-related models."""
    
    # User model
    user_model = api.model('User', {
        'id': fields.Integer(
            required=True,
            description='Unique user identifier',
            example=1
        ),
        'email': fields.String(
            required=True,
            description='User email address',
            example='john.doe@werent.com'
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
        'phone_number': fields.String(
            required=False,
            description='User phone number',
            example='+1234567890'
        ),
        'is_admin': fields.Boolean(
            required=True,
            description='Admin status',
            example=False
        ),
        'is_verified': fields.Boolean(
            required=True,
            description='Verification status',
            example=False
        ),
        'is_active': fields.Boolean(
            required=True,
            description='Account status',
            example=True
        ),
        'uuid': fields.String(
            required=True,
            description='Unique user UUID',
            example='550e8400-e29b-41d4-a716-446655440000'
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
        'profile_image': fields.String(
            required=False,
            description='Base64 encoded profile image data',
            example=None
        )
    })
    
    # Profile update request
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
        'phone_number': fields.String(
            required=False,
            description='Updated phone number',
            example='+1234567890'
        )
    })
    
    # Profile response
    profile_response = api.model('ProfileResponse', {
        'success': fields.Boolean(
            required=True,
            description='Request success status',
            example=True
        ),
        'message': fields.String(
            required=True,
            description='Response message',
            example='Profile retrieved successfully'
        ),
        'data': fields.Nested(api.model('ProfileData', {
            'user': fields.Nested(user_model, description='User profile information')
        }))
    })
    
    return {
        'user_model': user_model,
        'profile_update_request': profile_update_request,
        'profile_response': profile_response
    }
