"""
API paths definition for WeRent Backend API.
Contains all endpoint paths and their OpenAPI specifications.
"""


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
                "description": "Register a new user account with email and password. Does not create JWT session - use login endpoint to authenticate.",
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
    }


def get_admin_paths():
    """Get admin management paths."""
    return {
        "/api/admin/users/promote": {
            "post": {
                "tags": ["Admin"],
                "summary": "Promote user to admin",
                "description": "Promote a regular user to admin status. Requires admin authentication.",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "user_id": {
                                        "type": "integer",
                                        "description": "ID of the user to promote",
                                        "example": 123
                                    }
                                },
                                "required": ["user_id"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "User promoted successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean", "example": True},
                                        "message": {"type": "string", "example": "User promoted to admin successfully"},
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "user": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {"type": "integer", "example": 123},
                                                        "email": {"type": "string", "example": "user@example.com"},
                                                        "first_name": {"type": "string", "example": "John"},
                                                        "last_name": {"type": "string", "example": "Doe"},
                                                        "is_admin": {"type": "boolean", "example": True}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Invalid request or user already admin"},
                    "401": {"description": "Authentication required"},
                    "403": {"description": "Admin access required"},
                    "404": {"description": "User not found"}
                }
            }
        },
        "/api/admin/users": {
            "get": {
                "tags": ["Admin"],
                "summary": "List all admin users",
                "description": "Retrieve a list of all users with admin privileges. Requires admin authentication.",
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


def get_all_paths():
    """Get all API paths."""
    paths = {}
    paths.update(get_item_paths())
    paths.update(get_auth_paths())
    paths.update(get_admin_paths())
    return paths
