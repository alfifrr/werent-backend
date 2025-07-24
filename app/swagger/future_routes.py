"""
Future feature routes for Swagger documentation.
Placeholder endpoints for gear, rentals, reviews, and admin functionality.
"""

from flask_restx import Resource
from app.swagger import gear_ns, rental_ns, review_ns


def register_future_routes(api):
    """Register placeholder routes for future features."""
    
    # Gear Management Routes (Coming Soon)
    @gear_ns.route('/')
    class GearListResource(Resource):
        @gear_ns.doc(
            'list_gear',
            description='List all available camera equipment (Coming Soon)',
            responses={
                200: 'List of available gear',
                501: 'Not implemented yet'
            }
        )
        def get(self):
            """List all available gear."""
            return {
                'success': False,
                'error': 'Gear management endpoints coming soon in Phase 2',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

        @gear_ns.doc(
            'create_gear',
            description='Add new camera equipment (Admin only, Coming Soon)',
            security='JWT',
            responses={
                201: 'Gear created successfully',
                501: 'Not implemented yet'
            }
        )
        def post(self):
            """Add new gear (Admin only)."""
            return {
                'success': False,
                'error': 'Gear management endpoints coming soon in Phase 2',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    @gear_ns.route('/<int:gear_id>')
    class GearResource(Resource):
        @gear_ns.doc(
            'get_gear',
            description='Get specific gear details (Coming Soon)',
            responses={
                200: 'Gear details',
                404: 'Gear not found',
                501: 'Not implemented yet'
            }
        )
        def get(self, gear_id):
            """Get specific gear details."""
            return {
                'success': False,
                'error': 'Gear management endpoints coming soon in Phase 2',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    @gear_ns.route('/categories')
    class GearCategoriesResource(Resource):
        @gear_ns.doc(
            'list_gear_categories',
            description='List all gear categories (Coming Soon)',
            responses={
                200: 'List of gear categories',
                501: 'Not implemented yet'
            }
        )
        def get(self):
            """List all gear categories."""
            return {
                'success': False,
                'error': 'Gear management endpoints coming soon in Phase 2',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    # Rental System Routes (Coming Soon)
    @rental_ns.route('/')
    class RentalListResource(Resource):
        @rental_ns.doc(
            'list_rentals',
            description='List user rentals (Coming Soon)',
            security='JWT',
            responses={
                200: 'List of user rentals',
                501: 'Not implemented yet'
            }
        )
        def get(self):
            """List user rentals."""
            return {
                'success': False,
                'error': 'Rental system endpoints coming soon in Phase 3',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    @rental_ns.route('/checkout')
    class RentalCheckoutResource(Resource):
        @rental_ns.doc(
            'checkout_rental',
            description='Process rental checkout (Coming Soon)',
            security='JWT',
            responses={
                201: 'Rental created successfully',
                501: 'Not implemented yet'
            }
        )
        def post(self):
            """Process rental checkout."""
            return {
                'success': False,
                'error': 'Rental system endpoints coming soon in Phase 3',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    @rental_ns.route('/cart')
    class CartResource(Resource):
        @rental_ns.doc(
            'get_cart',
            description='Get user cart (Coming Soon)',
            security='JWT',
            responses={
                200: 'User cart contents',
                501: 'Not implemented yet'
            }
        )
        def get(self):
            """Get user cart."""
            return {
                'success': False,
                'error': 'Cart functionality coming soon in Phase 3',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

        @rental_ns.doc(
            'add_to_cart',
            description='Add gear to cart (Coming Soon)',
            security='JWT',
            responses={
                201: 'Item added to cart',
                501: 'Not implemented yet'
            }
        )
        def post(self):
            """Add gear to cart."""
            return {
                'success': False,
                'error': 'Cart functionality coming soon in Phase 3',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    # Review System Routes (Coming Soon)
    @review_ns.route('/')
    class ReviewListResource(Resource):
        @review_ns.doc(
            'list_reviews',
            description='List reviews (Coming Soon)',
            responses={
                200: 'List of reviews',
                501: 'Not implemented yet'
            }
        )
        def get(self):
            """List reviews."""
            return {
                'success': False,
                'error': 'Review system endpoints coming soon in Phase 4',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

        @review_ns.doc(
            'create_review',
            description='Create gear review (Coming Soon)',
            security='JWT',
            responses={
                201: 'Review created successfully',
                501: 'Not implemented yet'
            }
        )
        def post(self):
            """Create gear review."""
            return {
                'success': False,
                'error': 'Review system endpoints coming soon in Phase 4',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    @review_ns.route('/gear/<int:gear_id>')
    class GearReviewsResource(Resource):
        @review_ns.doc(
            'get_gear_reviews',
            description='Get reviews for specific gear (Coming Soon)',
            responses={
                200: 'Gear reviews',
                501: 'Not implemented yet'
            }
        )
        def get(self, gear_id):
            """Get reviews for specific gear."""
            return {
                'success': False,
                'error': 'Review system endpoints coming soon in Phase 4',
                'error_code': 'NOT_IMPLEMENTED'
            }, 501

    # Admin Routes - Implemented (see admin_routes.py)
    # The admin functionality has been implemented and documented in admin_routes.py
    # These placeholder routes have been removed to avoid conflicts with the actual implementation
