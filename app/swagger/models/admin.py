"""
Admin models for WeRent Backend API Swagger documentation.
Admin-related request and response models.
"""

from flask_restx import fields

def create_admin_models(api, user_model, success_field, message_field):
    """Create admin-related models."""
    
    # Admin request fields
    user_id_field = fields.Integer(
        required=True,
        description='ID of the user to promote/demote',
        example=26,
        min=1
    )
    
    admin_action_field = fields.String(
        required=True,
        description='Action to perform on user',
        enum=['promote', 'demote'],
        example='promote'
    )
    
    # Admin promotion models
    admin_promotion_request = api.model('AdminPromotionRequest', {
        'user_id': user_id_field,
        'action': admin_action_field
    })
    
    admin_promotion_data = api.model('AdminPromotionData', {
        'action_performed': fields.Boolean(
            required=True,
            description='Whether the action was successfully performed',
            example=True
        ),
        'previous_status': fields.Boolean(
            required=True,
            description='Previous admin status of the user',
            example=False
        ),
        'new_status': fields.Boolean(
            required=True,
            description='New admin status of the user',
            example=True
        ),
        'user': fields.Nested(user_model, description='Updated user information')
    })
    
    admin_promotion_response = api.model('AdminPromotionResponse', {
        'success': success_field,
        'message': message_field,
        'data': fields.Nested(admin_promotion_data)
    })
    
    # Admin list models
    admin_list_data = api.model('AdminListData', {
        'admins': fields.List(
            fields.Nested(user_model),
            required=True,
            description='List of all admin users'
        ),
        'total_count': fields.Integer(
            required=True,
            description='Total number of admin users',
            example=4
        )
    })
    
    admin_list_response = api.model('AdminListResponse', {
        'success': success_field,
        'message': message_field,
        'data': fields.Nested(admin_list_data)
    })
    
    # Admin detail models
    admin_detail_data = api.model('AdminDetailData', {
        'admin': fields.Nested(
            user_model,
            required=True,
            description='Admin user details'
        )
    })
    
    admin_detail_response = api.model('AdminDetailResponse', {
        'success': success_field,
        'message': message_field,
        'data': fields.Nested(admin_detail_data)
    })
    
    return {
        'user_id_field': user_id_field,
        'admin_action_field': admin_action_field,
        'admin_promotion_request': admin_promotion_request,
        'admin_promotion_data': admin_promotion_data,
        'admin_promotion_response': admin_promotion_response,
        'admin_list_data': admin_list_data,
        'admin_list_response': admin_list_response,
        'admin_detail_data': admin_detail_data,
        'admin_detail_response': admin_detail_response
    }
