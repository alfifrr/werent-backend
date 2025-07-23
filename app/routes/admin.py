"""
Admin routes for WeRent Backend API.
Handles admin-specific operations like user promotion/demotion.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils.admin_required import admin_required
from app.controllers.admin import (
    promote_user_controller, 
    get_all_admins_controller, 
    get_admin_by_id_controller
)

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/users/promote', methods=['POST'])
@jwt_required()
@admin_required
def promote_user():
    """
    Promote or demote a user to/from admin status.
    
    Expected JSON payload:
    {
        "user_id": 123,
        "action": "promote"  # or "demote"
    }
    """
    data = request.get_json()
    return promote_user_controller(data)


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_admins():
    """
    Get all admin users.
    Only accessible by existing admins.
    """
    return get_all_admins_controller()


@admin_bp.route('/users/<int:admin_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_by_id(admin_id):
    """
    Get specific admin user by ID.
    Only accessible by existing admins.
    """
    return get_admin_by_id_controller(admin_id)
