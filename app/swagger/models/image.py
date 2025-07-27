"""
Profile image models for WeRent Backend API Swagger documentation.
Profile image upload related request and response models.
"""

from flask_restx import fields

def create_image_models(api, user_model, success_field, message_field):
    """Create profile image related models."""
    
    # Profile image request
    profile_image_request = api.model('ProfileImageRequest', {
        'profile_image': fields.String(
            required=True,
            description='Base64 encoded image data (JPEG, PNG, WebP supported)',
            example='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/4A==',
            min_length=100
        )
    })
    
    # Image processing info
    image_info_model = api.model('ImageInfo', {
        'original_size': fields.Integer(
            description='Original image size in bytes',
            example=1048576
        ),
        'compressed_size': fields.Integer(
            description='Compressed image size in bytes',
            example=442250
        ),
        'compression_ratio': fields.String(
            description='Compression percentage',
            example='58% reduction'
        ),
        'format': fields.String(
            description='Image format',
            example='JPEG'
        ),
        'dimensions': fields.String(
            description='Image dimensions',
            example='800x600'
        )
    })
    
    # Profile image response data
    profile_image_data = api.model('ProfileImageData', {
        'user': fields.Nested(user_model, description='Updated user information'),
        'image_info': fields.Nested(image_info_model, description='Image processing information')
    })
    
    # Profile image response
    profile_image_response = api.model('ProfileImageResponse', {
        'success': success_field,
        'message': message_field,
        'data': fields.Nested(profile_image_data)
    })
    
    return {
        'profile_image_request': profile_image_request,
        'profile_image_response': profile_image_response,
        'image_info_model': image_info_model,
        'profile_image_data': profile_image_data
    }
