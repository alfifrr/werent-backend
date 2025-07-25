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
                "description": {"type": "string", "example": "Lightweight summer dress."},
                "price_per_day": {"type": "number", "example": 15.0},
                "rating": {"type": "number", "example": 4.7},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
                "user_id": {"type": "integer", "example": 2},
                "images": {
                    "type": "array",
                    "items": {"type": "string"},
                    "example": []
                }
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
                "name": {"type": "string", "description": "Item name", "example": "Summer Dress"},
                "type": {
                    "type": "string", 
                    "description": "Item type",
                    "enum": ["dress", "top", "bottom", "outerwear", "shoes", "accessory", "jewelry", "bag", "formal_wear", "costume", "other"],
                    "example": "dress"
                },
                "size": {
                    "type": "string",
                    "description": "Item size",
                    "enum": ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "One Size"],
                    "example": "M"
                },
                "gender": {
                    "type": "string",
                    "description": "Target gender",
                    "enum": ["mens", "womens", "unisex", "kids"],
                    "example": "womens"
                },
                "brand": {"type": "string", "description": "Brand name", "example": "Zara"},
                "color": {"type": "string", "description": "Item color", "example": "Red"},
                "quantity": {"type": "integer", "description": "Available quantity", "minimum": 0, "example": 3},
                "product_code": {
                    "type": "string", 
                    "description": "Unique product code (must be unique across all items)",
                    "example": "ZARA_DRESS_001"
                },
                "description": {"type": "string", "description": "Item description", "example": "Lightweight summer dress."},
                "price_per_day": {"type": "number", "description": "Daily rental price", "minimum": 0, "example": 15.0},
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
            },
        },
        "ItemUpdateRequest": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Item name", "example": "Summer Dress Updated"},
                "type": {
                    "type": "string", 
                    "description": "Item type",
                    "enum": ["dress", "top", "bottom", "outerwear", "shoes", "accessory", "jewelry", "bag", "formal_wear", "costume", "other"],
                    "example": "dress"
                },
                "size": {
                    "type": "string",
                    "description": "Item size",
                    "enum": ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "One Size"],
                    "example": "L"
                },
                "gender": {
                    "type": "string",
                    "description": "Target gender",
                    "enum": ["mens", "womens", "unisex", "kids"],
                    "example": "womens"
                },
                "brand": {"type": "string", "description": "Brand name", "example": "Zara"},
                "color": {"type": "string", "description": "Item color", "example": "Blue"},
                "quantity": {"type": "integer", "description": "Available quantity", "minimum": 0, "example": 5},
                "product_code": {
                    "type": "string", 
                    "description": "Unique product code (must be unique across all items)",
                    "example": "ZARA_DRESS_001_UPDATED"
                },
                "description": {"type": "string", "description": "Item description", "example": "Updated description for summer dress."},
                "price_per_day": {"type": "number", "description": "Daily rental price", "minimum": 0, "example": 18.0},
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


def get_review_schemas():
    """Get review system schemas."""
    return {
        "Review": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "item_id": {"type": "integer", "example": 1, "description": "ID of the item being reviewed"},
                "service_id": {"type": "integer", "example": 1, "description": "ID of the service transaction"},
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "example": 5,
                },
                "comment": {
                    "type": "string",
                    "example": "Excellent service, perfect condition!",
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
                    "example": "Excellent service, perfect condition!",
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
                "payment_type": {"type": "string", "enum": ["RENT", "FINE"], "example": "RENT"},
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
                "payment_type": {"type": "string", "enum": ["RENT", "FINE"]},
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
                "payment_type": {"type": "string", "enum": ["RENT", "FINE"]},
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
    return schemas
