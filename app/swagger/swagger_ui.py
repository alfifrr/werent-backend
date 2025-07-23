"""
Enhanced Swagger UI integration for WeRent Backend API.
Provides comprehensive interactive API documentation using OpenAPI 3.0 specification.
"""

import os
from flask import Blueprint, render_template_string, jsonify, url_for, request
import json

# Create Swagger blueprint
swagger_bp = Blueprint('swagger', __name__, url_prefix='/docs')

def get_server_urls():
    """
    Get server URLs based on environment and request context.
    Returns appropriate server URLs for Swagger documentation.
    
    These URLs represent the base API endpoints, not the documentation URLs.
    Users can switch between development and production APIs in the Swagger UI.
    """
    servers = []
    
    # Development server (localhost)
    servers.append({
        "url": "http://localhost:5000",
        "description": "Development server (localhost)"
    })
    
    # Production server (Render deployment)
    production_url = "https://werent-backend-api.onrender.com"
    servers.append({
        "url": production_url,
        "description": "Production server (Render deployment)"
    })
    
    # If running in production, put production server first in dropdown
    if os.environ.get('FLASK_ENV') == 'production':
        servers.reverse()
    
    return servers

# OpenAPI 3.0 specification
def get_openapi_spec():
    """Generate comprehensive OpenAPI 3.0 specification for the API."""
    return {
        "openapi": "3.0.0",
        "info": {
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
- **Admin Panel**: Administrative features for managing the platform 🚧

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
4. When access token expires (15 min), use refresh token at `/api/auth/refresh` to get new access token
5. Explore the available endpoints below

## Development Status
- ✅ **Authentication System**: Fully implemented
- 🚧 **Gear Management**: In development
- 🚧 **Rental System**: Planning phase
- 🚧 **Review System**: Planning phase
- 🚧 **Admin Panel**: Planning phase

For the latest development status, see the PROJECT_STATUS.md file.
            """,
            "contact": {
                "name": "WeRent Development Team",
                "email": "dev@werent.com"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "servers": get_server_urls(),
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Enter JWT token in format: Bearer <token>"
                }
            },
            "schemas": {
                # Item Models
                "Item": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "name": {"type": "string", "example": "Summer Dress"},
                        "type": {"type": "string", "example": "Dress"},
                        "size": {"type": "string", "example": "M"},
                        "gender": {"type": "string", "example": "Women's"},
                        "brand": {"type": "string", "example": "Zara"},
                        "color": {"type": "string", "example": "Red"},
                        "quantity": {"type": "integer", "example": 3},
                        "product_code": {"type": "string", "example": "SKU12345"},
                        "description": {"type": "string", "example": "Lightweight summer dress."},
                        "price_per_day": {"type": "number", "example": 15.0},
                        "rating": {"type": "number", "example": 4.7},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "user_id": {"type": "integer", "example": 2},
                        "images": {"type": "array", "items": {"type": "string"}, "example": ["https://.../image1.jpg"]}
                    }
                },
                "ItemCreateRequest": {
                    "type": "object",
                    "required": ["name", "type", "size", "gender", "product_code", "description", "price_per_day", "quantity"],
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "size": {"type": "string"},
                        "gender": {"type": "string"},
                        "brand": {"type": "string"},
                        "color": {"type": "string"},
                        "quantity": {"type": "integer"},
                        "product_code": {"type": "string"},
                        "description": {"type": "string"},
                        "price_per_day": {"type": "number"}
                    }
                },
                "ItemUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "size": {"type": "string"},
                        "gender": {"type": "string"},
                        "brand": {"type": "string"},
                        "color": {"type": "string"},
                        "quantity": {"type": "integer"},
                        "product_code": {"type": "string"},
                        "description": {"type": "string"},
                        "price_per_day": {"type": "number"}
                    }
                },
                # Authentication Models
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "email": {"type": "string", "format": "email", "example": "john.doe@werent.com"},
                        "first_name": {"type": "string", "example": "John"},
                        "last_name": {"type": "string", "example": "Doe"},
                        "phone": {"type": "string", "example": "+1234567890"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "is_active": {"type": "boolean", "example": True},
                        "is_admin": {"type": "boolean", "example": False}
                    }
                },
                "SignupRequest": {
                    "type": "object",
                    "required": ["email", "password", "first_name", "last_name"],
                    "properties": {
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "john.doe@werent.com",
                            "description": "Valid email address"
                        },
                        "password": {
                            "type": "string",
                            "minLength": 8,
                            "example": "SecurePass123",
                            "description": "Password (min 8 chars, uppercase, lowercase, number)"
                        },
                        "first_name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 50,
                            "example": "John"
                        },
                        "last_name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 50,
                            "example": "Doe"
                        },
                        "phone": {
                            "type": "string",
                            "example": "+1234567890",
                            "description": "Phone number (optional)"
                        }
                    }
                },
                "LoginRequest": {
                    "type": "object",
                    "required": ["email", "password"],
                    "properties": {
                        "email": {"type": "string", "format": "email", "example": "john.doe@werent.com"},
                        "password": {"type": "string", "example": "SecurePass123"}
                    }
                },
                "ProfileUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "minLength": 1, "maxLength": 50, "example": "John"},
                        "last_name": {"type": "string", "minLength": 1, "maxLength": 50, "example": "Doe"},
                        "phone": {"type": "string", "example": "+1234567890"}
                    }
                },
                
                # Gear Management Models (Future)
                "GearItem": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "name": {"type": "string", "example": "Canon EOS R5"},
                        "category": {"type": "string", "example": "camera", "enum": ["camera", "lens", "lighting", "accessory"]},
                        "brand": {"type": "string", "example": "Canon"},
                        "model": {"type": "string", "example": "EOS R5"},
                        "description": {"type": "string", "example": "Professional mirrorless camera with 45MP sensor"},
                        "daily_rate": {"type": "number", "example": 85.00},
                        "weekly_rate": {"type": "number", "example": 500.00},
                        "deposit_amount": {"type": "number", "example": 1000.00},
                        "availability_status": {"type": "string", "example": "available", "enum": ["available", "rented", "maintenance", "unavailable"]},
                        "condition": {"type": "string", "example": "excellent", "enum": ["excellent", "good", "fair", "poor"]},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    }
                },
                "GearCreateRequest": {
                    "type": "object",
                    "required": ["name", "category", "brand", "daily_rate"],
                    "properties": {
                        "name": {"type": "string", "example": "Canon EOS R5"},
                        "category": {"type": "string", "example": "camera", "enum": ["camera", "lens", "lighting", "accessory"]},
                        "brand": {"type": "string", "example": "Canon"},
                        "model": {"type": "string", "example": "EOS R5"},
                        "description": {"type": "string", "example": "Professional mirrorless camera"},
                        "daily_rate": {"type": "number", "example": 85.00},
                        "weekly_rate": {"type": "number", "example": 500.00},
                        "deposit_amount": {"type": "number", "example": 1000.00}
                    }
                },
                
                # Rental System Models (Future)
                "Rental": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "user_id": {"type": "integer", "example": 1},
                        "gear_item_id": {"type": "integer", "example": 1},
                        "start_date": {"type": "string", "format": "date", "example": "2024-01-15"},
                        "end_date": {"type": "string", "format": "date", "example": "2024-01-20"},
                        "total_cost": {"type": "number", "example": 425.00},
                        "deposit_paid": {"type": "number", "example": 1000.00},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    }
                },
                "RentalRequest": {
                    "type": "object",
                    "required": ["gear_item_id", "start_date", "end_date"],
                    "properties": {
                        "gear_item_id": {"type": "integer", "example": 1},
                        "start_date": {"type": "string", "format": "date", "example": "2024-01-15"},
                        "end_date": {"type": "string", "format": "date", "example": "2024-01-20"},
                        "notes": {"type": "string", "example": "Needed for wedding photography"}
                    }
                },
                
                # Review System Models (Future)
                "Review": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "user_id": {"type": "integer", "example": 1},
                        "gear_item_id": {"type": "integer", "example": 1},
                        "rental_id": {"type": "integer", "example": 1},
                        "rating": {"type": "integer", "minimum": 1, "maximum": 5, "example": 5},
                        "comment": {"type": "string", "example": "Excellent camera, perfect condition!"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    }
                },
                "ReviewRequest": {
                    "type": "object",
                    "required": ["rating"],
                    "properties": {
                        "rating": {"type": "integer", "minimum": 1, "maximum": 5, "example": 5},
                        "comment": {"type": "string", "example": "Excellent camera, perfect condition!"}
                    }
                },
                
                # Response Models
                "SignupSuccessResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "User created successfully"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "user": {"$ref": "#/components/schemas/User"}
                            }
                        }
                    }
                },
                "LoginSuccessResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "Login successful"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "user": {"$ref": "#/components/schemas/User"},
                                "access_token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "description": "JWT access token (expires in 15 minutes)"},
                                "refresh_token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "description": "JWT refresh token (expires in 30 days)"}
                            }
                        }
                    }
                },
                "RefreshTokenResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "Access token refreshed successfully"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "access_token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "description": "New JWT access token (expires in 15 minutes)"}
                            }
                        }
                    }
                },
                "ProfileResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "Profile retrieved successfully"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "user": {"$ref": "#/components/schemas/User"}
                            }
                        }
                    }
                },
                "ErrorResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "error": {"type": "string", "example": "Invalid email format"},
                        "error_code": {"type": "string", "example": "VALIDATION_ERROR"},
                        "details": {"type": "object"}
                    }
                },
                "ValidationErrorResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "error": {"type": "string", "example": "Validation failed"},
                        "error_code": {"type": "string", "example": "VALIDATION_ERROR"},
                        "details": {
                            "type": "object",
                            "properties": {
                                "field_errors": {
                                    "type": "object",
                                    "example": {
                                        "email": "Invalid email format",
                                        "password": "Password must be at least 8 characters"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "paths": {
            "/items": {
                "get": {
                    "tags": ["Item"],
                    "summary": "List all available items",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "List of items",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Item"],
                    "summary": "Create a new item (admin only)",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ItemCreateRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Item created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
                                }
                            }
                        },
                        "403": {"description": "Admin access required"}
                    }
                }
            },
            "/items/{item_id}": {
                "get": {
                    "tags": ["Item"],
                    "summary": "Get item details",
                    "security": [{"BearerAuth": []}],
                    "parameters": [{
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }],
                    "responses": {
                        "200": {
                            "description": "Item details",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
                                }
                            }
                        },
                        "404": {"description": "Item not found"}
                    }
                },
                "put": {
                    "tags": ["Item"],
                    "summary": "Update item (admin only)",
                    "security": [{"BearerAuth": []}],
                    "parameters": [{
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ItemUpdateRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Item updated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
                                }
                            }
                        },
                        "403": {"description": "Admin access required"},
                        "404": {"description": "Item not found"}
                    }
                },
                "delete": {
                    "tags": ["Item"],
                    "summary": "Delete item (admin only)",
                    "security": [{"BearerAuth": []}],
                    "parameters": [{
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }],
                    "responses": {
                        "204": {"description": "Item deleted successfully"},
                        "403": {"description": "Admin access required"},
                        "404": {"description": "Item not found"}
                    }
                }
            },
            # Authentication Endpoints
            "/api/auth/signup": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Register a new user account",
                    "description": "Register a new user account with email and password. Does not create JWT session - use login endpoint to authenticate.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SignupRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "User created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SignupSuccessResponse"}
                                }
                            }
                        },
                        "400": {
                            "description": "Bad request",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        },
                        "409": {
                            "description": "Email already registered",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        },
                        "422": {
                            "description": "Validation error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ValidationErrorResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/auth/login": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Authenticate user and return JWT tokens",
                    "description": "Authenticate user with email and password. Returns both access token (15 min expiry) and refresh token (30 day expiry).",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/LoginSuccessResponse"}
                                }
                            }
                        },
                        "400": {
                            "description": "Bad request",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        },
                        "401": {
                            "description": "Unauthorized",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/auth/profile": {
                "get": {
                    "tags": ["Authentication"],
                    "summary": "Get current user's profile",
                    "description": "Retrieve current user's profile information",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Profile retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ProfileResponse"}
                                }
                            }
                        },
                        "401": {
                            "description": "Unauthorized",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        },
                        "404": {
                            "description": "User not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        }
                    }
                },
                "put": {
                    "tags": ["Authentication"],
                    "summary": "Update user profile",
                    "description": "Update current user's profile information",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ProfileUpdateRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Profile updated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ProfileResponse"}
                                }
                            }
                        },
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"},
                        "404": {"description": "User not found"},
                        "422": {"description": "Validation error"}
                    }
                }
            },
            "/api/auth/refresh": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Refresh access token",
                    "description": "Generate a new access token using a valid refresh token. Use this when the access token expires (after 15 minutes).",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Access token refreshed successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/RefreshTokenResponse"}
                                }
                            }
                        },
                        "401": {
                            "description": "Unauthorized - Invalid or expired refresh token",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        },
                        "404": {
                            "description": "User not found",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            }
                        }
                    }
                }
            },
            
            # Future Gear Management Endpoints (Placeholder)
            "/api/gear": {
                "get": {
                    "tags": ["Gear Management"],
                    "summary": "[Coming Soon] List all available gear",
                    "description": "Retrieve a paginated list of all available gear items",
                    "parameters": [
                        {
                            "name": "category",
                            "in": "query",
                            "description": "Filter by gear category",
                            "schema": {"type": "string", "enum": ["camera", "lens", "lighting", "accessory"]}
                        },
                        {
                            "name": "availability_status",
                            "in": "query",
                            "description": "Filter by availability status",
                            "schema": {"type": "string", "enum": ["available", "rented", "maintenance"]}
                        },
                        {
                            "name": "page",
                            "in": "query",
                            "description": "Page number for pagination",
                            "schema": {"type": "integer", "minimum": 1, "default": 1}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "description": "Number of items per page",
                            "schema": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20}
                        }
                    ],
                    "responses": {
                        "200": {"description": "List of gear items"},
                        "400": {"description": "Bad request"}
                    }
                },
                "post": {
                    "tags": ["Gear Management"],
                    "summary": "[Coming Soon] Add new gear item",
                    "description": "Add a new gear item to the inventory (Admin only)",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/GearCreateRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Gear item created successfully"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"},
                        "403": {"description": "Admin access required"}
                    }
                }
            },
            "/api/gear/{gear_id}": {
                "get": {
                    "tags": ["Gear Management"],
                    "summary": "[Coming Soon] Get gear item details",
                    "description": "Retrieve detailed information about a specific gear item",
                    "parameters": [
                        {
                            "name": "gear_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the gear item",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Gear item details"},
                        "404": {"description": "Gear item not found"}
                    }
                }
            },
            
            # Future Rental Management Endpoints (Placeholder)
            "/api/rentals": {
                "get": {
                    "tags": ["Rental System"],
                    "summary": "[Coming Soon] List user's rentals",
                    "description": "Retrieve a list of current user's rental history",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {"description": "List of user rentals"},
                        "401": {"description": "Unauthorized"}
                    }
                },
                "post": {
                    "tags": ["Rental System"],
                    "summary": "[Coming Soon] Create new rental",
                    "description": "Create a new rental booking for gear item",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RentalRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Rental created successfully"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"},
                        "409": {"description": "Gear not available for selected dates"}
                    }
                }
            },
            
            # Future Review System Endpoints (Placeholder)
            "/api/gear/{gear_id}/reviews": {
                "get": {
                    "tags": ["Review System"],
                    "summary": "[Coming Soon] Get gear reviews",
                    "description": "Retrieve reviews for a specific gear item",
                    "parameters": [
                        {
                            "name": "gear_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the gear item",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "List of reviews"},
                        "404": {"description": "Gear item not found"}
                    }
                },
                "post": {
                    "tags": ["Review System"],
                    "summary": "[Coming Soon] Add review for gear",
                    "description": "Add a review for gear item (requires completed rental)",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "gear_id",
                            "in": "path",
                            "required": True,
                            "description": "ID of the gear item",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ReviewRequest"}
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Review added successfully"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"},
                        "403": {"description": "Must complete rental to review"}
                    }
                }
            }
        },
        "tags": [
            {
                "name": "Authentication",
                "description": "User authentication and account management"
            },
            {
                "name": "Gear Management",
                "description": "Camera equipment catalog and inventory (Coming Soon)"
            },
            {
                "name": "Rental System",
                "description": "Equipment booking and rental management (Coming Soon)"
            },
            {
                "name": "Review System",
                "description": "User reviews and ratings (Coming Soon)"
            },
            {
                "name": "Admin",
                "description": "Administrative endpoints (Coming Soon)"
            }
        ]
    }


@swagger_bp.route('/')
def swagger_ui():
    """Render Swagger UI page."""
    swagger_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WeRent API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui.css" />
        <style>
            html {
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }
            *, *:before, *:after {
                box-sizing: inherit;
            }
            body {
                margin:0;
                background: #fafafa;
            }
            .swagger-ui .topbar {
                background-color: #1f2937;
                border-bottom: 1px solid #374151;
            }
            .swagger-ui .topbar .topbar-wrapper .link {
                content: '';
            }
            .swagger-ui .topbar .topbar-wrapper .link:after {
                content: 'WeRent API Documentation';
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
            }
            .swagger-ui .info {
                margin: 50px 0;
            }
            .swagger-ui .info .title {
                font-size: 36px;
                color: #1f2937;
            }
            .swagger-ui .scheme-container {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: '{{ url_for("swagger.openapi_spec") }}',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout",
                    tryItOutEnabled: true,
                    supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                    docExpansion: 'list',
                    defaultModelExpandDepth: 3,
                    defaultModelsExpandDepth: 3,
                    showExtensions: true,
                    showCommonExtensions: true,
                    onComplete: function() {
                        console.log('Swagger UI loaded successfully');
                        
                        // Add custom styling for coming soon endpoints
                        setTimeout(() => {
                            document.querySelectorAll('.opblock-summary-description').forEach(el => {
                                if (el.textContent.includes('[Coming Soon]')) {
                                    el.closest('.opblock').style.opacity = '0.6';
                                    el.closest('.opblock').style.borderLeft = '4px solid #f59e0b';
                                }
                            });
                        }, 1000);
                    },
                    onFailure: function(data) {
                        console.error('Failed to load Swagger UI', data);
                    }
                });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(swagger_html)


@swagger_bp.route('/openapi.json')
def openapi_spec():
    """Return OpenAPI specification as JSON."""
    return jsonify(get_openapi_spec())


@swagger_bp.route('/redoc')
def redoc():
    """Render ReDoc documentation page."""
    redoc_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WeRent API Documentation - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body { 
                margin: 0; 
                padding: 0; 
                font-family: 'Roboto', sans-serif;
            }
            redoc {
                display: block;
            }
        </style>
    </head>
    <body>
        <redoc spec-url='{{ url_for("swagger.openapi_spec") }}' theme='{"colors": {"primary": {"main": "#1f2937"}}}'></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@2.1.2/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    return render_template_string(redoc_html)


@swagger_bp.route('/postman')
def postman_collection():
    """Generate Postman collection for API testing."""
    spec = get_openapi_spec()
    
    collection = {
        "info": {
            "name": "WeRent Backend API",
            "description": spec["info"]["description"],
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "variable": [
            {
                "key": "baseUrl",
                "value": "https://werent-backend-api.onrender.com" if os.environ.get('FLASK_ENV') == 'production' else "http://localhost:5000",
                "type": "string"
            },
            {
                "key": "accessToken",
                "value": "",
                "type": "string"
            },
            {
                "key": "refreshToken",
                "value": "",
                "type": "string"
            }
        ],
        "item": [
            {
                "name": "Authentication",
                "item": [
                    {
                        "name": "Register User",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "email": "test@werent.com",
                                    "password": "SecurePass123",
                                    "first_name": "Test",
                                    "last_name": "User",
                                    "phone": "+1234567890"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{baseUrl}}/api/auth/signup",
                                "host": ["{{baseUrl}}"],
                                "path": ["api", "auth", "signup"]
                            }
                        }
                    },
                    {
                        "name": "Login User",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "email": "test@werent.com",
                                    "password": "SecurePass123"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{baseUrl}}/api/auth/login",
                                "host": ["{{baseUrl}}"],
                                "path": ["api", "auth", "login"]
                            }
                        },
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "exec": [
                                        "if (pm.response.code === 200) {",
                                        "    const response = pm.response.json();",
                                        "    pm.collectionVariables.set('accessToken', response.data.access_token);",
                                        "    pm.collectionVariables.set('refreshToken', response.data.refresh_token);",
                                        "}"
                                    ]
                                }
                            }
                        ]
                    },
                    {
                        "name": "Get Profile",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{accessToken}}"
                                }
                            ],
                            "url": {
                                "raw": "{{baseUrl}}/api/auth/profile",
                                "host": ["{{baseUrl}}"],
                                "path": ["api", "auth", "profile"]
                            }
                        }
                    },
                    {
                        "name": "Refresh Access Token",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Authorization",
                                    "value": "Bearer {{refreshToken}}"
                                }
                            ],
                            "url": {
                                "raw": "{{baseUrl}}/api/auth/refresh",
                                "host": ["{{baseUrl}}"],
                                "path": ["api", "auth", "refresh"]
                            }
                        },
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "exec": [
                                        "if (pm.response.code === 200) {",
                                        "    const response = pm.response.json();",
                                        "    pm.collectionVariables.set('accessToken', response.data.access_token);",
                                        "}"
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return jsonify(collection)
