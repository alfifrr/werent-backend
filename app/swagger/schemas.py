"""
OpenAPI 3.0 schemas for WeRent Backend API.
Contains all data models and component schemas used in the API documentation.
"""


def get_item_schemas():
    """Get item-related schemas."""
    return {
        "Item": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "Summer Dress"},
                "type": {"type": "string", "example": "Dress"},
                "size": {"type": "string", "example": "M"},
                "gender": {"type": "string", "example": "Womens"},
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
            },
        },
        "ItemCreateRequest": {
            "type": "object",
            "required": [
                "name",
                "type",
                "size",
                "gender",
                "product_code",
                "description",
                "price_per_day",
                "quantity",
            ],
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
                "price_per_day": {"type": "number"},
            },
            "example": {
                "name": "Summer Dress",
                "type": "Dress",
                "size": "M",
                "gender": "Womens",
                "brand": "Zara",
                "color": "Red",
                "quantity": 3,
                "product_code": "SKU12345",
                "description": "Lightweight summer dress.",
                "price_per_day": 15.0,
            },
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
                "price_per_day": {"type": "number"},
            },
            "example": {
                "name": "Summer Dress Updated",
                "type": "Dress",
                "size": "L",
                "gender": "Womens",
                "brand": "Zara",
                "color": "Blue",
                "quantity": 5,
                "product_code": "SKU12345",
                "description": "Updated description for summer dress.",
                "price_per_day": 18.0,
            },
        },
    }


def get_auth_schemas():
    """Get authentication-related schemas."""
    return {
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john.doe@werent.com",
                },
                "first_name": {"type": "string", "example": "John"},
                "last_name": {"type": "string", "example": "Doe"},
                "phone_number": {"type": "string", "example": "+1234567890"},
                "profile_image": {
                    "type": "string",
                    "nullable": True,
                    "description": "Base64 encoded profile image data",
                    "example": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
                },
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
                "is_active": {"type": "boolean", "example": True},
                "is_admin": {"type": "boolean", "example": False},
                "is_verified": {"type": "boolean", "example": False},
                "uuid": {"type": "string", "example": "bc84edc9-04a2-4a4b-a219-f2b33903562d"},
            },
        },
        "SignupRequest": {
            "type": "object",
            "required": ["email", "password", "first_name", "last_name"],
            "properties": {
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john.doe@werent.com",
                    "description": "Valid email address",
                },
                "password": {
                    "type": "string",
                    "minLength": 8,
                    "example": "SecurePass123",
                    "description": "Password (min 8 chars, uppercase, lowercase, number)",
                },
                "first_name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50,
                    "example": "John",
                },
                "last_name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50,
                    "example": "Doe",
                },
                "phone": {
                    "type": "string",
                    "example": "+1234567890",
                    "description": "Phone number (optional)",
                },
            },
        },
        "LoginRequest": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john.doe@werent.com",
                },
                "password": {"type": "string", "example": "SecurePass123"},
            },
        },
        "ProfileUpdateRequest": {
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50,
                    "example": "John",
                },
                "last_name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50,
                    "example": "Doe",
                },
                "phone_number": {"type": "string", "example": "+1234567890"},
                "profile_image": {
                    "type": "string",
                    "description": "Base64 encoded image data with data URI prefix (e.g., data:image/jpeg;base64,...)",
                    "example": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
                },
            },
        },
        "EmailRequest": {
            "type": "object",
            "required": ["email"],
            "properties": {
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "Email address to send verification to",
                    "example": "user@example.com"
                }
            }
        },
        "EmailVerificationResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {"type": "string", "example": "Email verified successfully! Welcome to WeRent."},
                "data": {
                    "type": "object",
                    "properties": {
                        "verified": {"type": "boolean", "example": True}
                    }
                }
            }
        },
        "ResendVerificationResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {"type": "string", "example": "Verification email sent successfully. Please check your inbox."},
                "data": {
                    "type": "object",
                    "properties": {
                        "email_sent": {"type": "boolean", "example": True}
                    }
                }
            }
        },
    }


def get_gear_schemas():
    """Get gear management schemas (future implementation)."""
    return {
        "GearItem": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "Canon EOS R5"},
                "category": {
                    "type": "string",
                    "example": "camera",
                    "enum": ["camera", "lens", "lighting", "accessory"],
                },
                "brand": {"type": "string", "example": "Canon"},
                "model": {"type": "string", "example": "EOS R5"},
                "description": {
                    "type": "string",
                    "example": "Professional mirrorless camera with 45MP sensor",
                },
                "daily_rate": {"type": "number", "example": 85.00},
                "weekly_rate": {"type": "number", "example": 500.00},
                "deposit_amount": {"type": "number", "example": 1000.00},
                "availability_status": {
                    "type": "string",
                    "example": "available",
                    "enum": [
                        "available",
                        "rented",
                        "maintenance",
                        "unavailable",
                    ],
                },
                "condition": {
                    "type": "string",
                    "example": "excellent",
                    "enum": ["excellent", "good", "fair", "poor"],
                },
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "GearCreateRequest": {
            "type": "object",
            "required": ["name", "category", "brand", "daily_rate"],
            "properties": {
                "name": {"type": "string", "example": "Canon EOS R5"},
                "category": {
                    "type": "string",
                    "example": "camera",
                    "enum": ["camera", "lens", "lighting", "accessory"],
                },
                "brand": {"type": "string", "example": "Canon"},
                "model": {"type": "string", "example": "EOS R5"},
                "description": {
                    "type": "string",
                    "example": "Professional mirrorless camera",
                },
                "daily_rate": {"type": "number", "example": 85.00},
                "weekly_rate": {"type": "number", "example": 500.00},
                "deposit_amount": {"type": "number", "example": 1000.00},
            },
        },
    }


def get_rental_schemas():
    """Get rental system schemas (future implementation)."""
    return {
        "Rental": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "gear_item_id": {"type": "integer", "example": 1},
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "example": "2024-01-15",
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "example": "2024-01-20",
                },
                "total_cost": {"type": "number", "example": 425.00},
                "deposit_paid": {"type": "number", "example": 1000.00},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "RentalRequest": {
            "type": "object",
            "required": ["gear_item_id", "start_date", "end_date"],
            "properties": {
                "gear_item_id": {"type": "integer", "example": 1},
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "example": "2024-01-15",
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "example": "2024-01-20",
                },
                "notes": {
                    "type": "string",
                    "example": "Needed for wedding photography",
                },
            },
        },
    }


def get_review_schemas():
    """Get review system schemas (future implementation)."""
    return {
        "Review": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "gear_item_id": {"type": "integer", "example": 1},
                "rental_id": {"type": "integer", "example": 1},
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "example": 5,
                },
                "comment": {
                    "type": "string",
                    "example": "Excellent camera, perfect condition!",
                },
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "ReviewRequest": {
            "type": "object",
            "required": ["rating"],
            "properties": {
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "example": 5,
                },
                "comment": {
                    "type": "string",
                    "example": "Excellent camera, perfect condition!",
                },
            },
        },
    }


def get_response_schemas():
    """Get common response schemas."""
    return {
        "SignupSuccessResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {
                    "type": "string",
                    "example": "User created successfully",
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "user": {"$ref": "#/components/schemas/User"}
                    },
                },
            },
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
                        "access_token": {
                            "type": "string",
                            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "description": "JWT access token (expires in 15 minutes)",
                        },
                        "refresh_token": {
                            "type": "string",
                            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "description": "JWT refresh token (expires in 30 days)",
                        },
                    },
                },
            },
        },
        "RefreshTokenResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {
                    "type": "string",
                    "example": "Access token refreshed successfully",
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "access_token": {
                            "type": "string",
                            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "description": "New JWT access token (expires in 15 minutes)",
                        }
                    },
                },
            },
        },
        "ProfileResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {
                    "type": "string",
                    "example": "Profile retrieved successfully",
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "user": {"$ref": "#/components/schemas/User"}
                    },
                },
            },
        },
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": False},
                "error": {"type": "string", "example": "Invalid email format"},
                "error_code": {"type": "string", "example": "VALIDATION_ERROR"},
                "details": {"type": "object"},
            },
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
                                "password": "Password must be at least 8 characters",
                            },
                        }
                    },
                },
            },
        },
    }


def get_all_schemas():
    """Get all OpenAPI component schemas."""
    schemas = {}
    schemas.update(get_item_schemas())
    schemas.update(get_auth_schemas())
    schemas.update(get_gear_schemas())
    schemas.update(get_rental_schemas())
    schemas.update(get_review_schemas())
    schemas.update(get_response_schemas())
    return schemas
