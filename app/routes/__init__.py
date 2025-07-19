"""
Routes package for CamRent Backend API.
Contains all application route blueprints.
"""

from .main import main_bp
from .auth import auth_bp

# Import future route blueprints here
# from .gear import gear_bp
# from .rentals import rentals_bp
# from .reviews import reviews_bp

def register_blueprints(app):
    """Register all application blueprints with the Flask app."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # Register future blueprints here
    # app.register_blueprint(gear_bp)
    # app.register_blueprint(rentals_bp)
    # app.register_blueprint(reviews_bp)

__all__ = ['register_blueprints', 'main_bp', 'auth_bp']
