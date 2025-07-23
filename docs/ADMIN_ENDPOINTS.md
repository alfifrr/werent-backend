# Admin User Management Endpoint Documentation

## Overview
The WeRent Backend API now includes comprehensive admin user management functionality that allows existing admins to promote regular users to admin status and demote admin users back to regular status.

## Endpoints

### 1. Promote/Demote User Admin Status
**POST** `/api/admin/users/promote`

Promote a regular user to admin or demote an admin user to regular status.

**Authentication:** Required (JWT Token)
**Authorization:** Admin access required

**Request Body:**
```json
{
    "user_id": 123,
    "action": "promote"  // or "demote"
}
```

**Response (Success):**
```json
{
    "success": true,
    "message": "User user@example.com has been promoted to admin",
    "data": {
        "user": {
            "id": 123,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_admin": true,
            "is_verified": true,
            "is_active": true,
            // ... other user fields
        },
        "previous_status": false,
        "new_status": true,
        "action_performed": true
    }
}
```

### 2. Get All Admin Users
**GET** `/api/admin/users`

Retrieve a list of all admin users in the system.

**Authentication:** Required (JWT Token)
**Authorization:** Admin access required

**Response:**
```json
{
    "success": true,
    "message": "Admin users retrieved successfully",
    "data": {
        "admins": [
            {
                "id": 1,
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "is_admin": true,
                // ... other user fields
            }
        ],
        "total_count": 1
    }
}
```

### 3. Get Admin User by ID
**GET** `/api/admin/users/{admin_id}`

Retrieve a specific admin user by their ID.

**Authentication:** Required (JWT Token)
**Authorization:** Admin access required

**Response:**
```json
{
    "success": true,
    "message": "Admin user retrieved successfully",
    "data": {
        "admin": {
            "id": 1,
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "is_admin": true,
            // ... other user fields
        }
    }
}
```

## Security Features

### 1. Self-Demotion Prevention
Admins cannot demote themselves from admin status to prevent accidental lockouts.

### 2. Admin-Only Access
All admin endpoints require:
- Valid JWT authentication token
- User must have `is_admin: true` in their profile

### 3. Input Validation
- `user_id` must be a valid integer
- `action` must be either "promote" or "demote"
- Comprehensive Pydantic validation with detailed error messages

## Usage Examples

### Promote a User to Admin
```bash
curl -X POST http://localhost:5000/api/admin/users/promote \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "action": "promote"
  }'
```

### Demote an Admin to Regular User
```bash
curl -X POST http://localhost:5000/api/admin/users/promote \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "action": "demote"
  }'
```

### Get All Admins
```bash
curl -X GET http://localhost:5000/api/admin/users \
  -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN"
```

## Error Responses

### Validation Error (422)
```json
{
    "success": false,
    "error": "Validation failed",
    "error_code": "VALIDATION_ERROR",
    "details": {
        "field_errors": {
            "user_id": ["Input should be a valid integer"],
            "action": ["Action must be either 'promote' or 'demote'"]
        }
    }
}
```

### Unauthorized (401)
```json
{
    "success": false,
    "error": "Authentication required",
    "error_code": "UNAUTHORIZED"
}
```

### Forbidden (403)
```json
{
    "success": false,
    "error": "Admin access required",
    "error_code": "FORBIDDEN"
}
```

### User Not Found (404)
```json
{
    "success": false,
    "error": "Target user not found",
    "error_code": "NOT_FOUND"
}
```

## Implementation Details

### Model Updates
- User model includes `is_admin` boolean field
- UserService includes admin management methods
- Proper database relationships maintained

### Validation
- Pydantic schemas ensure data integrity
- Field validators for action types and user IDs
- Comprehensive error messages

### Service Layer
- `UserService.promote_to_admin(user_id)`
- `UserService.demote_from_admin(user_id)`
- `UserService.get_all_admins()`
- `UserService.get_admin_by_id(admin_id)`

### Security
- JWT token validation
- Admin role verification
- Self-modification protection

## Testing
Comprehensive test suite included (`test_admin_functionality.py`) covering:
- User creation and promotion
- Authentication and authorization
- Admin user management
- Access control
- Input validation
- Edge cases and error scenarios

All tests pass successfully! ✅
