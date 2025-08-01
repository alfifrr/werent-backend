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
                "gender": {"type": "string", "example": "Women's"},
                "brand": {"type": "string", "example": "Zara"},
                "color": {"type": "string", "example": "Red"},
                "quantity": {"type": "integer", "example": 3},
                "product_code": {"type": "string", "example": "ZARA_DRESS_001"},
                "description": {
                    "type": "string",
                    "example": "Lightweight summer dress.",
                },
                "price_per_day": {"type": "number", "example": 15.0},
                "rating": {"type": "number", "example": 4.7},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
                "user_id": {"type": "integer", "example": 2},
                "images": {"type": "array", "items": {"type": "string"}, "example": []},
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
                "name": {
                    "type": "string",
                    "description": "Item name",
                    "example": "Summer Dress",
                },
                "type": {
                    "type": "string",
                    "description": "Item type",
                    "enum": [
                        "dress",
                        "top",
                        "bottom",
                        "outerwear",
                        "shoes",
                        "accessory",
                        "jewelry",
                        "bag",
                        "formal_wear",
                        "costume",
                        "other",
                    ],
                    "example": "dress",
                },
                "size": {
                    "type": "string",
                    "description": "Item size",
                    "enum": ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "One Size"],
                    "example": "M",
                },
                "gender": {
                    "type": "string",
                    "description": "Target gender",
                    "enum": ["mens", "womens", "unisex", "kids"],
                    "example": "womens",
                },
                "brand": {
                    "type": "string",
                    "description": "Brand name",
                    "example": "Zara",
                },
                "color": {
                    "type": "string",
                    "description": "Item color",
                    "example": "Red",
                },
                "quantity": {
                    "type": "integer",
                    "description": "Available quantity",
                    "minimum": 0,
                    "example": 3,
                },
                "product_code": {
                    "type": "string",
                    "description": "Unique product code (must be unique across all items)",
                    "example": "ZARA_DRESS_001",
                },
                "description": {
                    "type": "string",
                    "description": "Item description",
                    "example": "Lightweight summer dress.",
                },
                "price_per_day": {
                    "type": "number",
                    "description": "Daily rental price",
                    "minimum": 0,
                    "example": 15.0,
                },
                "images": {
                    "type": "array",
                    "description": "List of base64-encoded images (raw or data URL prefixed)",
                    "items": {
                        "type": "string",
                        "example": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...",
                    },
                    "example": [
                        "iVBORw0KGgoAAAANSUhEUgAAAAUA...",  # raw base64
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...",  # data URL base64
                    ],
                },
            },
            "example": {
                "name": "Summer Dress",
                "type": "dress",
                "size": "M",
                "gender": "womens",
                "brand": "Zara",
                "color": "Red",
                "quantity": 3,
                "product_code": "ZARA_DRESS_001",
                "description": "Lightweight summer dress.",
                "price_per_day": 15.0,
                "images": [
                    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                ],
            },
        },
        "ItemUpdateRequest": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Item name",
                    "example": "Summer Dress Updated",
                },
                "type": {
                    "type": "string",
                    "description": "Item type",
                    "enum": [
                        "dress",
                        "top",
                        "bottom",
                        "outerwear",
                        "shoes",
                        "accessory",
                        "jewelry",
                        "bag",
                        "formal_wear",
                        "costume",
                        "other",
                    ],
                    "example": "dress",
                },
                "size": {
                    "type": "string",
                    "description": "Item size",
                    "enum": ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "One Size"],
                    "example": "L",
                },
                "gender": {
                    "type": "string",
                    "description": "Target gender",
                    "enum": ["mens", "womens", "unisex", "kids"],
                    "example": "womens",
                },
                "brand": {
                    "type": "string",
                    "description": "Brand name",
                    "example": "Zara",
                },
                "color": {
                    "type": "string",
                    "description": "Item color",
                    "example": "Blue",
                },
                "quantity": {
                    "type": "integer",
                    "description": "Available quantity",
                    "minimum": 0,
                    "example": 5,
                },
                "product_code": {
                    "type": "string",
                    "description": "Unique product code (must be unique across all items)",
                    "example": "ZARA_DRESS_001_UPDATED",
                },
                "description": {
                    "type": "string",
                    "description": "Item description",
                    "example": "Updated description for summer dress.",
                },
                "price_per_day": {
                    "type": "number",
                    "description": "Daily rental price",
                    "minimum": 0,
                    "example": 18.0,
                },
                "images": {
                    "type": "array",
                    "description": "List of base64-encoded images (raw or data URL prefixed). To remove all images, set to an empty array []. To update specific images, include all images that should remain, including any existing ones.",
                    "items": {
                        "type": "string",
                        "example": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...",
                    },
                    "example": [
                        "iVBORw0KGgoAAAANSUhEUgAAAAUA...",  # raw base64
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...",  # data URL base64
                    ],
                },
            },
            "example": {
                "name": "Summer Dress Updated",
                "type": "dress",
                "size": "L",
                "gender": "womens",
                "brand": "Zara",
                "color": "Blue",
                "quantity": 5,
                "product_code": "ZARA_DRESS_001_UPDATED",
                "description": "Updated description for summer dress.",
                "price_per_day": 18.0,
                "images": [
                    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                ],
            },
        },
    }


def get_statistics_schemas():
    """Get admin dashboard statistics schemas."""
    return {
        "AdminStatisticsResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {"type": "string", "example": "Admin statistics fetched successfully"},
                "data": {
                    "type": "object",
                    "properties": {
                        "total_users": {"type": "integer", "example": 120},
                        "total_items": {"type": "integer", "example": 85},
                        "total_bookings": {"type": "integer", "example": 340},
                        "total_revenue": {"type": "number", "example": 18500.50},
                        "total_reviews": {"type": "integer", "example": 210},
                        "total_tickets": {"type": "integer", "example": 14},
                        "weekly": {
                            "type": "object",
                            "properties": {
                                "users": {"type": "integer", "example": 5},
                                "items": {"type": "integer", "example": 3},
                                "bookings": {"type": "integer", "example": 22},
                                "revenue": {"type": "number", "example": 1500.75},
                                "reviews": {"type": "integer", "example": 11},
                                "tickets": {"type": "integer", "example": 2}
                            }
                        }
                    }
                }
            },
            "example": {
                "success": True,
                "message": "Admin statistics fetched successfully",
                "data": {
                    "total_users": 120,
                    "total_items": 85,
                    "total_bookings": 340,
                    "total_revenue": 18500.50,
                    "total_reviews": 210,
                    "total_tickets": 14,
                    "weekly": {
                        "users": 5,
                        "items": 3,
                        "bookings": 22,
                        "revenue": 1500.75,
                        "reviews": 11,
                        "tickets": 2
                    }
                }
            }
        },
        "AdminMonthlyStatisticsResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {"type": "string", "example": "Monthly statistics for 2024 fetched successfully"},
                "data": {
                    "type": "object",
                    "properties": {
                        "users": {"type": "array", "items": {"type": "integer"}, "example": [2, 3, 5, 1, 6, 2, 0, 0, 3, 4, 2, 2]},
                        "items": {"type": "array", "items": {"type": "integer"}, "example": [1, 2, 1, 0, 3, 1, 0, 0, 2, 1, 0, 1]},
                        "bookings": {"type": "array", "items": {"type": "integer"}, "example": [15, 20, 18, 22, 30, 25, 10, 12, 17, 19, 13, 16]},
                        "revenue": {"type": "array", "items": {"type": "number"}, "example": [1250.0, 1500.5, 1800.0, 1400.0, 2100.0, 1750.0, 900.0, 950.0, 1600.0, 1700.0, 1200.0, 1300.0]},
                        "reviews": {"type": "array", "items": {"type": "integer"}, "example": [4, 6, 5, 3, 7, 2, 0, 1, 5, 4, 2, 3]},
                        "tickets": {"type": "array", "items": {"type": "integer"}, "example": [1, 0, 2, 1, 1, 0, 0, 1, 2, 1, 0, 1]}
                    }
                }
            },
            "example": {
                "success": True,
                "message": "Monthly statistics for 2024 fetched successfully",
                "data": {
                    "users": [2, 3, 5, 1, 6, 2, 0, 0, 3, 4, 2, 2],
                    "items": [1, 2, 1, 0, 3, 1, 0, 0, 2, 1, 0, 1],
                    "bookings": [15, 20, 18, 22, 30, 25, 10, 12, 17, 19, 13, 16],
                    "revenue": [1250.0, 1500.5, 1800.0, 1400.0, 2100.0, 1750.0, 900.0, 950.0, 1600.0, 1700.0, 1200.0, 1300.0],
                    "reviews": [4, 6, 5, 3, 7, 2, 0, 1, 5, 4, 2, 3],
                    "tickets": [1, 0, 2, 1, 1, 0, 0, 1, 2, 1, 0, 1]
                }
            }
        }
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
                    "example": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA...",
                },
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
                "is_active": {"type": "boolean", "example": True},
                "is_admin": {"type": "boolean", "example": False},
                "is_verified": {"type": "boolean", "example": False},
                "uuid": {
                    "type": "string",
                    "example": "bc84edc9-04a2-4a4b-a219-f2b33903562d",
                },
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
                "phone_number": {
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
                    "example": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
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
                    "example": "user@example.com",
                }
            },
        },
        "EmailVerificationResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {
                    "type": "string",
                    "example": "Email verified successfully! Welcome to WeRent.",
                },
                "data": {
                    "type": "object",
                    "properties": {"verified": {"type": "boolean", "example": True}},
                },
            },
        },
        "ResendVerificationResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {
                    "type": "string",
                    "example": "Verification email sent successfully. Please check your inbox.",
                },
                "data": {
                    "type": "object",
                    "properties": {"email_sent": {"type": "boolean", "example": True}},
                },
            },
        },
    }


def get_review_schemas():
    """Get review system schemas."""
    return {
        "Review": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "user_full_name": {"type": "string", "example": "John Doe"},
                "item_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "ID of the item being reviewed",
                },
                "service_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "ID of the service transaction",
                },
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "example": 5,
                },
                "review_message": {
                    "type": "string",
                    "example": "Excellent service, perfect condition!",
                },
                "images": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Array of image URLs or base64 encoded strings",
                    },
                    "example": [
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                    ],
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
                "review_message": {
                    "type": "string",
                    "example": "Excellent service, perfect condition!",
                },
                "images": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Array of image URLs or base64 encoded strings",
                    },
                    "example": [
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII=",
                    ],
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


def get_payment_schemas():
    """Get payment-related schemas."""
    return {
        "Payment": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "booking_id": {"type": "array", "items": {"type": "integer"}, "example": [1, 2]},
                "total_price": {"type": "number", "example": 100.0},
                "payment_method": {"type": "string", "enum": ["CC", "QRIS", "TRANSFER", "Cash"], "example": "CC"},
                "payment_type": {"type": "string", "enum": ["RENT", "FINE"], "example": "RENT", "description": "Payment type: RENT sets booking status to PAID, FINE sets booking status to RETURNED"},
                "payment_date": {"type": "string", "format": "date-time", "example": "2024-05-01T12:00:00Z"},
                "user_id": {"type": "integer", "example": 1},
            },
        },
        "PaymentCreateRequest": {
            "type": "object",
            "required": ["booking_id", "total_price", "payment_method", "payment_type"],
            "properties": {
                "booking_id": {"type": "array", "items": {"type": "integer"}},
                "total_price": {"type": "number"},
                "payment_method": {"type": "string", "enum": ["CC", "QRIS", "TRANSFER", "Cash"]},
                "payment_type": {"type": "string", "enum": ["RENT", "FINE"], "description": "Payment type: RENT sets booking status to PAID, FINE sets booking status to RETURNED"},
                "user_id": {"type": "integer"},
            },
            "example": {
                "booking_id": [1, 2],
                "total_price": 100.0,
                "payment_method": "CC",
                "payment_type": "RENT",
                "user_id": 1
            },
        },
        "PaymentUpdateRequest": {
            "type": "object",
            "properties": {
                "booking_id": {"type": "array", "items": {"type": "integer"}},
                "total_price": {"type": "number"},
                "payment_method": {"type": "string", "enum": ["CC", "QRIS", "TRANSFER", "Cash"]},
                "payment_type": {"type": "string", "enum": ["RENT", "FINE"], "description": "Payment type: RENT sets booking status to PAID, FINE sets booking status to RETURNED"},
                "user_id": {"type": "integer"},
            },
            "example": {
                "total_price": 120.0
            },
        },
    }


def get_health_schemas():
    """Get health check schemas."""
    return {
        "HealthResponse": {
            "type": "object",
            "properties": {
                "service": {"type": "string", "example": "WeRent Backend API"},
                "status": {"type": "string", "example": "healthy"},
                "version": {"type": "string", "example": "1.0.0"},
                "timestamp": {"type": "string", "example": "2025-07-25T14:30:51.467768"},
                "environment": {"type": "string", "example": "development"},
                "uptime": {"type": "string", "example": "Service is running"},
                "database": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "healthy"},
                        "type": {"type": "string", "example": "sqlite"}
                    }
                }
            }
        },
        "DetailedHealthResponse": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "example": "WeRent Backend API"},
                        "description": {"type": "string", "example": "Equipment rental platform backend service"},
                        "version": {"type": "string", "example": "1.0.0"}
                    }
                },
                "status": {"type": "string", "example": "healthy"},
                "timestamp": {"type": "string", "example": "2025-07-25T14:30:59.176323"},
                "database": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "healthy"},
                        "type": {"type": "string", "example": "sqlite"},
                        "version": {"type": "string", "example": "3.47.1"}
                    }
                },
                "environment": {
                    "type": "object",
                    "properties": {
                        "flask_env": {"type": "string", "example": "development"},
                        "port": {"type": "string", "example": "5000"},
                        "python_version": {"type": "string", "example": "3.12.11"}
                    }
                },
                "features": {
                    "type": "object",
                    "properties": {
                        "authentication": {"type": "string", "example": "JWT"},
                        "cors": {"type": "string", "example": "enabled"},
                        "migrations": {"type": "string", "example": "flask-migrate"}
                    }
                }
            }
        }
    }


def get_ticketing_schemas():
    """Get ticketing system schemas."""
    return {
        "Ticket": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "booking_id": {"type": "integer", "nullable": True, "example": None, "description": "Optional booking ID if ticket is booking-related"},
                "chat_content": {"type": "string", "example": "[2025-07-25 16:45:30] I have an issue with my camera rental", "description": "Conversation history with timestamps"},
                "is_resolved": {"type": "boolean", "example": False, "description": "Whether the ticket is resolved"},
                "created_at": {"type": "string", "format": "date-time", "example": "2025-07-25T16:45:30.814919"},
                "updated_at": {"type": "string", "format": "date-time", "example": "2025-07-25T16:45:30.814924"}
            },
            "required": ["id", "user_id", "chat_content", "is_resolved", "created_at", "updated_at"]
        },
        "TicketCreateRequest": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string", 
                    "minLength": 1,
                    "maxLength": 5000,
                    "example": "I have an issue with my camera rental",
                    "description": "Initial message describing the issue"
                },
                "booking_id": {
                    "type": "integer", 
                    "nullable": True, 
                    "example": None,
                    "description": "Optional booking ID if ticket is related to a specific booking"
                }
            },
            "required": ["message"],
            "example": {
                "message": "I have an issue with my camera rental",
                "booking_id": None
            }
        },
        "TicketMessageRequest": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000,
                    "example": "The camera lens appears to be damaged",
                    "description": "Message content to add to the ticket conversation"
                }
            },
            "required": ["message"],
            "example": {
                "message": "The camera lens appears to be damaged"
            }
        },
        "TicketListResponse": {
            "type": "object",
            "properties": {
                "tickets": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Ticket"}
                },
                "total_count": {"type": "integer", "example": 5}
            },
            "required": ["tickets", "total_count"]
        },
        "TicketStatsResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "message": {"type": "string", "example": "Ticket statistics retrieved successfully"},
                "data": {
                    "type": "object",
                    "properties": {
                        "total_tickets": {"type": "integer", "example": 15},
                        "open_tickets": {"type": "integer", "example": 3},
                        "resolved_tickets": {"type": "integer", "example": 12}
                    },
                    "required": ["total_tickets", "open_tickets", "resolved_tickets"]
                }
            },
            "required": ["success", "message", "data"]
        }
    }


def get_booking_schemas():
    """Get booking-related schemas."""
    return {
        "Booking": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "item_id": {"type": "integer", "example": 2},
                "start_date": {"type": "string", "format": "date", "example": "2024-08-01"},
                "end_date": {"type": "string", "format": "date", "example": "2024-08-05"},
                "total_price": {"type": "number", "example": 100.0},
                "status": {
                    "type": "string", 
                    "enum": ["pending", "confirmed", "completed", "cancelled", "pastdue", "returned"], 
                    "example": "pending"
                },
                "is_paid": {"type": "boolean", "example": False},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "BookingCreate": {
            "type": "object",
            "required": ["item_id", "start_date", "end_date"],
            "properties": {
                "item_id": {
                    "type": "integer",
                    "description": "ID of the item to book",
                    "example": 2
                },
                "start_date": {
                    "type": "string", 
                    "format": "date",
                    "description": "Booking start date (YYYY-MM-DD)",
                    "example": "2024-08-01"
                },
                "end_date": {
                    "type": "string", 
                    "format": "date",
                    "description": "Booking end date (YYYY-MM-DD)",
                    "example": "2024-08-05"
                },
            },
        },
        "BookingCreateRequest": {
            "type": "object",
            "required": ["item_id", "start_date", "end_date"],
            "properties": {
                "item_id": {
                    "type": "integer",
                    "description": "ID of the item to book",
                    "example": 2
                },
                "start_date": {
                    "type": "string", 
                    "format": "date",
                    "description": "Booking start date (YYYY-MM-DD)",
                    "example": "2024-08-01"
                },
                "end_date": {
                    "type": "string", 
                    "format": "date",
                    "description": "Booking end date (YYYY-MM-DD)",
                    "example": "2024-08-05"
                },
            },
        },
        "BookingOut": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "item_id": {"type": "integer", "example": 2},
                "start_date": {"type": "string", "format": "date", "example": "2024-08-01"},
                "end_date": {"type": "string", "format": "date", "example": "2024-08-05"},
                "total_price": {"type": "number", "example": 100.0},
                "status": {
                    "type": "string", 
                    "enum": ["pending", "confirmed", "completed", "cancelled", "pastdue", "returned"], 
                    "example": "pending"
                },
                "is_paid": {"type": "boolean", "example": False},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "BookingUpdateRequest": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string", 
                    "format": "date",
                    "description": "New booking start date (YYYY-MM-DD)",
                    "example": "2024-08-02"
                },
                "end_date": {
                    "type": "string", 
                    "format": "date",
                    "description": "New booking end date (YYYY-MM-DD)",
                    "example": "2024-08-06"
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "confirmed", "completed", "cancelled", "pastdue", "returned"],
                    "description": "Booking status",
                    "example": "confirmed"
                },
                "is_paid": {
                    "type": "boolean",
                    "description": "Payment status",
                    "example": True
                },
            },
            "example": {
                "start_date": "2024-08-02",
                "end_date": "2024-08-06",
                "status": "confirmed"
            }
        },
        "BookingStatusUpdate": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pending", "confirmed", "completed", "cancelled", "pastdue", "returned"],
                    "description": "New booking status. Follows this flow:\n1. PENDING (when booking created)\n2. PAID (changed after payment creation)\n3. CONFIRMED (Manually changed by admin in admin dashboard)\n4. RETURNED (Manually changed by renter in user dashboard)\n5. COMPLETED (manually changed by admin in admin dashboard)\n\nOwners can cancel bookings at any time. Admins can cancel from PENDING or CONFIRMED to CANCELLED.",
                    "example": "confirmed"
                }
            },
            "example": {
                "status": "confirmed"
            }
        },
        "BookingExtendRequest": {
            "type": "object",
            "required": ["new_end_date"],
            "properties": {
                "new_end_date": {
                    "type": "string", 
                    "format": "date",
                    "description": "New end date for the booking (YYYY-MM-DD)",
                    "example": "2024-08-10"
                },
            },
            "example": {
                "new_end_date": "2024-08-10"
            }
        },
        "BookingStatistics": {
            "type": "object",
            "properties": {
                "total_bookings": {
                    "type": "integer",
                    "description": "Total number of bookings",
                    "example": 150
                },
                "pending_bookings": {
                    "type": "integer",
                    "description": "Number of pending bookings",
                    "example": 25
                },
                "confirmed_bookings": {
                    "type": "integer",
                    "description": "Number of confirmed bookings",
                    "example": 80
                },
                "completed_bookings": {
                    "type": "integer",
                    "description": "Number of completed bookings",
                    "example": 40
                },
                "cancelled_bookings": {
                    "type": "integer",
                    "description": "Number of cancelled bookings",
                    "example": 5
                },
                "pastdue_bookings": {
                    "type": "integer",
                    "description": "Number of pastdue bookings",
                    "example": 10
                },
                "returned_bookings": {
                    "type": "integer",
                    "description": "Number of returned bookings",
                    "example": 10
                },
                "total_revenue": {
                    "type": "number",
                    "description": "Total revenue from completed bookings",
                    "example": 2500.75
                }
            },
            "example": {
                "total_bookings": 150,
                "pending_bookings": 25,
                "confirmed_bookings": 80,
                "completed_bookings": 40,
                "cancelled_bookings": 5,
                "pastdue_bookings": 10,
                "returned_bookings": 10,
                "total_revenue": 2500.75
            }
        },
    }


def get_all_schemas():
    """Get all OpenAPI component schemas."""
    schemas = {}
    schemas.update(get_item_schemas())
    schemas.update(get_auth_schemas())
    schemas.update(get_review_schemas())
    schemas.update(get_response_schemas())
    schemas.update(get_payment_schemas())
    schemas.update(get_health_schemas())
    schemas.update(get_ticketing_schemas())
    schemas.update(get_booking_schemas())
    schemas.update(get_statistics_schemas())
    return schemas
