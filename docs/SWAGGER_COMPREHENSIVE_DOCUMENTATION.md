# WeRent Backend API - Swagger Documentation

## Overview

The WeRent Backend API now features comprehensive Swagger/OpenAPI 3.0 documentation with interactive endpoints for testing and exploration. The documentation includes detailed specifications for all implemented features including authentication, admin management, and profile image functionality.

## Accessing Swagger Documentation

### Development
- **Swagger UI**: http://localhost:5000/docs/
- **OpenAPI JSON**: http://localhost:5000/docs/swagger.json

### Production
- **Swagger UI**: https://api.werent.com/docs/
- **OpenAPI JSON**: https://api.werent.com/docs/swagger.json

---

## API Namespaces

The API is organized into logical namespaces for better organization and discoverability:

### 1. Authentication (`/api/auth`)
Complete user authentication and profile management:

#### Endpoints:
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `PUT /api/auth/profile/image` - **NEW** Update profile image
- `POST /api/auth/logout` - User logout

#### Features:
- JWT token-based authentication
- Email validation and uniqueness checks
- Password strength requirements
- Profile image upload with Base64 encoding
- Automatic image compression and optimization

### 2. Admin (`/api/admin`)
Administrative endpoints for platform management:

#### Endpoints:
- `POST /api/admin/users/promote` - **NEW** Promote/demote users
- `GET /api/admin/users` - **NEW** List all admin users
- `GET /api/admin/users/{id}` - **NEW** Get admin user details

#### Features:
- Role-based access control
- User privilege management
- Admin-only operations
- Comprehensive audit trails

### 3. Health (`/api/health`)
System health and monitoring:
- `GET /api/health` - Basic health check
- `GET /api/health/detailed` - Detailed system information

### 4. Future Namespaces (Coming Soon)
- **Gear Management** (`/api/gear`) - Equipment catalog
- **Rental System** (`/api/rentals`) - Booking management
- **Review System** (`/api/reviews`) - User feedback

---

## New Features Documented

### Profile Image Upload System

**Endpoint**: `PUT /api/auth/profile/image`

**Key Features**:
- Base64 image encoding support
- Automatic image compression (40-60% reduction)
- Support for JPEG, PNG, WebP formats
- Real-time compression statistics
- Secure image validation

**Swagger Documentation Includes**:
- Request/response models
- Image format requirements
- Compression information
- Error scenarios
- Security considerations

### Admin Management System

**Endpoints**:
- `POST /api/admin/users/promote` - User privilege management
- `GET /api/admin/users` - Admin user listing
- `GET /api/admin/users/{id}` - Admin user details

**Key Features**:
- Role-based access control
- User promotion/demotion
- Admin privilege verification
- Comprehensive error handling

**Swagger Documentation Includes**:
- Admin-specific models
- Authorization requirements
- Business rules documentation
- Security considerations
- Error response specifications

---

## Swagger Model Definitions

### Core Models

#### User Model
```json
{
  "id": 1,
  "email": "user@werent.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "is_admin": false,
  "is_verified": false,
  "is_active": true,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-07-23T10:12:12.908589",
  "updated_at": "2025-07-23T10:12:12.908589",
  "profile_image": "data:image/jpeg;base64,..."
}
```

#### Admin Promotion Model
```json
{
  "user_id": 26,
  "action": "promote"
}
```

#### Profile Image Model
```json
{
  "profile_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
}
```

### Response Models

#### Standard Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {...}
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Error description",
  "error_code": "ERROR_CODE",
  "details": {...}
}
```

#### Validation Error Response
```json
{
  "success": false,
  "error": "Validation failed",
  "error_code": "VALIDATION_ERROR",
  "details": {
    "field_errors": {
      "field_name": ["Error message"]
    }
  }
}
```

---

## Security Documentation

### Authentication
- **Type**: JWT Bearer Token
- **Header**: `Authorization: Bearer <token>`
- **Scope**: Required for most endpoints

### Authorization Levels
1. **Public**: Health checks, login, signup
2. **Authenticated**: Profile management, basic user operations
3. **Admin**: User management, platform administration

### Security Features
- JWT token validation
- Role-based access control
- Input validation with Pydantic
- CORS configuration
- Rate limiting (planned)

---

## Interactive Features

### Swagger UI Capabilities

1. **Try It Out**: Execute real API calls directly from documentation
2. **Authentication**: Built-in JWT token management
3. **Model Explorer**: Interactive model definitions
4. **Response Viewer**: Real-time response inspection
5. **Code Generation**: Multiple language client code examples

### Testing Environment

The Swagger UI provides:
- **Server Selection**: Toggle between development/production
- **Request Builder**: Interactive parameter input
- **Response Validation**: Schema validation feedback
- **Error Debugging**: Detailed error information

---

## API Documentation Features

### Comprehensive Documentation

Each endpoint includes:
- **Description**: Detailed functionality explanation
- **Parameters**: Required/optional parameter specifications
- **Request Bodies**: Complete model definitions
- **Response Examples**: Success and error scenarios
- **Security Requirements**: Authentication/authorization needs
- **Business Rules**: Operational constraints
- **Error Codes**: Standardized error responses

### Code Examples

Documentation includes examples for:
- **curl**: Command-line testing
- **JavaScript**: Frontend integration
- **Python**: Backend integration
- **React**: Component examples

---

## Development Workflow

### Using Swagger for Development

1. **API Exploration**: Browse available endpoints
2. **Authentication**: Test login to get JWT tokens
3. **Endpoint Testing**: Execute API calls with real data
4. **Response Analysis**: Examine response structures
5. **Error Handling**: Test error scenarios

### Integration Testing

Swagger UI enables:
- **End-to-End Testing**: Complete user workflows
- **Admin Operations**: Test administrative functions
- **Image Upload**: Test profile image functionality
- **Error Scenarios**: Validate error handling

---

## Production Considerations

### Documentation Deployment

- **Auto-Generated**: Documentation updates with code changes
- **Version Control**: Documentation versioning with API releases
- **Security**: Production docs exclude sensitive information
- **Performance**: Optimized for fast loading

### Monitoring Integration

- **Health Checks**: Integrated system monitoring
- **Error Tracking**: Standardized error reporting
- **Performance Metrics**: Response time monitoring
- **Usage Analytics**: API endpoint usage tracking

---

## Next Steps

### Planned Enhancements

1. **Interactive Authentication**: Enhanced token management
2. **Advanced Models**: Complex nested data structures
3. **File Upload UI**: Direct file upload in Swagger
4. **Mock Data**: Pre-populated test data
5. **API Versioning**: Multiple API version support

### Extended Documentation

1. **Workflow Guides**: Step-by-step API usage guides
2. **Integration Examples**: Framework-specific examples
3. **Best Practices**: API usage recommendations
4. **Troubleshooting**: Common issue resolution

---

## Technical Implementation

### Swagger Stack
- **Flask-RESTX**: OpenAPI 3.0 specification generation
- **Pydantic**: Model validation and documentation
- **JWT Integration**: Security scheme implementation
- **CORS Support**: Cross-origin request handling

### Documentation Structure
```
app/swagger/
├── __init__.py          # Main API configuration
├── models.py            # Swagger model definitions
├── auth_routes.py       # Authentication endpoints
├── admin_routes.py      # Admin endpoints
├── future_routes.py     # Placeholder endpoints
├── routes.py           # Route registration
└── swagger_ui.py       # UI customization
```

### Model Organization
- **Base Models**: Common response structures
- **Request Models**: Endpoint-specific inputs
- **Response Models**: Endpoint-specific outputs
- **Error Models**: Standardized error formats

---

## Usage Examples

### Getting Started with Swagger

1. **Navigate to Swagger UI**: http://localhost:5000/docs/
2. **Explore Endpoints**: Browse available API operations
3. **Authenticate**: Use `/api/auth/login` to get JWT token
4. **Set Authorization**: Click "Authorize" and enter `Bearer <token>`
5. **Test Endpoints**: Use "Try it out" on any endpoint
6. **View Responses**: Examine real API responses

### Admin Workflow Example

1. **Login as Admin**: Get admin JWT token
2. **View Users**: List all admin users
3. **Promote User**: Convert regular user to admin
4. **Verify Changes**: Check updated user status
5. **Demote User**: Revert admin status if needed

### Image Upload Workflow

1. **Authenticate**: Get user JWT token
2. **Prepare Image**: Convert image to Base64
3. **Upload**: Send PUT request to `/api/auth/profile/image`
4. **View Results**: Check compression statistics
5. **Verify Update**: Confirm profile image update

---

The WeRent Backend API now provides industry-standard documentation with comprehensive Swagger integration, making it easy for developers to understand, test, and integrate with the platform.
