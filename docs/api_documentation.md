# WeRent Backend API Documentation

## Base URL
```
http://localhost:5000
```

## Interactive Documentation
- **Swagger UI:** [http://localhost:5000/docs/](http://localhost:5000/docs/)
- **ReDoc:** [http://localhost:5000/redoc/](http://localhost:5000/redoc/)

## Authentication System

WeRent uses JWT-based authentication with a dual-token system:
- **Access Token**: Short-lived (15 minutes) for API requests
- **Refresh Token**: Long-lived (30 days) for obtaining new access tokens

### Authentication Flow
1. Register a new account (no JWT created)
2. Login to receive both access and refresh tokens
3. Use access token for API requests
4. When access token expires, use refresh token to get a new access token

## Authentication Endpoints

### 1. User Signup
**POST** `/api/auth/signup`

Creates a new user account. **Does not create JWT session** - user must login separately.

**Request Body:**
```json
{
  "email": "user@werent.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "1234567890"
}
```

**Password Requirements:**
- At least 8 characters long
- Must contain uppercase letter
- Must contain lowercase letter
- Must contain number

**Response (201 - Success):**
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "+1234567890",
      "is_admin": false,
      "is_verified": false,
      "is_active": true,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2025-07-19T10:12:12.908589",
      "updated_at": "2025-07-19T10:12:12.908589"
    }
  }
}
```

**Error Responses:**
- `400` - Missing required fields or invalid email format
- `409` - Email already registered
- `422` - Validation errors

### 2. User Login
**POST** `/api/auth/login`

Authenticate a user and return user info with JWT tokens.

**Request Body:**
```json
{
  "email": "john.doe@werent.com",
  "password": "SecurePass123"
}
```

**Success Response**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "john.doe@werent.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "+1234567890",
      "is_verified": false,
      "is_admin": false,
      "is_active": true,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2025-07-19T10:12:12.908589",
      "updated_at": "2025-07-19T10:12:12.908589"
    },
    "access_token": "<JWT access token>",
    "refresh_token": "<JWT refresh token>"
  }
}
```

**Token Information:**
- **Access Token**: Expires in 15 minutes, use for API requests
- **Refresh Token**: Expires in 30 days, use to get new access tokens

**Error Responses:**
- `400` - Missing or invalid fields
- `401` - Invalid credentials or account deactivated
- `500` - Unexpected error

**Notes:**
- The `user` object fields match the User model and all other user-related endpoints.
- The `access_token` and `refresh_token` are JWTs for authentication and session refresh.
- Example values are for documentation; actual tokens will differ.

### 3. Refresh Access Token
**POST** `/api/auth/refresh`

Generates a new access token using a valid refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200 - Success):**
```json
{
  "success": true,
  "message": "Access token refreshed successfully",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**
- `401` - Invalid or expired refresh token
- `404` - User not found

### 4. Get User Profile
**GET** `/api/auth/profile`

Returns the current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 - Success):**
```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "+1234567890",
      "is_admin": false,
      "is_verified": false,
      "is_active": true,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2025-07-19T10:12:12.908589",
      "updated_at": "2025-07-19T10:12:12.908589"
    }
  }
}
```

**Error Responses:**
- `401` - Invalid or missing access token
- `404` - User not found

### 5. Update User Profile
**PUT** `/api/auth/profile`

Updates the current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```
**Request Body (all fields optional):**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+0987654321"
}
```

**Response (200 - Success):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "phone_number": "+0987654321",
      "is_admin": false,
      "is_verified": false,
      "is_active": true,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2025-07-19T10:12:12.908589",
      "updated_at": "2025-07-19T10:15:42.123456"
    }
  }
}
```

**Error Responses:**
- `400` - Invalid request data
- `401` - Invalid or missing access token
- `404` - User not found
- `422` - Validation errors

## Database Schema

### User Table
- `id` (Integer, Primary Key)
- `email` (String, Unique, Required)
- `password_hash` (String, Required)
- `first_name` (String, Required)
- `last_name` (String, Required)
- `phone` (String, Optional)
- `created_at` (DateTime, Auto-generated)
- `updated_at` (DateTime, Auto-updated)
- `is_active` (Boolean, Default: True)

## JWT Configuration
- **Access Token**: Expires in 15 minutes
- **Refresh Token**: Expires in 30 days
- Access token contains user ID as subject
- Include access token in Authorization header: `Bearer <access_token>`
- Use refresh token at `/api/auth/refresh` to get new access token

## Testing Examples

### Using curl:

**Signup:**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@camrent.com",
    "password": "TestPass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@camrent.com",
    "password": "TestPass123"
  }'
```

**Get Profile:**
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Refresh Token:**
```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN_HERE"
```

**Update Profile:**
```bash
curl -X PUT http://localhost:5000/api/auth/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "first_name": "Jane",
    "phone": "+0987654321"
  }'
```

## Authentication Flow Example

```bash
# 1. Register new user (no JWT created)
SIGNUP_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@camrent.com", "password": "TestPass123", "first_name": "John", "last_name": "Doe"}')

# 2. Login to get tokens
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@camrent.com", "password": "TestPass123"}')

# Extract tokens (requires jq)
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.data.access_token')
REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.data.refresh_token')

# 3. Use access token for API calls
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 4. When access token expires (15 min), refresh it
NEW_ACCESS_TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer $REFRESH_TOKEN" | jq -r '.data.access_token')
```

## Future Endpoints (Based on CamRent Sitemap)

### Gear Management
- `GET /api/gear/` - List all gear
- `GET /api/gear/categories` - Get gear categories
- `GET /api/gear/{id}` - Get specific gear details
- `POST /api/gear/` - Add new gear (admin)

### Rental System
- `POST /api/cart/add` - Add gear to cart
- `GET /api/cart/` - Get user's cart
- `POST /api/checkout/` - Process rental checkout
- `GET /api/user/rentals` - Get user's rental history

### Reviews & Content
- `GET /api/reviews/{gear_id}` - Get gear reviews
- `POST /api/reviews/` - Add review
- `GET /api/blog/` - Get blog posts
- `POST /api/contact/` - Contact form submission

## Security Features Implemented
- ✅ JWT-based authentication with dual-token system
- ✅ Short-lived access tokens (15 minutes) for security
- ✅ Long-lived refresh tokens (30 days) for user convenience
- ✅ Secure password hashing with bcrypt
- ✅ Input validation and sanitization
- ✅ Environment-based configuration for secrets

## Security Notes
- Change secret keys in production
- Use environment variables for configuration
- Implement proper error logging
- Add rate limiting for auth endpoints
- ✅ Refresh tokens implemented for better security
- Add password reset functionality (planned)
- Consider implementing token blacklisting for logout (planned)
