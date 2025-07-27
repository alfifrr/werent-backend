"""
Main swagger routes registration for WeRent Backend API.
Integrates all swagger-documented routes with the Flask-RESTX API.
"""

from app.swagger import api
from app.swagger.admin_routes import register_all_admin_routes


def register_all_swagger_routes():
    """Register all swagger-documented routes with the API."""
    
    # Register admin routes
    register_all_admin_routes(api)
    
    return api
