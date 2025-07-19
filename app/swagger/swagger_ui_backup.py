"""
Swagger UI integration for CamRent Backend API.
Provides interactive API documentation using OpenAPI 3.0 specification.
"""

from flask import Blueprint, render_template_string, jsonify, url_for
import json

# Create Swagger blueprint
swagger_bp = Blueprint('swagger', __name__, url_prefix='/docs')

# OpenAPI 3.0 specification
def get_openapi_spec():
    """Generate OpenAPI 3.0 specification for the API."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "CamRent Backend API",
            "version": "1.0.0",
            "description": """
# CamRent Backend API Documentation

A comprehensive camera and photography equipment rental platform backend service.

## Features
- **Authentication**: JWT-based user authentication and authorization
- **User Management**: User registration, login, and profile management
- **Gear Management**: Camera equipment catalog and inventory (Coming Soon)
- **Rental System**: Equipment booking and rental management (Coming Soon)
- **Review System**: User reviews and ratings (Coming Soon)
- **Admin Panel**: Administrative features for managing the platform (Coming Soon)

## Authentication
Most endpoints require authentication. Use the `/api/auth/login` endpoint to obtain a JWT token,
then include it in the `Authorization` header as `Bearer <token>`.

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
1. Register a new user account using `/api/auth/signup`
2. Login to receive a JWT token using `/api/auth/login`
3. Include the token in subsequent requests: `Authorization: Bearer <token>`
4. Explore the available endpoints below

## Development Status
- ✅ **Authentication System**: Fully implemented
- 🚧 **Gear Management**: In development
- 🚧 **Rental System**: Planning phase
- 🚧 **Review System**: Planning phase
- 🚧 **Admin Panel**: Planning phase

For the latest development status, see the [PROJECT_STATUS.md](https://github.com/camrent/backend/blob/main/PROJECT_STATUS.md) file.
            """,
            "contact": {
                "name": "CamRent Development Team",
                "email": "dev@camrent.com"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "servers": [
            {
                "url": "http://localhost:5000",
                "description": "Development server"
            },
            {
                "url": "https://api.camrent.com",
                "description": "Production server (when deployed)"
            }
        ],
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
                # Authentication Models
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "email": {"type": "string", "format": "email", "example": "john.doe@camrent.com"},
                        "first_name": {"type": "string", "example": "John"},
                        "last_name": {"type": "string", "example": "Doe"},
                        "phone": {"type": "string", "example": "+1234567890"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "is_active": {"type": "boolean", "example": True},
                        "is_admin": {"type": "boolean", "example": False}
                    }
                },
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "is_active": {"type": "boolean", "example": True}
                    }
                },
                "SignupRequest": {
                    "type": "object",
                    "required": ["email", "password", "first_name", "last_name"],
                    "properties": {
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "john.doe@camrent.com",
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
                        "email": {"type": "string", "format": "email", "example": "john.doe@camrent.com"},
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
                "AuthSuccessResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "Login successful"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "user": {"$ref": "#/components/schemas/User"},
                                "access_token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
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
            "/api/auth/signup": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Register a new user account",
                    "description": "Register a new user account with email and password",
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
                                    "schema": {"$ref": "#/components/schemas/AuthSuccessResponse"}
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
                    "summary": "Authenticate user and return JWT token",
                    "description": "Authenticate user with email and password",
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
                                    "schema": {"$ref": "#/components/schemas/AuthSuccessResponse"}
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
            "/api/auth/logout": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Logout user",
                    "description": "Logout current user session",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Logout successful",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean", "example": True},
                                            "message": {"type": "string", "example": "Logout successful"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {"description": "Unauthorized"}
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
        <title>CamRent API Documentation</title>
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
                content: 'CamRent API Documentation';
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
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
                    onComplete: function() {
                        console.log('Swagger UI loaded successfully');
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
        <title>CamRent API Documentation - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <redoc spec-url='{{ url_for("swagger.openapi_spec") }}'></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@2.1.2/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    return render_template_string(redoc_html)
