"""
WeRent Backend API - Main Application Entry Point.
Outfit rental platform backend service.
"""

import os
from app import create_app
from app.extensions import db

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # For development only - in production, gunicorn handles this
    port = int(os.environ.get('PORT', 5000))
    
    # Initialize database tables on first run (only in development)
    if os.environ.get('FLASK_ENV') != 'production':
        with app.app_context():
            db.create_all()
            print("Database tables created successfully.")
    
    # Run the development server
    print("Starting WeRent Backend API...")
    print("API Documentation: See API_DOCUMENTATION.md")
    print("Project Status: See PROJECT_STATUS.md")
    app.run(debug=True, host='0.0.0.0', port=port)
