"""
CamRent Backend API Application Factory.
Creates and configures the Flask application instance.
"""

from flask import Flask

from config import get_config
from app.extensions import init_extensions, db
from app.routes import register_blueprints


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str, optional): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name:
        from config.config import config
        app.config.from_object(config[config_name])
    else:
        app.config.from_object(get_config())
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Error handlers
    register_error_handlers(app)
    
    # CLI commands
    register_commands(app)
    
    return app


def register_error_handlers(app):
    """Register application error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        return {
            'success': False,
            'error': 'Endpoint not found',
            'error_code': 'NOT_FOUND'
        }, 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return {
            'success': False,
            'error': 'Method not allowed',
            'error_code': 'METHOD_NOT_ALLOWED'
        }, 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'success': False,
            'error': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }, 500


def register_commands(app):
    """Register CLI commands for the application."""
    
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized successfully.')
    
    @app.cli.command()
    def create_admin():
        """Create an admin user."""
        from app.models import User
        
        email = input('Enter admin email: ')
        password = input('Enter admin password: ')
        first_name = input('Enter first name: ')
        last_name = input('Enter last name: ')
        
        # Check if admin already exists
        if User.find_by_email(email):
            print('User with this email already exists.')
            return
        
        # Create admin user
        admin = User(
            email=email.lower().strip(),
            first_name=first_name,
            last_name=last_name,
            is_admin=True
        )
        admin.set_password(password)
        admin.save()
        
        print(f'Admin user created successfully: {email}')
    
    @app.cli.command()
    def reset_db():
        """Reset the database (drops all tables and recreates them)."""
        confirmation = input('This will delete all data. Are you sure? (yes/no): ')
        if confirmation.lower() == 'yes':
            db.drop_all()
            db.create_all()
            print('Database reset successfully.')
        else:
            print('Database reset cancelled.')
