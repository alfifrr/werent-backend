"""
Main routes for WeRent Backend API.
Contains general application routes and health checks.
"""

from flask import Blueprint
from app.controllers.main import get_index_info, get_health_status, get_api_info

# Create main blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')

def index():
    """API root endpoint with basic information."""
    return get_index_info()


@main_bp.route('/health')

def health_check():
    """Health check endpoint for monitoring."""
    return get_health_status()


@main_bp.route('/api')

def api_info():
    """API information endpoint."""
    return get_api_info()
