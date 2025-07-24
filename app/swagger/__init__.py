"""
Swagger/OpenAPI 3.0 configuration for WeRent Backend API.
Provides interactive API documentation with Flask-RESTX.
"""

from flask_restx import Api, Namespace, ValidationError
from flask import Blueprint

# Create API blueprint for Swagger documentation
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Configure Swagger/OpenAPI documentation
api = Api(
    api_bp,
    version='1.0.0',
    title='WeRent Backend API',
    description='''
    **WeRent Backend API Documentation**
    
    A comprehensive outfit rental platform backend service.
    
    ## Features
    - **Authentication**: JWT-based user authentication and authorization
    - **User Management**: User registration, login, and profile management
    - **Outfit Management**: Outfit catalog and inventory management
    - **Rental System**: Outfit booking and rental management
    - **Review System**: User reviews and ratings
    
    ## Authentication
    Most endpoints require authentication. Use the `/api/auth/login` endpoint to obtain a JWT token,
    then include it in the `Authorization` header as `Bearer <token>`.
    
    ## Response Format
    All API responses follow a standardized format:
    
    **Success Response:**
    ```json
    {
        "success": true,
        "message": "Operation successful",
        "data": {...}
    }
    ```
    
    **Error Response:**
    ```json
    {
        "success": false,
        "error": "Error description",
        "error_code": "ERROR_CODE",
        "details": {...}
    }
    ```
    
    ## Getting Started
    1. Register a new user account using `/api/auth/signup`
    2. Login to receive a JWT token using `/api/auth/login`
    3. Include the token in subsequent requests: `Authorization: Bearer <token>`
    4. Explore the available endpoints below
    
    ## Base URL
    - **Development**: `http://localhost:5000`
    - **Production**: `https://api.werent.com` (when deployed)
    ''',
    doc='/docs/',
    contact='WeRent Development Team',
    contact_email='dev@werent.com',
    license='MIT',
    license_url='https://opensource.org/licenses/MIT',
    authorizations={
        'JWT': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter JWT token in format: Bearer <token>'
        }
    },
    security='JWT',
    ordered=True
)

# Define namespaces for API organization
auth_ns = Namespace(
    'Authentication', 
    description='User authentication and account management endpoints',
    path='/auth'
)

gear_ns = Namespace(
    'Gear Management', 
    description='Camera equipment catalog and inventory management endpoints (Coming Soon)',
    path='/gear'
)

rental_ns = Namespace(
    'Rental System', 
    description='Equipment booking and rental management endpoints (Coming Soon)',
    path='/rentals'
)

review_ns = Namespace(
    'Review System', 
    description='User reviews and ratings endpoints (Coming Soon)',
    path='/reviews'
)

admin_ns = Namespace(
    'Admin', 
    description='Administrative endpoints for user management and platform administration',
    path='/admin'
)

# Register namespaces
api.add_namespace(auth_ns)
api.add_namespace(gear_ns)
api.add_namespace(rental_ns)
api.add_namespace(review_ns)
api.add_namespace(admin_ns)

# Error handlers for Swagger
@api.errorhandler
def default_error_handler(error):
    """Default error handler for API exceptions."""
    return {
        'success': False,
        'error': 'An unexpected error occurred',
        'error_code': 'INTERNAL_ERROR'
    }, 500

@api.errorhandler(ValidationError)
def validation_error_handler(error):
    """Handle validation errors."""
    return {
        'success': False,
        'error': 'Validation failed',
        'error_code': 'VALIDATION_ERROR',
        'details': {'field_errors': error.messages}
    }, 422
