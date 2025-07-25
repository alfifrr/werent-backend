"""
Routes package for WeRent Backend API.
Contains all application route blueprints.
"""

from .main import main_bp
from .auth import auth_bp
from .health import health_bp
from .item import item_bp
from .ticketing import ticketing_bp
from .admin import admin_bp
from .payment import payment_bp
from ..swagger.swagger_ui import swagger_bp

from .review_routes import review_bp
# Import future route blueprints here
# from .gear import gear_bp
# from .rentals import rentals_bp

def register_blueprints(app):
    """Register all application blueprints with the Flask app."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(swagger_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(ticketing_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payment_bp)

    # Register future blueprints here
    # app.register_blueprint(gear_bp)
    # app.register_blueprint(rentals_bp)
    # app.register_blueprint(reviews_bp)

__all__ = ['register_blueprints', 'main_bp', 'auth_bp', 'health_bp', 'swagger_bp', 'ticketing_bp', 'review_bp', 'admin_bp', 'payment_bp']
