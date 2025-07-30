"""
Health check route for WeRent Backend API.
Used for monitoring and deployment verification.
"""

from flask import Blueprint, jsonify
from app.controllers.health import health_check_controller, detailed_health_check_controller

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring service status.
    """
    data, status_code = health_check_controller()
    return jsonify(data), status_code


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """
    Detailed health check with more system information.
    """
    data, status_code = detailed_health_check_controller()
    return jsonify(data), status_code
