"""
CORS (Cross-Origin Resource Sharing) configuration for WeRent Backend API.
Handles cross-origin requests between frontend and backend applications.
"""

from flask import request


def setup_cors(app):
    """
    Configure CORS for the Flask application.
    
    Allows requests from specified origins and handles preflight OPTIONS requests.
    This is essential for frontend applications running on different ports/domains
    to communicate with the backend API.
    
    Args:
        app (Flask): Flask application instance
    """
    
    # Define allowed origins (frontend applications)
    ALLOWED_ORIGINS = [
        "http://localhost:3000",    # Next.js development server
        "http://127.0.0.1:3000",    # Alternative localhost
        "http://localhost:3001",    # Alternative React/Next.js port
        "http://127.0.0.1:3001",    # Alternative localhost
        # Add your production frontend URL here when deployed
        # "https://your-frontend-domain.com",
    ]
    
    @app.after_request
    def add_cors_headers(response):
        """
        Add CORS headers to all responses.
        
        This function runs after each request and adds the necessary
        CORS headers to allow cross-origin requests from approved origins.
        """
        origin = request.headers.get("Origin")
        
        # Only allow requests from specified origins for security
        if origin and origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        # Specify allowed HTTP methods
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        )
        
        # Specify allowed headers
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization, X-Requested-With, Accept"
        )
        
        # Cache preflight response for 1 hour
        response.headers["Access-Control-Max-Age"] = "3600"
        
        return response
    
    # Handle preflight OPTIONS requests
    @app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
    @app.route("/<path:path>", methods=["OPTIONS"])
    def handle_preflight_options(path=""):
        """
        Handle preflight OPTIONS requests.
        
        Browsers send OPTIONS requests before actual requests to check
        if the cross-origin request is allowed. This endpoint responds
        to those preflight checks.
        
        Args:
            path (str): The requested path (captured by the route)
            
        Returns:
            tuple: Empty response with 204 No Content status
        """
        return "", 204
    
    print("✅ CORS configured successfully")
    print(f"📍 Allowed origins: {', '.join(ALLOWED_ORIGINS)}")
