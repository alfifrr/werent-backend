"""
Controller functions for main routes (index, health, api info)
"""

def get_index_info():
    """Return API root information."""
    return {
        'name': 'WeRent Backend API',
        'version': '1.0.0',
        'status': 'running',
        'message': 'Welcome to WeRent - Equipment Rental Platform'
    }

def get_health_status():
    """Return health status."""
    return {
        'status': 'healthy',
        'timestamp': '2025-07-19T10:00:00Z'
    }

def get_api_info():
    """Return API information."""
    return {
        'api_name': 'WeRent Backend API',
        'version': '1.0.0',
        'documentation': '/docs/',
        'endpoints': {
            'authentication': '/api/auth/*',
            'equipment': '/api/equipment/* (coming soon)',
            'rentals': '/api/rentals/* (coming soon)',
            'reviews': '/api/reviews/* (coming soon)'
        }
    }
