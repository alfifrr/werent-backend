from flask_jwt_extended import get_jwt_identity
from app.services.item_service import ItemService
from app.schemas.item_schema import ItemCreateSchema, ItemUpdateSchema
from app.utils.responses import success_response, error_response, not_found_response, internal_error_response
from app.models.item import Item
from app import db

item_service = ItemService()

def list_items_controller():
    try:
        items = item_service.get_available_items()
        data = [item.to_dict() for item in items]
        return success_response('Items retrieved successfully', data)
    except Exception as e:
        return internal_error_response(str(e))

def create_item_controller(json_data):
    """
    Create a new item with optional images.
    
    Args:
        json_data (dict): Dictionary containing item data including optional 'images' list
        
    Returns:
        Response: JSON response with created item data or error message
    """
    try:
        # Validate input data using schema (includes image validation)
        schema = ItemCreateSchema(**json_data)
    except Exception as e:
        return error_response(f'Invalid input: {str(e)}', status_code=422)

    try:
        owner_id = get_jwt_identity()
        
        # Extract images from the validated data
        images = getattr(schema, 'images', None)
        
        # Create the item with all provided data
        item = item_service.create_item(
            name=schema.name,
            type=schema.type,
            size=schema.size,
            gender=schema.gender,
            brand=schema.brand,
            color=schema.color,
            quantity=schema.quantity,
            product_code=schema.product_code,
            description=schema.description,
            price_per_day=schema.price_per_day,
            user_id=owner_id,
            images=images  # Pass images to service layer for processing
        )
        
        # Get the full item data with images
        item_data = item.to_dict()
        item_data['images'] = [img.to_dict() for img in item.images] if hasattr(item, 'images') else []
        
        return success_response('Item created successfully', item_data, status_code=201)
    except Exception as e:
        db.session.rollback()
        error_str = str(e)
        # Handle database constraint violations
        if 'UNIQUE constraint failed: items.product_code' in error_str:
            return error_response('Product code already exists. Please use a unique product code.', status_code=400)
        elif 'IntegrityError' in error_str or 'constraint failed' in error_str:
            return error_response('Database constraint violation. Please check your input data.', status_code=400)
        # Handle other specific errors
        return internal_error_response(str(e))

def get_item_controller(item_id):
    try:
        item = db.session.get(Item, item_id)
        if not item:
            return not_found_response('Item')
        return success_response('Item retrieved successfully', item.to_dict())
    except Exception as e:
        return internal_error_response(str(e))

def update_item_controller(item_id, json_data):
    """
    Update an existing item and its images.
    
    Args:
        item_id (int): ID of the item to update
        json_data (dict): Dictionary containing updated item data including optional 'images' list
        
    Returns:
        Response: JSON response with updated item data or error message
    """
    try:
        # Validate input data using schema (includes image validation)
        schema = ItemUpdateSchema(**json_data)
    except Exception as e:
        return error_response(f'Invalid input: {str(e)}', status_code=422)

    try:
        # Get the current user ID for ownership verification
        current_user_id = get_jwt_identity()
        
        # Get the item to verify ownership
        item = db.session.get(Item, item_id)
        if not item:
            return not_found_response('Item')
            
        # Get current user to check admin status
        from app.models.user import User
        current_user = User.query.get(current_user_id)
        
        # Verify ownership or admin status
        if item.user_id != current_user_id and not (current_user and current_user.is_admin):
            return error_response('You do not have permission to update this item', status_code=403)
        
        # Prepare update data from the validated schema
        update_data = schema.model_dump(exclude_unset=True)
        
        # Remove user_id from update data to prevent unauthorized changes
        if 'user_id' in update_data:
            del update_data['user_id']
        
        # Update the item using the service
        updated_item = item_service.update_item(item_id, **update_data)
        
        if not updated_item:
            return not_found_response('Item')
            
        # Get the full updated item data with images
        item_data = updated_item.to_dict()
        item_data['images'] = [img.to_dict() for img in updated_item.images] if hasattr(updated_item, 'images') else []
        
        return success_response('Item updated successfully', item_data)
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(str(e))

def delete_item_controller(item_id):
    try:
        item = db.session.get(Item, item_id)
        if not item:
            return not_found_response('Item')
        db.session.delete(item)
        db.session.commit()
        return success_response('Item deleted successfully')
    except Exception as e:
        db.session.rollback()
        return internal_error_response(str(e))
