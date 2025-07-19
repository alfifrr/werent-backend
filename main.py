"""
CamRent Backend API - Main Application Entry Point.
Camera equipment rental platform backend service.
"""

from app import create_app
from app.extensions import db

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Initialize database tables on first run
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
    
    # Run the development server
    print("Starting CamRent Backend API...")
    print("API Documentation: See API_DOCUMENTATION.md")
    print("Project Status: See PROJECT_STATUS.md")
    app.run(debug=True, host='0.0.0.0', port=5000)
