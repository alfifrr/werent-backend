"""
Swagger/OpenAPI models for WeRent Backend API.
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
                    'email': ['Invalid email format'],
                    'password': ['Password must be at least 8 characters long'],
                    'first_name': ['Field required'],
                    'last_name': ['Field required'],
                    'phone': ['Phone number must be between 10-15 digits']
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
        )
    })
    
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
            description='Registered email address (case-insensitive)',
            example='john.doe@werent.com'
        ),
        'password': fields.String(
            required=True,
            description='User password (minimum 8 characters)',
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
                description='JWT access token (expires in 24 hours)',
                example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MjUwMDAwMCwianRpIjoiYWJjZGVmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEyMzQ1IiwibmJmIjoxNjQyNTAwMDAwLCJleHAiOjE2NDI1ODY0MDB9.example_signature'
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
    
    # Outfit models
    outfit_model = api.model('Outfit', {
        'id': fields.Integer(description='Outfit ID', example=1),
        'name': fields.String(required=True, description='Name of the outfit', example='Summer Floral Dress'),
        'type': fields.String(required=True, description='Type of outfit', enum=['Dress', 'Top', 'Bottom', 'Outerwear', 'Shoes', 'Accessory', 'Jewelry', 'Bag', 'Formal Wear', 'Costume', 'Other'], example='Dress'),
        'size': fields.String(required=True, description='Size of the outfit', enum=['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'One Size'], example='M'),
        'gender': fields.String(required=True, description='Gender category', enum=["Men's", "Women's", 'Unisex', 'Kids'], example="Women's"),
        'brand': fields.String(description='Brand name', example='Zara'),
        'color': fields.String(description='Color of the outfit', example='Floral'),
        'material': fields.String(description='Material composition', example='Cotton 70%, Polyester 30%'),
        'condition': fields.String(description='Condition of the outfit', example='Like New'),
        'quantity': fields.Integer(description='Available quantity', example=1),
        'product_code': fields.String(required=True, description='Unique product code', example='OF-12345'),
        'description': fields.String(required=True, description='Detailed description', example='Beautiful summer dress with floral pattern, perfect for outdoor events.'),
        'price_per_day': fields.Float(required=True, description='Daily rental price', example=25.99),
        'dry_cleaning_fee': fields.Float(description='Additional cleaning fee', example=5.00),
        'deposit_amount': fields.Float(description='Security deposit amount', example=50.00),
        'rating': fields.Float(description='Average rating (1-5)', example=4.8),
        'is_available': fields.Boolean(description='Availability status', example=True),
        'created_at': fields.DateTime(description='Creation timestamp'),
        'user_id': fields.Integer(description='Owner user ID')
    })
    
    booking_model = api.model('Booking', {
        'id': fields.Integer(description='Booking ID', example=1),
        'user_id': fields.Integer(description='Renter user ID', example=2),
        'item_id': fields.Integer(description='Outfit ID', example=1),
        'start_date': fields.Date(required=True, description='Rental start date (YYYY-MM-DD)'),
        'end_date': fields.Date(required=True, description='Rental end date (YYYY-MM-DD)'),
        'total_price': fields.Float(description='Total booking cost', example=129.95),
        'status': fields.String(description='Booking status', enum=['PENDING', 'PAID', 'CANCELLED', 'PASTDUE', 'RETURNED'], example='PENDING'),
        'is_paid': fields.Boolean(description='Payment status', example=False),
        'created_at': fields.DateTime(description='Booking creation timestamp')
    })
    
    review_model = api.model('Review', {
        'id': fields.Integer(description='Review ID', example=1),
        'user_id': fields.Integer(description='Reviewer user ID', example=2),
        'item_id': fields.Integer(description='Outfit ID', example=1),
        'rating': fields.Integer(required=True, description='Rating (1-5)', example=5, min=1, max=5),
        'comment': fields.String(description='Review comment', example='Beautiful dress, perfect fit!'),
        'created_at': fields.DateTime(description='Review timestamp')
    })
    
    image_model = api.model('Image', {
        'id': fields.Integer(description='Image ID', example=1),
        'url': fields.String(description='Image URL', example='https://example.com/images/dress-1.jpg'),
        'is_primary': fields.Boolean(description='If this is the primary image', example=True)
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
        'outfit_model': outfit_model,
        'booking_model': booking_model,
        'review_model': review_model,
        'image_model': image_model
    }
