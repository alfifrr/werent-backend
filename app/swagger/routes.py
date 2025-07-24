"""
Main swagger routes registration for WeRent Backend API.
Integrates all swagger-documented routes with the Flask-RESTX API.
"""

from app.swagger import api
from app.swagger.admin_routes import register_all_admin_routes
from app.swagger.future_routes import register_future_routes


def register_all_swagger_routes():
    """Register all swagger-documented routes with the API."""
    
    # Register admin routes
    register_all_admin_routes(api)
    
    # Register future/placeholder routes
    register_future_routes(api)
    
    return api
