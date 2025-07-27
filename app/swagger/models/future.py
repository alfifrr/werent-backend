"""
Future models for WeRent Backend API Swagger documentation.
Placeholder models for upcoming features.
"""

from flask_restx import fields

def create_future_models(api):
    """Create models for future features."""
    
    # Outfit/Gear models (Coming Soon)
    outfit_model = api.model('Outfit', {
        'id': fields.Integer(description='Outfit ID', example=1),
        'name': fields.String(description='Outfit name', example='Elegant Evening Dress'),
        'description': fields.String(description='Outfit description', example='Beautiful black evening dress perfect for formal events'),
        'category': fields.String(description='Outfit category', example='Evening Wear'),
        'size': fields.String(description='Outfit size', example='M'),
        'price_per_day': fields.Float(description='Daily rental price', example=75.00),
        'available': fields.Boolean(description='Availability status', example=True),
        'created_at': fields.DateTime(description='Creation timestamp')
    })
    
    # Booking models (Coming Soon)
    booking_model = api.model('Booking', {
        'id': fields.Integer(description='Booking ID', example=1),
        'user_id': fields.Integer(description='User ID', example=1),
        'item_id': fields.Integer(description='Outfit ID', example=1),
        'start_date': fields.Date(description='Rental start date', example='2025-07-20'),
        'end_date': fields.Date(description='Rental end date', example='2025-07-22'),
        'total_price': fields.Float(description='Total rental price', example=150.00),
        'status': fields.String(description='Booking status', enum=['PENDING', 'PAID', 'CANCELLED', 'PASTDUE', 'RETURNED'], example='PENDING'),
        'is_paid': fields.Boolean(description='Payment status', example=False),
        'created_at': fields.DateTime(description='Booking creation timestamp')
    })
    
    # Review models (Coming Soon)
    review_model = api.model('Review', {
        'id': fields.Integer(description='Review ID', example=1),
        'user_id': fields.Integer(description='Reviewer user ID', example=2),
        'item_id': fields.Integer(description='Outfit ID', example=1),
        'rating': fields.Integer(required=True, description='Rating (1-5)', example=5, min=1, max=5),
        'comment': fields.String(description='Review comment', example='Beautiful dress, perfect fit!'),
        'created_at': fields.DateTime(description='Review timestamp')
    })
    
    # Image models (Coming Soon)
    image_model = api.model('Image', {
        'id': fields.Integer(description='Image ID', example=1),
        'url': fields.String(description='Image URL', example='https://example.com/images/dress-1.jpg'),
        'is_primary': fields.Boolean(description='If this is the primary image', example=True)
    })
    
    return {
        'outfit_model': outfit_model,
        'booking_model': booking_model,
        'review_model': review_model,
        'image_model': image_model
    }
