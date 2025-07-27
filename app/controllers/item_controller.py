from flask_jwt_extended import get_jwt_identity
from app.services.item_service import ItemService
from app.schemas.item_schema import ItemCreateSchema, ItemUpdateSchema
from app.utils.responses import success_response, error_response, not_found_response, internal_error_response
from app.models.item import Item
from app import db
from app.utils.validators import validate_base64_image
from app.models.image import Image

item_service = ItemService()

def list_items_controller():
    try:
        items = item_service.get_available_items()
        data = [item.to_dict() for item in items]
        return success_response('Items retrieved successfully', data)
    except Exception as e:
        return internal_error_response(str(e))

def create_item_controller(json_data):
    try:
        schema = ItemCreateSchema(**json_data)
    except Exception as e:
        return error_response(f'Invalid input: {str(e)}', status_code=422)

    try:
        owner_id = get_jwt_identity()
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
            user_id=owner_id
        )
        # Handle multiple images if provided
        images = getattr(schema, 'images', None)
        if images:
            for img in images:
                if not validate_base64_image(img):
                    return error_response('Invalid image in images array: not a valid base64-encoded image', status_code=400)
                # Store with data URL prefix if missing
                if not img.startswith('data:image'):
                    img = f'data:image/jpeg;base64,{img}'
                image = Image(image_base64=img, item_id=item.id)
                image.save()

        return success_response('Item created successfully', item.to_dict(), status_code=201)
    except Exception as e:
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
    try:
        schema = ItemUpdateSchema(**json_data)
    except Exception as e:
        return error_response(f'Invalid input: {str(e)}', status_code=422)

    try:
        item = db.session.get(Item, item_id)
        if not item:
            return not_found_response('Item')
        # Update item fields except image_base64
        for field, value in schema.model_dump(exclude_unset=True).items():
            if value is not None and field not in ['images', 'user_id']:
                setattr(item, field, value)
        db.session.commit()
        # Handle multiple images if provided
        images = getattr(schema, 'images', None)
        if images:
            # Validate all images before DB ops
            for img in images:
                if not validate_base64_image(img):
                    return error_response('Invalid image in images array: not a valid base64-encoded image', status_code=400)
            else:
                # Only proceed if all images are valid
                # Remove all existing images for this item
                existing_images = Image.find_by_item_id(item.id)
                for img_obj in existing_images:
                    img_obj.delete()
                # Add new images
                for img in images:
                    # Store with data URL prefix if missing
                    if not img.startswith('data:image'):
                        img = f'data:image/jpeg;base64,{img}'
                    image = Image(image_base64=img, item_id=item.id)
                    image.save()

        return success_response('Item updated successfully', item.to_dict())
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
