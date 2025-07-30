"""
Admin routes for WeRent Backend API.
Handles admin-specific read-only operations.
Admin status changes are handled via manual database operations.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.admin_required import admin_required
from app.controllers.admin import (
    get_all_admins_controller, 
    get_admin_by_id_controller
)

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


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
