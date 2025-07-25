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
                    "403": {"description": "Admin access required"},
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
                "description": "Update the authenticated user's profile information.",
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
    """Get ticketing system paths."""
    return {
        "/api/tickets": {
            "post": {
                "tags": ["Tickets"],
                "summary": "Create a new ticket",
                "description": "Create a new support ticket",
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
                                "schema": {"$ref": "#/components/schemas/Ticket"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data"
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}": {
            "get": {
                "tags": ["Tickets"],
                "summary": "Get a specific ticket",
                "description": "Retrieve details of a specific ticket by ID",
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
                                "schema": {"$ref": "#/components/schemas/Ticket"}
                            }
                        }
                    },
                    "404": {
                        "description": "Ticket not found"
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}/message": {
            "post": {
                "tags": ["Tickets"],
                "summary": "Add message to ticket",
                "description": "Add a new message to an existing ticket",
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
                    "201": {
                        "description": "Message added successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TicketMessage"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input data"
                    },
                    "404": {
                        "description": "Ticket not found"
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}/resolve": {
            "patch": {
                "tags": ["Tickets"],
                "summary": "Resolve a ticket",
                "description": "Mark a ticket as resolved",
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
                                "schema": {"$ref": "#/components/schemas/Ticket"}
                            }
                        }
                    },
                    "404": {
                        "description": "Ticket not found"
                    }
                }
            }
        },
        "/api/tickets/{ticket_id}/reopen": {
            "patch": {
                "tags": ["Tickets"],
                "summary": "Reopen a ticket",
                "description": "Reopen a resolved ticket",
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
                                "schema": {"$ref": "#/components/schemas/Ticket"}
                            }
                        }
                    },
                    "404": {
                        "description": "Ticket not found"
                    }
                }
            }
        },
        "/api/tickets/user/{user_id}": {
            "get": {
                "tags": ["Tickets"],
                "summary": "Get user tickets",
                "description": "Get all tickets for a specific user",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID of the user"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User tickets retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Ticket"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/open": {
            "get": {
                "tags": ["Tickets"],
                "summary": "Get open tickets",
                "description": "Get all open (unresolved) tickets",
                "responses": {
                    "200": {
                        "description": "Open tickets retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Ticket"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/tickets/resolved": {
            "get": {
                "tags": ["Tickets"],
                "summary": "Get resolved tickets",
                "description": "Get all resolved tickets",
                "responses": {
                    "200": {
                        "description": "Resolved tickets retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Ticket"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }


def get_all_paths():
    """Get all API paths."""
    paths = {}
    paths.update(get_health_paths())
    paths.update(get_item_paths())
    paths.update(get_auth_paths())
    paths.update(get_admin_paths())
    paths.update(get_review_paths())
    paths.update(get_payment_paths())
    paths.update(get_ticketing_paths())
    return paths
