"""
Server configuration for Swagger UI.
Handles environment-specific server URLs and configuration.
"""

import os


def get_server_urls():
    """
    Get server URLs based on environment and request context.
    Returns appropriate server URLs for Swagger documentation.

    These URLs represent the base API endpoints, not the documentation URLs.
    Users can switch between development and production APIs in the Swagger UI.
    """
    servers = []

    # Development server (localhost)
    servers.append(
        {
            "url": "http://localhost:5000",
            "description": "Development server (localhost)",
        }
    )

    # Production server (Render deployment)
    production_url = "https://werent-backend-api.onrender.com"
    servers.append(
        {"url": production_url, "description": "Production server (Render deployment)"}
    )

    # If running in production, put production server first in dropdown
    if os.environ.get("FLASK_ENV") == "production":
        servers.reverse()

    return servers


def get_api_info():
    """Get API information for OpenAPI specification."""
    return {
        "title": "WeRent Backend API",
        "version": "1.0.0",
        "description": """
# WeRent Backend API Documentation

A comprehensive camera and photography equipment rental platform backend service.

## Features
- **Authentication**: JWT-based user authentication and authorization ✅
- **User Management**: User registration, login, and profile management ✅
- **Gear Management**: Camera equipment catalog and inventory 🚧
- **Rental System**: Equipment booking and rental management 🚧
- **Review System**: User reviews and ratings 🚧
- **Admin Panel**: Administrative features for managing the platform ✅

## Authentication
Most endpoints require authentication. Use the `/api/auth/login` endpoint to obtain JWT tokens,
then include the access token in the `Authorization` header as `Bearer <token>`.

**Token System:**
- **Access Token**: Expires in 15 minutes, used for API requests
- **Refresh Token**: Expires in 30 days, used to get new access tokens
- When access token expires, use `/api/auth/refresh` with refresh token to get a new access token

## Response Format
All API responses follow a standardized format:

**Success Response:**
```json
{
    "success": true,
    "message": "Operation successful",
    "data": {...}
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "Error description",
    "error_code": "ERROR_CODE",
    "details": {...}
}
```

## Getting Started
1. Register a new user account using `/api/auth/signup` (no JWT created)
2. Login using `/api/auth/login` to receive both access and refresh tokens
3. Include the access token in subsequent requests: `Authorization: Bearer <access_token>`
4. Explore the available endpoints below

## Base URL
- **Development**: `http://localhost:5000`
- **Production**: `https://werent-backend-api.onrender.com` (when deployed)

## Current Implementation Status

### ✅ Implemented Features
- 🔐 **Authentication System**: Complete JWT-based auth with refresh tokens
- 👤 **User Profile Management**: Profile updates with Base64 image support
- 🛡️ **Admin Management**: User promotion and admin user management
- 🏥 **Health Monitoring**: Basic and detailed health check endpoints

### 🚧 In Development
- 📷 **Gear Management**: Planning phase
- 🏪 **Rental System**: Planning phase  
- ⭐ **Review System**: Planning phase

## Project Roadmap
- ✅ **Phase 1**: Authentication & User Management (Completed)
- 🚧 **Phase 2**: Gear Management (Planning)
- 🚧 **Phase 3**: Rental System (Planning)
- 🚧 **Phase 4**: Review System (Planning)
- 🚧 **Phase 5**: Advanced Admin Features (Planning)
""",
        "contact": {
            "name": "WeRent Development Team",
            "email": "dev@werent.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }


def get_security_schemes():
    """Get security schemes for OpenAPI specification."""
    return {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token in format: Bearer <token>"
        }
    }


def get_tags():
    """Get API tags for grouping endpoints."""
    return [
        {
            "name": "Authentication",
            "description": "User authentication and account management",
        },
        {
            "name": "Gear Management",
            "description": "Camera equipment catalog and inventory (Coming Soon)",
        },
        {
            "name": "Rental System",
            "description": "Equipment booking and rental management (Coming Soon)",
        },
        {
            "name": "Review System",
            "description": "User reviews and ratings (Coming Soon)",
        },
        {"name": "Admin", "description": "Administrative endpoints for user management and platform administration"},
    ]
