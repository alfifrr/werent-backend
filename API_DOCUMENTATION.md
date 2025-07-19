# CamRent Backend API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication Endpoints

### 1. User Signup
**POST** `/api/auth/signup`

Creates a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890" // optional
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
  "message": "User created successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "created_at": "2025-07-19T10:12:12.908589",
    "is_active": true
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `400` - Missing required fields or invalid email format
- `409` - Email already registered

### 2. User Login
**POST** `/api/auth/login`

Authenticates a user and returns access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200 - Success):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "created_at": "2025-07-19T10:12:12.908589",
    "is_active": true
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `400` - Missing email or password
- `401` - Invalid credentials or account deactivated

### 3. Get User Profile
**GET** `/api/auth/profile`

Returns the current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 - Success):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "created_at": "2025-07-19T10:12:12.908589",
    "is_active": true
  }
}
```

**Error Responses:**
- `401` - Invalid or missing token
- `404` - User not found

### 4. User Logout
**POST** `/api/auth/logout`

Logs out the current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 - Success):**
```json
{
  "message": "Logout successful"
}
```

## Database Schema

### User Table
- `id` (Integer, Primary Key)
- `email` (String, Unique, Required)
- `password_hash` (String, Required)
- `first_name` (String, Required)
- `last_name` (String, Required)
- `phone` (String, Optional)
- `created_at` (DateTime, Auto-generated)
- `is_active` (Boolean, Default: True)

## JWT Configuration
- Token expires in 24 hours
- Token contains user ID as subject
- Include token in Authorization header: `Bearer <token>`

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
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Logout:**
```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
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

## Security Notes
- Change secret keys in production
- Use environment variables for configuration
- Implement proper error logging
- Add rate limiting for auth endpoints
- Consider implementing refresh tokens
- Add password reset functionality
