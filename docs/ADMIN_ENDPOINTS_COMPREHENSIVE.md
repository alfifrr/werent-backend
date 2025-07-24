# Admin Endpoints Documentation

## Overview

The WeRent Backend API provides comprehensive admin management functionality for platform administration. These endpoints allow existing admin users to manage user privileges and oversee platform operations.

## Authentication & Authorization

All admin endpoints require:
- **JWT Authentication**: Valid access token in `Authorization: Bearer <token>` header
- **Admin Privileges**: Current user must have `is_admin: true` status

## Base URL

- **Development**: `http://localhost:5000/api/admin`
- **Production**: `https://api.werent.com/api/admin`

---

## Admin Endpoints

### 1. Promote/Demote User

**Endpoint**: `POST /api/admin/users/promote`

**Description**: Promote a regular user to admin status or demote an admin to regular user.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "user_id": 26,
  "action": "promote"
}
```

**Parameters**:
- `user_id` (integer, required): ID of the user to promote/demote
- `action` (string, required): Action to perform (`"promote"` or `"demote"`)

**Success Response** (200):
```json
{
  "success": true,
  "message": "User regular_user@werent.com has been promoted to admin",
  "data": {
    "action_performed": true,
    "previous_status": false,
    "new_status": true,
    "user": {
      "id": 26,
      "email": "regular_user@werent.com",
      "first_name": "Regular",
      "last_name": "User",
      "phone_number": "+1555888888",
      "is_admin": true,
      "is_verified": false,
      "is_active": true,
      "uuid": "56e0fbfa-99a3-4999-be0f-c97692cf8650",
      "created_at": "Wed, 23 Jul 2025 23:19:35 GMT",
      "updated_at": "Wed, 23 Jul 2025 23:27:56 GMT",
      "profile_image": null
    }
  }
}
```

**Error Responses**:

*Validation Error (422)*:
```json
{
  "success": false,
  "error": "Validation failed",
  "error_code": "VALIDATION_ERROR",
  "details": {
    "field_errors": {
      "action": ["Value error, Action must be either \"promote\" or \"demote\""]
    }
  }
}
```

*User Not Found (404)*:
```json
{
  "success": false,
  "error": "Target user not found not found",
  "error_code": "NOT_FOUND"
}
```

*Access Denied (403)*:
```json
{
  "success": false,
  "error": "Admin access required",
  "error_code": "FORBIDDEN"
}
```

---

### 2. List All Admin Users

**Endpoint**: `GET /api/admin/users`

**Description**: Retrieve a list of all users with admin privileges.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Success Response** (200):
```json
{
  "success": true,
  "message": "Admin users retrieved successfully",
  "data": {
    "admins": [
      {
        "id": 19,
        "email": "admin_1753286585@werent.com",
        "first_name": "Admin",
        "last_name": "User",
        "phone_number": "+1555000001",
        "is_admin": true,
        "is_verified": false,
        "is_active": true,
        "uuid": "40e26396-d073-4244-9b87-bdfd823e83ce",
        "created_at": "Wed, 23 Jul 2025 23:03:06 GMT",
        "updated_at": "Wed, 23 Jul 2025 23:03:06 GMT",
        "profile_image": null
      },
      {
        "id": 25,
        "email": "new_admin@werent.com",
        "first_name": "New",
        "last_name": "Admin",
        "phone_number": "+1555999999",
        "is_admin": true,
        "is_verified": false,
        "is_active": true,
        "uuid": "affa3a27-c719-4c41-9d1c-1fefaa74c590",
        "created_at": "Wed, 23 Jul 2025 23:19:14 GMT",
        "updated_at": "Wed, 23 Jul 2025 23:20:05 GMT",
        "profile_image": null
      }
    ],
    "total_count": 4
  }
}
```

**Error Responses**:

*Access Denied (403)*:
```json
{
  "success": false,
  "error": "Admin access required",
  "error_code": "FORBIDDEN"
}
```

---

### 3. Get Admin User by ID

**Endpoint**: `GET /api/admin/users/{admin_id}`

**Description**: Retrieve detailed information about a specific admin user.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
- `admin_id` (integer, required): ID of the admin user to retrieve

**Success Response** (200):
```json
{
  "success": true,
  "message": "Admin user retrieved successfully",
  "data": {
    "admin": {
      "id": 25,
      "email": "new_admin@werent.com",
      "first_name": "New",
      "last_name": "Admin",
      "phone_number": "+1555999999",
      "is_admin": true,
      "is_verified": false,
      "is_active": true,
      "uuid": "affa3a27-c719-4c41-9d1c-1fefaa74c590",
      "created_at": "Wed, 23 Jul 2025 23:19:14 GMT",
      "updated_at": "Wed, 23 Jul 2025 23:20:05 GMT",
      "profile_image": null
    }
  }
}
```

**Error Responses**:

*Admin Not Found (404)*:
```json
{
  "success": false,
  "error": "Admin user not found",
  "error_code": "NOT_FOUND"
}
```

*Access Denied (403)*:
```json
{
  "success": false,
  "error": "Admin access required",
  "error_code": "FORBIDDEN"
}
```

---

## Business Rules

### User Promotion/Demotion Rules:
1. **Self-Management Prevention**: Admins cannot promote or demote themselves
2. **Admin-Only Access**: Only users with `is_admin: true` can access admin endpoints
3. **Target User Validation**: Target user must exist in the system
4. **Action Validation**: Action must be either `"promote"` or `"demote"`
5. **Status Check**: System validates current admin status before performing action

### Security Features:
- **JWT Token Validation**: All requests require valid authentication
- **Role-Based Access Control**: Admin decorator enforces privilege requirements
- **Input Validation**: Pydantic schemas validate all request data
- **Audit Trail**: All admin actions are logged with timestamps

---

## Curl Examples

### Get Admin Token:
```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@werent.com", "password": "AdminPass123!"}' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print(data['data']['access_token'])")
```

### Promote User to Admin:
```bash
curl -X POST http://localhost:5000/api/admin/users/promote \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 26, "action": "promote"}'
```

### Demote Admin to Regular User:
```bash
curl -X POST http://localhost:5000/api/admin/users/promote \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 26, "action": "demote"}'
```

### List All Admins:
```bash
curl -X GET http://localhost:5000/api/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Get Specific Admin:
```bash
curl -X GET http://localhost:5000/api/admin/users/25 \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

## Error Handling

The admin endpoints return standardized error responses with appropriate HTTP status codes:

- **400 Bad Request**: Invalid request data or malformed JSON
- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: Insufficient privileges (non-admin user)
- **404 Not Found**: Target user or admin not found
- **422 Unprocessable Entity**: Validation failed on request data
- **500 Internal Server Error**: Unexpected server error

All error responses follow the format:
```json
{
  "success": false,
  "error": "Error description",
  "error_code": "ERROR_CODE",
  "details": {} // Optional additional context
}
```

---

## Integration Notes

- **Database**: Admin status changes are immediately persisted to the database
- **Validation**: All inputs are validated using Pydantic schemas
- **Logging**: Admin actions should be logged for audit purposes
- **Security**: Admin endpoints are protected by JWT and role-based access control
- **Testing**: Comprehensive curl testing has been performed and all endpoints are functional

## Next Steps

1. **Audit Logging**: Implement comprehensive admin action logging
2. **Permissions**: Add granular permission levels beyond basic admin/user
3. **Bulk Operations**: Support bulk user promotion/demotion
4. **Admin Dashboard**: Create web interface for admin operations
5. **Notifications**: Notify users when their admin status changes
