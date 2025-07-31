"""
CORS (Cross-Origin Resource Sharing) configuration for WeRent Backend API.
Handles cross-origin requests between frontend and backend applications.
"""

import os
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
        "http://localhost:5000",    # Backend development server
        "http://127.0.0.1:5000",    # Alternative localhost
    ]
    
    # Add production frontend URL from environment variable
    frontend_url = os.environ.get('FRONTEND_URL', '').strip()
    if frontend_url:
        # Ensure URL has no trailing slash
        frontend_url = frontend_url.rstrip('/')
        # Add both with and without www if applicable
        if frontend_url.startswith('https://www.'):
            ALLOWED_ORIGINS.extend([
                frontend_url,
                frontend_url.replace('www.', '')
            ])
        elif frontend_url.startswith('http'):
            ALLOWED_ORIGINS.append(frontend_url)
    
    # Add common production patterns
    if app.config.get('FLASK_ENV') == 'production':
        # Add your production frontend domains here
        production_origins = [
            "https://werent-frontend.vercel.app",
            "https://werent.com",
            "https://www.werent.com",
        ]
        # Only add if not already in ALLOWED_ORIGINS
        for origin in production_origins:
            if origin not in ALLOWED_ORIGINS:
                ALLOWED_ORIGINS.append(origin)
    
    # Remove duplicates while preserving order
    seen = set()
    ALLOWED_ORIGINS = [x for x in ALLOWED_ORIGINS if not (x in seen or seen.add(x))]
    
    # Debug output
    print("\n🔧 CORS Configuration:")
    print(f"- Environment: {app.config.get('FLASK_ENV', 'development')}")
    print(f"- Frontend URL from ENV: {frontend_url}")
    print(f"- Allowed Origins: {ALLOWED_ORIGINS}\n")
    
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
            # Debug logging
            app.logger.debug(f"CORS: Allowed request from origin: {origin}")
        elif origin:
            app.logger.warning(f"CORS: Blocked request from origin: {origin}. Not in allowed origins.")
            app.logger.debug(f"Allowed origins: {ALLOWED_ORIGINS}")
        else:
            app.logger.debug("CORS: Request with no origin header")
        
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
