"""
Swagger-documented admin routes for WeRent Backend API.
Administrative endpoints with comprehensive OpenAPI documentation.
"""

from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.swagger import admin_ns
from app.swagger.models import create_swagger_models
from app.controllers.admin import (
    promote_user_controller, 
    get_all_admins_controller, 
    get_admin_by_id_controller
)
from app.utils.admin_required import admin_required


def register_admin_routes(api):
    """Register admin routes with Swagger documentation."""
    
    print("🔧 Registering admin routes with Swagger...")  # Debug output
    
    # Create Swagger models
    models = create_swagger_models(api)

    @admin_ns.route('/users/promote')
    class UserPromotionResource(Resource):
        @admin_ns.doc(
            'promote_demote_user',
            description='''
            Promote a regular user to admin status or demote an admin to regular user.
            
            **Authorization Required:**
            - Valid JWT token in Authorization header
            - Current user must have admin privileges
            
            **Actions Available:**
            - `promote`: Convert regular user to admin
            - `demote`: Convert admin user to regular user
            
            **Business Rules:**
            - Users cannot promote/demote themselves
            - Only existing admins can perform these operations
            - Target user must exist in the system
            - Action must be valid ("promote" or "demote")
            
            **Response includes:**
            - Action performed status (true/false)
            - Previous admin status
            - New admin status
            - Updated user information
            ''',
            security='JWT',
            responses={
                200: ('User promotion/demotion successful', models['admin_promotion_response']),
                400: ('Invalid request data', models['error_response']),
                401: ('Authentication required', models['error_response']),
                403: ('Admin access required', models['error_response']),
                404: ('Target user not found', models['error_response']),
                422: ('Validation failed', models['validation_error_response'])
            }
        )
        @admin_ns.expect(models['admin_promotion_request'], validate=True)
        @admin_ns.marshal_with(models['admin_promotion_response'])
        @jwt_required()
        @admin_required
        def post(self):
            """Promote or demote a user's admin status."""
            data = request.get_json()
            return promote_user_controller(data)

    @admin_ns.route('/users')
    class AdminListResource(Resource):
        @admin_ns.doc(
            'get_all_admins',
            description='''
            Retrieve a list of all users with admin privileges.
            
            **Authorization Required:**
            - Valid JWT token in Authorization header
            - Current user must have admin privileges
            
            **Response includes:**
            - Total count of admin users
            - Array of admin user objects with full profile information
            - User creation and update timestamps
            - Admin status verification
            
            **Use Cases:**
            - Admin dashboard user management
            - Admin user auditing
            - Platform administration oversight
            ''',
            security='JWT',
            responses={
                200: ('Admin users retrieved successfully', models['admin_list_response']),
                401: ('Authentication required', models['error_response']),
                403: ('Admin access required', models['error_response'])
            }
        )
        @admin_ns.marshal_with(models['admin_list_response'])
        @jwt_required()
        @admin_required
        def get(self):
            """Get all admin users."""
            return get_all_admins_controller()

    @admin_ns.route('/users/<int:admin_id>')
    class AdminDetailResource(Resource):
        @admin_ns.doc(
            'get_admin_by_id',
            description='''
            Retrieve detailed information about a specific admin user by their ID.
            
            **Authorization Required:**
            - Valid JWT token in Authorization header
            - Current user must have admin privileges
            
            **Path Parameters:**
            - `admin_id`: Integer ID of the admin user to retrieve
            
            **Response includes:**
            - Complete admin user profile
            - Account creation and modification timestamps
            - Admin status verification
            - Contact information and preferences
            
            **Use Cases:**
            - Admin profile management
            - Admin user verification
            - Detailed admin information lookup
            ''',
            security='JWT',
            params={
                'admin_id': {
                    'description': 'ID of the admin user to retrieve',
                    'type': 'integer',
                    'required': True,
                    'example': 25
                }
            },
            responses={
                200: ('Admin user retrieved successfully', models['admin_detail_response']),
                401: ('Authentication required', models['error_response']),
                403: ('Admin access required', models['error_response']),
                404: ('Admin user not found', models['error_response'])
            }
        )
        @admin_ns.marshal_with(models['admin_detail_response'])
        @jwt_required()
        @admin_required
        def get(self, admin_id):
            """Get admin user by ID."""
            return get_admin_by_id_controller(admin_id)

    print("✅ Admin routes registered successfully!")  # Debug output
    return admin_ns


def register_all_admin_routes(api):
    """Register all admin-related routes."""
    return register_admin_routes(api)
