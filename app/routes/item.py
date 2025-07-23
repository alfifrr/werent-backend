from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils.admin_required import admin_required
from app.controllers.item_controller import list_items_controller, create_item_controller, get_item_controller, update_item_controller, delete_item_controller

item_bp = Blueprint('item', __name__, url_prefix='/items')

# GET /items - List all available items
@item_bp.route('', methods=['GET'])
def list_items():
    return list_items_controller()

# POST /items - Create a new item (admin only)
@item_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def create_item():
    json_data = request.get_json()
    return create_item_controller(json_data)

# GET /items/<int:item_id> - Get item details
@item_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    return get_item_controller(item_id)

# PUT /items/<int:item_id> - Update item info (admin only)
@item_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_item(item_id):
    json_data = request.get_json()
    return update_item_controller(item_id, json_data)

# DELETE /items/<int:item_id> - Delete item (admin only)
@item_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_item(item_id):
    return delete_item_controller(item_id)
