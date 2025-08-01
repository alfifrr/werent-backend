"""
API paths definition for WeRent Backend API.
Contains all endpoint paths and their OpenAPI specifications.
"""


def get_health_paths():
    """Get health check paths."""
    return {
        "/api/health": {
            "get": {
                "tags": ["Health"],
                "summary": "Basic health check",
                "description": "Check service status and basic connectivity",
                "responses": {
                    "200": {
                        "description": "Service is healthy",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/HealthResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/health/detailed": {
            "get": {
                "tags": ["Health"],
                "summary": "Detailed health check",
                "description": "Detailed system information including database version and environment details",
                "responses": {
                    "200": {
                        "description": "Detailed system information",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/DetailedHealthResponse"}
                            }
                        }
                    }
                }
            }
        }
    }


def get_item_paths():
    """Get item management paths."""
    return {
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
                                    "items": {"$ref": "#/components/schemas/Item"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Item"],
                "summary": "Create a new item (admin only)",
                "description": "Create a new rental item. Only administrators can create items. Product codes must be unique across all items.",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ItemCreateRequest"
                            }
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Item created successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                    },
                    "400": {
                        "description": "Bad request - validation error or constraint violation",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                                "examples": {
                                    "duplicate_product_code": {
                                        "summary": "Duplicate product code",
                                        "value": {
                                            "success": False,
                                            "error": "Product code already exists. Please use a unique product code."
                                        }
                                    },
                                    "invalid_enum": {
                                        "summary": "Invalid enum value",
                                        "value": {
                                            "success": False,
                                            "error": "'INVALID_TYPE' is not among the defined enum values. Enum name: itemtype. Possible values: DRESS, TOP, BOTTOM, ..., OTHER",
                                            "error_code": "INTERNAL_ERROR"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Authentication required"},
                    "403": {"description": "Admin access required"},
                    "500": {
                        "description": "Internal server error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                },
            },
        },
        "/items/{item_id}": {
            "get": {
                "tags": ["Item"],
                "summary": "Get item details",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Item details",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                    },
                    "404": {"description": "Item not found"},
                },
            },
            "put": {
                "tags": ["Item"],
                "summary": "Update item (admin only)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ItemUpdateRequest"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Item updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                    },
                    "403": {"description": "Admin access required"},
                    "404": {"description": "Item not found"},
                },
            },
            "delete": {
                "tags": ["Item"],
                "summary": "Delete item (admin only)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "204": {"description": "Item deleted successfully"},
                    "403": {"description": "Admin access required"},
                    "404": {"description": "Item not found"},
                },
            },
        },
    }


def get_auth_paths():
    """Get authentication paths."""
    return {
        "/api/auth/signup": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Register a new user account",
                "description": "Register a new user account with email and password. Sends verification email automatically. Account must be verified before login is possible.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/SignupRequest"}
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "User created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/SignupSuccessResponse"
                                }
                            }
                        },
                    },
                    "400": {
                        "description": "Bad request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        },
                    },
                    "409": {
                        "description": "User already exists",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        },
                    },
                    "422": {
                        "description": "Validation error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ValidationErrorResponse"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/auth/login": {
            "post": {
                "tags": ["Authentication"],
                "summary": "User login",
                "description": "Authenticate user with email and password. Returns both access and refresh tokens.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/LoginSuccessResponse"
                                }
                            }
                        },
                    },
                    "401": {
                        "description": "Invalid credentials",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        },
                    },
                    "422": {
                        "description": "Validation error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/auth/profile": {
            "get": {
                "tags": ["Authentication"],
                "summary": "Get user profile",
                "description": "Retrieve the authenticated user's profile information.",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Profile retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ProfileResponse"
                                }
                            }
                        },
                    },
                    "401": {
                        "description": "Unauthorized",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        },
                    },
                },
            },
            "put": {
                "tags": ["Authentication"],
                "summary": "Update user profile",
                "description": "Update the authenticated user's profile information. If the profile image is an empty string or None, it will delete any pre-existing profile image.",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ProfileUpdateRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Profile updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ProfileResponse"
                                }
                            }
                        },
                    },
                    "401": {"description": "Unauthorized"},
                    "422": {"description": "Validation error"},
                },
            },
        },
        "/api/auth/verify-email/{uuid}": {
            "get": {
                "tags": ["Authentication"],
                "summary": "Verify user email address using UUID",
                "description": "Verify user email address using UUID from verification email.\n\n**Process:**\n1. User receives verification email after registration\n2. Email contains a unique verification link with UUID\n3. User clicks the link to verify their account\n4. Account is marked as verified in the system\n5. Welcome email is sent upon successful verification\n\n**UUID Requirements:**\n- Must be a valid UUID from the verification email\n- UUID is unique to each user account\n- Links do not expire (but you can implement expiration if needed)\n\n**Success Response:**\n- User account is marked as verified\n- Welcome email is automatically sent\n- Returns verification status and success message\n\n**Error Scenarios:**\n- Invalid or non-existent UUID\n- Account already verified\n- Technical errors during verification\n\n**Security Notes:**\n- UUIDs are cryptographically secure\n- One-time verification (subsequent clicks are harmless)\n- No authentication required for this endpoint",
                "parameters": [
                    {
                        "name": "uuid",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "format": "uuid"
                        },
                        "description": "Unique verification UUID from email",
                        "example": "550e8400-e29b-41d4-a716-446655440000"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Email verified successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/EmailVerificationResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid UUID format",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Invalid or expired verification link",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/auth/resend-verification": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Resend verification email to current user",
                "description": "Resend email verification link to the authenticated user's email address.\n\n**Authentication Required:**\n- Must be logged in with valid JWT token\n- Only sends verification email to the authenticated user's account\n\n**Use Cases:**\n- User didn't receive original verification email\n- Original verification email was deleted/lost\n- User wants a fresh verification link\n\n**Process:**\n1. Authenticate user with JWT token\n2. Check if current user's account is unverified\n3. Verify account is active (not deactivated)\n4. Send verification email to user's registered email\n5. Return status of email sending operation\n\n**Email Content:**\n- Professional welcome message\n- Clear verification instructions\n- Clickable verification button/link\n- Fallback text link for compatibility\n- Security note about link validity\n\n**Success Response:**\n- Confirmation that email was sent\n- User should check their inbox/spam folder\n\n**Error Scenarios:**\n- User not authenticated (no JWT token)\n- Account already verified\n- Account deactivated\n- Email sending technical failure\n\n**Security Benefits:**\n- Prevents email enumeration attacks\n- Users can only request verification for their own account\n- Rate limiting applies per authenticated user",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Verification email sent successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ResendVerificationResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Account already verified",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - no valid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "403": {
                        "description": "Account deactivated",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "User not found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Failed to send email",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/auth/refresh": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Refresh access token",
                "description": "Get a new access token using a valid refresh token.\n\n**Purpose:**\n- Allows users to obtain a new access token when their current one expires\n- Prevents the need to re-login when access token expires\n- Maintains user session security with short-lived access tokens\n\n**Two Methods Supported:**\n\n**Method 1: Authorization Header (Recommended)**\n```\nPOST /api/auth/refresh\nAuthorization: Bearer <refresh_token>\n```\n\n**Method 2: Request Body**\n```\nPOST /api/auth/refresh\nContent-Type: application/json\n\n{\n  \"refresh_token\": \"<refresh_token>\"\n}\n```\n\n**Process:**\n1. Client sends refresh token using either method above\n2. Server validates the refresh token\n3. If valid, server issues a new access token\n4. Original refresh token remains valid until its expiration\n\n**Security Considerations:**\n- Refresh tokens have longer lifespan (30 days)\n- Access tokens have short lifespan (15 minutes)\n- Refresh tokens can be revoked server-side if needed\n\n**Error Scenarios:**\n- Invalid refresh token\n- Expired refresh token\n- Revoked refresh token\n- User account deactivated",
                "security": [],
                "requestBody": {
                    "description": "Method 2: Send refresh token in request body (alternative to Authorization header)",
                    "required": False,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "refresh_token": {
                                        "type": "string",
                                        "description": "JWT refresh token obtained from login",
                                        "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MzkyODY2MCwianRpIjoiODcyMDhkMjgtNDU3MS00YTYzLTkyYWQtYzdhNjUyNjVmMDc0IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzUzOTI4NjYwLCJjc3JmIjoiNTJhMWY1NjktY2E1Ni00YTBkLWE1NTAtNzg5OTYwOGQ1YzFlIiwiZXhwIjoxNzU2NTIwNjYwfQ.LDvURVLfWFRb61QTCdjhSEBJlbuPnipvMmomaacMUoE"
                                    }
                                },
                                "required": ["refresh_token"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Access token refreshed successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/RefreshTokenResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid refresh token format",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Invalid, expired or revoked refresh token",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
    }


def get_admin_paths():
    """Get admin management paths."""
    return {
        "/api/admin/users": {
            "get": {
                "tags": ["Admin"],
                "summary": "List all admin users",
                "description": "Retrieve a list of all users with admin privileges. Admin status changes are managed via manual database operations. Requires admin authentication.",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Admin users retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "Admin users retrieved successfully"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "admins": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "integer", "example": 1},
                                                            "email": {"type": "string", "example": "admin@example.com"},
                                                            "first_name": {"type": "string", "example": "Admin"},
                                                            "last_name": {"type": "string", "example": "User"},
                                                            "phone_number": {"type": "string", "example": "+1234567890"},
                                                            "created_at": {"type": "string", "format": "date-time"},
                                                            "updated_at": {"type": "string", "format": "date-time"}
                                                        }
                                                    }
                                                },
                                                "total_count": {"type": "integer", "example": 5}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Authentication required"},
                    "403": {"description": "Admin access required"}
                }
            }
        },
        "/api/admin/users/{admin_id}": {
            "get": {
                "tags": ["Admin"],
                "summary": "Get admin user details",
                "description": "Retrieve detailed information about a specific admin user by ID. Requires admin authentication.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "admin_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the admin user to retrieve",
                        "example": 1
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Admin user details retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "Admin user retrieved successfully"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "admin": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {"type": "integer", "example": 1},
                                                        "email": {"type": "string", "example": "admin@example.com"},
                                                        "first_name": {"type": "string", "example": "Admin"},
                                                        "last_name": {"type": "string", "example": "User"},
                                                        "phone_number": {"type": "string", "example": "+1234567890"},
                                                        "created_at": {"type": "string", "format": "date-time"},
                                                        "updated_at": {"type": "string", "format": "date-time"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {"description": "Authentication required"},
                    "403": {"description": "Admin access required"},
                    "404": {"description": "Admin user not found"}
                }
            }
        },
    }


def get_statistics_paths():
    """Get admin statistics dashboard paths."""
    return {
        "/api/admin/statistics/": {
            "get": {
                "tags": ["Admin", "Statistics"],
                "summary": "Get admin dashboard statistics",
                "description": "Retrieve total and weekly statistics for users, items, bookings, revenue, reviews, and tickets. Admin access only.",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Admin statistics fetched successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AdminStatisticsResponse"}
                            }
                        }
                    },
                    "401": {"description": "Authentication required"},
                    "403": {"description": "Admin access required"}
                }
            }
        },
        "/api/admin/statistics/monthly": {
            "post": {
                "tags": ["Admin", "Statistics"],
                "summary": "Get monthly admin dashboard statistics",
                "description": "Retrieve monthly statistics for users, items, bookings, revenue, reviews, and tickets for a given year. Admin access only.",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "year": {"type": "integer", "example": 2024}
                                },
                                "required": ["year"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Monthly statistics fetched successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AdminMonthlyStatisticsResponse"}
                            }
                        }
                    },
                    "400": {"description": "Missing or invalid 'year' in request body"},
                    "401": {"description": "Authentication required"},
                    "403": {"description": "Admin access required"}
                }
            }
        }
    }

def get_review_paths():
    """Get review and testimonial paths."""
    return {
        "/testimonial": {
            "get": {
                "tags": ["Review System"],
                "summary": "Get testimonials",
                "description": "Get all reviews to display as testimonials",
                "responses": {
                    "200": {
                        "description": "List of testimonials retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Review"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "/items/{item_id}/reviews": {
            "get": {
                "tags": ["Review System"],
                "summary": "List reviews for an item",
                "description": "Get all reviews for a specific item",
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the item to get reviews for"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Reviews retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Review"}
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Item not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Review System"],
                "summary": "Create a review",
                "description": "Create a new review for an item (requires authentication)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the item to review"
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
                    "201": {
                        "description": "Review created successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Review"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data"
                    },
                    "401": {
                        "description": "Authentication required"
                    },
                    "404": {
                        "description": "Item not found"
                    }
                }
            }
        },
        "/reviews/{review_id}": {
            "put": {
                "tags": ["Review System"],
                "summary": "Update a review",
                "description": "Update an existing review (owner only)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "review_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the review to update"
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
                    "200": {
                        "description": "Review updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Review"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data"
                    },
                    "401": {
                        "description": "Authentication required"
                    },
                    "403": {
                        "description": "Not authorized to update this review"
                    },
                    "404": {
                        "description": "Review not found"
                    }
                }
            },
            "delete": {
                "tags": ["Review System"],
                "summary": "Delete a review",
                "description": "Delete an existing review (owner only)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "review_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the review to delete"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Review deleted successfully"
                    },
                    "401": {
                        "description": "Authentication required"
                    },
                    "403": {
                        "description": "Not authorized to delete this review"
                    },
                    "404": {
                        "description": "Review not found"
                    }
                }
            }
        }
    }


def get_payment_paths():
    """Get payment management paths."""
    return {
        "/payments": {
            "get": {
                "tags": ["Payment"],
                "summary": "List all payments",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "List of payments",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Payment"}
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Payment"],
                "summary": "Create a new payment",
                "description": "Create a payment record. Payment type affects booking status: RENT payments set status to PAID, FINE payments set status to RETURNED (both keep is_paid=true).",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PaymentCreateRequest"}
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Payment created successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Payment"}
                            }
                        },
                    },
                    "400": {"description": "Invalid input"},
                },
            },
        },
        "/payments/user/{user_id}": {
            "get": {
                "tags": ["Payment"],
                "summary": "List all payments for a specific user",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the user to get payments for"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "List of payments for the user",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Payment"}
                                }
                            }
                        },
                    },
                    "404": {"description": "User not found or no payments"},
                },
            }
        },
        "/payments/{payment_id}": {
            "get": {
                "tags": ["Payment"],
                "summary": "Get payment by ID",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "payment_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Payment details",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Payment"}
                            }
                        },
                    },
                    "404": {"description": "Payment not found"},
                },
            },
            "put": {
                "tags": ["Payment"],
                "summary": "Update payment",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "payment_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PaymentUpdateRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Payment updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Payment"}
                            }
                        },
                    },
                    "404": {"description": "Payment not found"},
                },
            },
            "delete": {
                "tags": ["Payment"],
                "summary": "Delete payment",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "payment_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {"description": "Payment deleted"},
                    "404": {"description": "Payment not found"},
                },
            },
        },
    }


def get_ticketing_paths():
    """
    Get ticketing system paths with comprehensive role-based access control.
    
    SECURITY OVERVIEW:
    =================
    The ticketing system implements strict role-based authorization:
    
    👤 REGULAR USERS can:
    - Create tickets for themselves
    - View their own tickets only  
    - Add messages to their own tickets only
    - Reopen their own resolved tickets
    
    🔒 ADMIN USERS can:
    - All user permissions above
    - View ANY ticket system-wide
    - Access admin-only endpoints (/open, /resolved, /stats)
    - Resolve any ticket
    - Add messages to any ticket
    - Reopen any ticket
    - View tickets for any user
    
    🚫 BLOCKED ACTIONS for regular users:
    - Accessing other users' tickets (403 Forbidden)
    - Viewing system-wide ticket lists (403 Forbidden)
    - Resolving tickets (403 Forbidden)
    - Accessing ticket statistics (403 Forbidden)
    
    All endpoints require JWT Bearer authentication.
    Authorization is enforced at the controller level with proper error responses.
    """
    return {
        "/api/tickets": {
            "post": {
                "tags": ["Ticketing"],
                "summary": "Create a new support ticket",
                "description": """
                Create a new support ticket for assistance or reporting issues.
                
                **Authorization Rules:**
                - **Users**: ✅ Can create tickets for themselves
                - **Admins**: ✅ Can create tickets for themselves
                
                **Security**: JWT Bearer token required. User ID is automatically extracted from JWT token for security.
                
                **Note**: The user_id field in the request body will be ignored and overridden with the authenticated user's ID.
                """,
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/TicketCreateRequest"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Ticket created successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data or validation error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}": {
            "get": {
                "tags": ["Ticketing"],
                "summary": "Get a specific ticket",
                "description": """
                Retrieve details of a specific ticket by ID.
                
                **Authorization Rules:**
                - **Users**: Can only view tickets they created
                - **Admins**: Can view any ticket
                
                **Security**: JWT Bearer token required with role-based access control.
                """,
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "ticket_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the ticket to retrieve"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Ticket retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid ticket ID format",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Access denied - Can only view own tickets (unless admin)",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "Ticket not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}/message": {
            "post": {
                "tags": ["Ticketing"],
                "summary": "Add message to ticket conversation",
                "description": """
                Add a new message to an existing ticket's conversation history.
                
                **Authorization Rules:**
                - **Users**: Can only add messages to their own tickets
                - **Admins**: Can add messages to any ticket
                
                **Security**: JWT Bearer token required with ownership or admin validation.
                **Note**: Messages are timestamped and appended to the ticket's chat history.
                """,
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "ticket_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the ticket to add message to"
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/TicketMessageRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Message added successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data or ticket ID format",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Access denied - Can only add messages to own tickets (unless admin)",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "Ticket not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}/resolve": {
            "patch": {
                "tags": ["Ticketing"],
                "summary": "Resolve a ticket (Admin Only)",
                "description": """
                Mark a ticket as resolved and close it.
                
                **Authorization Rules:**
                - **Users**: ❌ Cannot resolve tickets
                - **Admins**: ✅ Can resolve any ticket
                
                **Security**: JWT Bearer token required with admin privileges.
                """,
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "ticket_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the ticket to resolve"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Ticket resolved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid ticket ID or ticket cannot be resolved",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Admin access required - Only administrators can resolve tickets",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "Ticket not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}/reopen": {
            "patch": {
                "tags": ["Ticketing"],
                "summary": "Reopen a resolved ticket",
                "description": """
                Reopen a previously resolved ticket for further assistance.
                
                **Authorization Rules:**
                - **Users**: Can only reopen their own tickets
                - **Admins**: Can reopen any ticket
                
                **Security**: JWT Bearer token required with ownership or admin validation.
                """,
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "ticket_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the ticket to reopen"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Ticket reopened successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid ticket ID or ticket cannot be reopened",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Access denied - Can only reopen own tickets (unless admin)",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "Ticket not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/user/{user_id}": {
            "get": {
                "tags": ["Ticketing"],
                "summary": "Get all tickets for a specific user",
                "description": """
                Retrieve all support tickets created by a specific user.
                
                **Authorization Rules:**
                - **Users**: Can only get their own tickets (user_id must match JWT identity)
                - **Admins**: Can get tickets for any user
                
                **Security**: JWT Bearer token required with user identity or admin validation.
                """,
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the user to get tickets for"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User tickets retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid user ID format",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Access denied - Can only access own data (unless admin)",
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
        "/api/tickets/open": {
            "get": {
                "tags": ["Ticketing"],
                "summary": "Get all open tickets (Admin Only)",
                "description": """
                Retrieve all open (unresolved) support tickets across all users for admin management.
                
                **Authorization Rules:**
                - **Users**: ❌ Cannot access (403 Forbidden)
                - **Admins**: ✅ Can view all open tickets system-wide
                
                **Security**: JWT Bearer token required with admin privileges.
                **Use Case**: Admin dashboard for ticket management and support overview.
                """,
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Open tickets retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Admin access required - Only administrators can view all tickets",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/resolved": {
            "get": {
                "tags": ["Ticketing"],
                "summary": "Get all resolved tickets (Admin Only)",
                "description": """
                Retrieve all resolved (closed) support tickets across all users for admin analysis.
                
                **Authorization Rules:**
                - **Users**: ❌ Cannot access (403 Forbidden)
                - **Admins**: ✅ Can view all resolved tickets system-wide
                
                **Security**: JWT Bearer token required with admin privileges.
                **Use Case**: Admin reports, performance analysis, and historical ticket review.
                """,
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Resolved tickets retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Admin access required - Only administrators can view all tickets",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/stats": {
            "get": {
                "tags": ["Ticketing"],
                "summary": "Get ticket statistics (Admin Only)",
                "description": """
                Retrieve comprehensive ticket statistics for admin dashboard and reporting.
                
                **Authorization Rules:**
                - **Users**: ❌ Cannot access (403 Forbidden)
                - **Admins**: ✅ Can view system-wide ticket statistics
                
                **Security**: JWT Bearer token required with admin privileges.
                
                **Response Data:**
                - Total ticket count across all users
                - Open (unresolved) ticket count
                - Resolved ticket count
                
                **Use Case**: Admin dashboard metrics, performance monitoring, and support analytics.
                """,
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Ticket statistics retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TicketStatsResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication required - Missing or invalid JWT token",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "403": {
                        "description": "Admin access required - Only administrators can view ticket statistics",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        }
    }


def get_booking_paths():
    """Get booking management paths."""
    return {
        "/bookings": {
            "get": {
                "tags": ["Booking"],
                "summary": "List all bookings in the system",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "List of all bookings",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Booking"}
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Booking"],
                "summary": "Create a new booking",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/BookingCreateRequest"}
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Booking created successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Booking"}
                            }
                        },
                    },
                    "400": {"description": "Item not available, not found, or user not verified"},
                },
            },
        },
        "/bookings/user/{user_id}": {
            "get": {
                "tags": ["Booking"],
                "summary": "List all bookings for a specific user",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "user_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID of the user to get bookings for"}
                ],
                "responses": {
                    "200": {
                        "description": "List of bookings for the user",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Booking"}
                                }
                            }
                        },
                    },
                    "404": {"description": "User not found or no bookings"},
                },
            }
        },
        "/bookings/{booking_id}": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get booking by ID (owner or admin only)",
                "description": "Get booking details. Only the booking owner or admin can access.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "booking_id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {
                        "description": "Booking details",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Booking"}
                            }
                        },
                    },
                    "403": {"description": "Access denied - not owner or admin"},
                    "404": {"description": "Booking not found"},
                },
            },
            "put": {
                "tags": ["Booking"],
                "summary": "Update booking (owner or admin only)",
                "description": "Update booking details. Only the booking owner or admin can modify. The booking status will follow this flow: \n1. PENDING (when booking created) \n2. PAID (changed after payment creation) \n3. CONFIRMED (Manually changed by admin in admin dashboard) \n4. RETURNED (Manually changed by renter in user dashboard) \n5. COMPLETED (manually changed by admin in admin dashboard) \n\nThe booking can also be cancelled at any time by the booking owner, in which case the booking status will be changed to CANCELLED. \n\nThe booking can also be cancelled by the admin in the admin dashboard from PENDING to CANCELLED or from CONFIRMED to CANCELLED.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "booking_id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/BookingStatusUpdate"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Booking updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Booking"}
                            }
                        },
                    },
                    "403": {"description": "Access denied - not owner or admin"},
                    "404": {"description": "Booking not found or invalid update"},
                },
            },
        },
        "/bookings/availability": {
            "get": {
                "tags": ["Booking"],
                "summary": "Check item availability",
                "description": "Check if an item is available for booking in a specific date range. Public endpoint - no authentication required.",
                "parameters": [
                    {"name": "item_id", "in": "query", "required": True, "schema": {"type": "integer"}, "description": "ID of the item to check"},
                    {"name": "start_date", "in": "query", "required": True, "schema": {"type": "string", "format": "date"}, "description": "Start date (YYYY-MM-DD)"},
                    {"name": "end_date", "in": "query", "required": True, "schema": {"type": "string", "format": "date"}, "description": "End date (YYYY-MM-DD)"},
                    {"name": "quantity", "in": "query", "required": False, "schema": {"type": "integer", "default": 1}, "description": "Quantity needed (default: 1)"}
                ],
                "responses": {
                    "200": {
                        "description": "Availability information with quantity details",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "available": {"type": "boolean", "description": "Whether item is available"},
                                        "available_quantity": {"type": "integer", "description": "Available quantity"},
                                        "total_quantity": {"type": "integer", "description": "Total item quantity"},
                                        "requested_quantity": {"type": "integer", "description": "Requested quantity"},
                                        "can_fulfill": {"type": "boolean", "description": "Can fulfill the request"},
                                        "confirmed_reserved": {"type": "integer", "description": "Quantity reserved by confirmed bookings"},
                                        "pending_reserved": {"type": "integer", "description": "Quantity reserved by pending bookings"},
                                        "date_range": {
                                            "type": "object",
                                            "properties": {
                                                "start_date": {"type": "string", "format": "date"},
                                                "end_date": {"type": "string", "format": "date"}
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    },
                    "400": {"description": "Missing required parameters or invalid date format"},
                },
            },
        },
        "/bookings/availability/calendar": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get availability calendar",
                "description": "Get a calendar view of item availability for a date range. Public endpoint - no authentication required.",
                "parameters": [
                    {"name": "item_id", "in": "query", "required": True, "schema": {"type": "integer"}, "description": "ID of the item"},
                    {"name": "start_date", "in": "query", "required": True, "schema": {"type": "string", "format": "date"}, "description": "Start date (YYYY-MM-DD)"},
                    {"name": "end_date", "in": "query", "required": True, "schema": {"type": "string", "format": "date"}, "description": "End date (YYYY-MM-DD)"}
                ],
                "responses": {
                    "200": {
                        "description": "Calendar availability data by date",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "calendar": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "type": "object",
                                                "properties": {
                                                    "date": {"type": "string", "format": "date"},
                                                    "available": {"type": "boolean"},
                                                    "available_quantity": {"type": "integer"},
                                                    "total_quantity": {"type": "integer"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    },
                    "400": {"description": "Missing required parameters or invalid date format"},
                },
            },
        },
        "/bookings/{booking_id}/cancel": {
            "post": {
                "tags": ["Booking"],
                "summary": "Cancel booking",
                "description": "Cancel a booking with RBAC controls. Users can cancel PENDING/CONFIRMED bookings, admins have broader privileges. Industry best practice dedicated endpoint.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "booking_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID of the booking to cancel"}
                ],
                "responses": {
                    "200": {
                        "description": "Booking cancelled successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "Booking cancelled successfully. Status changed from PENDING to CANCELLED."},
                                        "data": {
                                            "allOf": [
                                                {"$ref": "#/components/schemas/Booking"},
                                                {
                                                    "type": "object",
                                                    "properties": {
                                                        "refund_info": {
                                                            "type": "object",
                                                            "properties": {
                                                                "cancellation_reason": {"type": "string", "example": "User requested"},
                                                                "cancelled_at": {"type": "string", "format": "date-time"},
                                                                "original_total": {"type": "number", "example": 108.0},
                                                                "refund_eligible": {"type": "boolean", "example": True},
                                                                "refund_amount": {"type": "number", "example": 108.0}
                                                            }
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        },
                    },
                    "400": {"description": "Booking already cancelled"},
                    "403": {"description": "Cannot cancel this booking status - contact support"},
                    "404": {"description": "Booking not found"},
                },
            },
        },
        "/bookings/{booking_id}/finish": {
            "put": {
                "tags": ["Booking"],
                "summary": "Finish booking",
                "description": "Finish a booking by changing status from CONFIRMED to RETURNED. Users can only finish their own CONFIRMED bookings, admins can finish any CONFIRMED booking.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "booking_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID of the booking to finish"}
                ],
                "responses": {
                    "200": {
                        "description": "Booking finished successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "Booking finished successfully"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "booking": {"$ref": "#/components/schemas/Booking"},
                                                "finished_at": {"type": "string", "format": "date-time", "example": "2025-08-01T09:24:32.875708"},
                                                "previous_status": {"type": "string", "example": "CONFIRMED"},
                                                "new_status": {"type": "string", "example": "RETURNED"}
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    },
                    "400": {"description": "Cannot finish booking - invalid status or booking already returned"},
                    "401": {"description": "Authentication required"},
                    "403": {"description": "Access denied - not booking owner or admin"},
                    "404": {"description": "Booking not found"},
                },
            },
        },
        "/bookings/status/{status}": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get bookings by status",
                "description": "Get all bookings with a specific status.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "status", 
                        "in": "path", 
                        "required": True, 
                        "schema": {
                            "type": "string",
                            "enum": ["pending", "paid", "pastdue", "returned", "confirmed", "cancelled", "completed"]
                        },
                        "description": "Booking status to filter by"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "List of bookings with specified status",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Booking"}
                                }
                            }
                        },
                    }
                },
            },
        },
        "/bookings/history": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get booking history",
                "description": "Get booking history for the current user with optional limit.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "limit", 
                        "in": "query", 
                        "required": False, 
                        "schema": {"type": "integer", "default": 20},
                        "description": "Maximum number of bookings to return (default: 20)"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User's booking history",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Booking"}
                                }
                            }
                        },
                    }
                },
            },
        },
        "/bookings/item/{item_id}": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get bookings for specific item",
                "description": "Get all bookings for a specific item. Should only be accessible by item owner.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "item_id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {
                        "description": "List of bookings for the item",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Booking"}
                                }
                            }
                        },
                    }
                },
            },
        },
        "/bookings/{booking_id}/duration": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get booking duration",
                "description": "Get the duration of a booking in days. Users can only access their own bookings.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "booking_id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {
                        "description": "Booking duration",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "duration_days": {"type": "integer", "example": 5}
                                    }
                                }
                            }
                        },
                    },
                    "404": {"description": "Booking not found or access denied"},
                },
            },
        },
        "/bookings/revenue": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get revenue from user's items",
                "description": "Calculate total revenue from completed bookings for the current user's items.",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Total revenue",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "total_revenue": {"type": "number", "example": 1250.50}
                                    }
                                }
                            }
                        },
                    }
                },
            },
        },
        "/bookings/statistics": {
            "get": {
                "tags": ["Booking"],
                "summary": "Get booking statistics",
                "description": "Get comprehensive booking statistics with optional date range filtering.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "start_date", 
                        "in": "query", 
                        "required": False, 
                        "schema": {"type": "string", "format": "date"},
                        "description": "Start date for statistics (YYYY-MM-DD)"
                    },
                    {
                        "name": "end_date", 
                        "in": "query", 
                        "required": False, 
                        "schema": {"type": "string", "format": "date"},
                        "description": "End date for statistics (YYYY-MM-DD)"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Booking statistics",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/BookingStatistics"}
                            }
                        },
                    },
                    "400": {"description": "Invalid date format"},
                },
            },
        },
    }


def get_all_paths():
    """Get all API paths."""
    paths = {}
    paths.update(get_health_paths())
    paths.update(get_item_paths())
    paths.update(get_auth_paths())
    paths.update(get_admin_paths())
    paths.update(get_statistics_paths())
    paths.update(get_review_paths())
    paths.update(get_payment_paths())
    paths.update(get_ticketing_paths())
    paths.update(get_booking_paths())
    return paths
