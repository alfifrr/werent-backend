"""
Main routes for CamRent Backend API.
Contains general application routes and health checks.
"""

from flask import Blueprint

# Create main blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """API root endpoint with basic information."""
    return {
        'name': 'CamRent Backend API',
        'version': '1.0.0',
        'status': 'running',
        'message': 'Welcome to CamRent - Camera Equipment Rental Platform'
    }


@main_bp.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return {
        'status': 'healthy',
        'timestamp': '2025-07-19T10:00:00Z'
    }


@main_bp.route('/api')
def api_info():
    """API information endpoint."""
    return {
        'api_name': 'CamRent Backend API',
        'version': '1.0.0',
        'documentation': '/api/docs',
        'endpoints': {
            'authentication': '/api/auth/*',
            'gear': '/api/gear/* (coming soon)',
            'rentals': '/api/rentals/* (coming soon)',
            'reviews': '/api/reviews/* (coming soon)'
        }
    }
