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
    try:
        schema = ItemCreateSchema(**json_data)
    except Exception as e:
        return error_response(f'Invalid input: {str(e)}', status_code=422)
    try:
        owner_id = get_jwt_identity()
        # Pass all relevant fields from the schema to the service
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
        return success_response('Item created successfully', item.to_dict(), status_code=201)
    except Exception as e:
        return internal_error_response(str(e))

def get_item_controller(item_id):
    try:
        item = Item.query.get(item_id)
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
        item = Item.query.get(item_id)
        if not item:
            return not_found_response('Item')
        for field, value in schema.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(item, field, value)
        db.session.commit()
        return success_response('Item updated successfully', item.to_dict())
    except Exception as e:
        db.session.rollback()
        return internal_error_response(str(e))

def delete_item_controller(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return not_found_response('Item')
        db.session.delete(item)
        db.session.commit()
        return success_response('Item deleted successfully')
    except Exception as e:
        db.session.rollback()
        return internal_error_response(str(e))
