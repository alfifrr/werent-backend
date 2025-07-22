# WeRent API Documentation System

## Overview
The WeRent backend features a comprehensive API documentation system built with OpenAPI 3.0 specification and multiple viewing interfaces for different developer needs.

## Documentation Access Points

### 🔗 Available Documentation URLs

| Interface | URL | Description |
|-----------|-----|-------------|
| **Swagger UI** | `/docs/` | Interactive API documentation with live testing |
| **ReDoc** | `/docs/redoc` | Clean, readable documentation interface |
| **OpenAPI JSON** | `/docs/openapi.json` | Raw OpenAPI 3.0 specification |
| **Postman Collection** | `/docs/postman` | Postman collection for API testing |

### 📊 Development vs Production URLs

**Development Server (localhost:5000):**
- Swagger UI: http://localhost:5000/docs/
- ReDoc: http://localhost:5000/docs/redoc
- OpenAPI Spec: http://localhost:5000/docs/openapi.json
- Postman: http://localhost:5000/docs/postman

**Production Server:**
- Swagger UI: https://api.werent.com/docs/
- ReDoc: https://api.werent.com/docs/redoc
- OpenAPI Spec: https://api.werent.com/docs/openapi.json
- Postman: https://api.werent.com/docs/postman

## Features

### ✅ Current Implementation
- **Authentication Endpoints**: Complete documentation for signup, login, profile management
- **Interactive Testing**: Swagger UI allows live API testing with authentication
- **Multiple Formats**: Swagger UI, ReDoc, JSON spec, and Postman collection
- **Comprehensive Models**: Request/response schemas with validation rules
- **Security Documentation**: JWT authentication setup and usage
- **Error Handling**: Standardized error responses and status codes

### 🚧 Future Endpoints (Placeholders Ready)
- **Gear Management**: Equipment catalog and inventory
- **Rental System**: Booking and rental management  
- **Review System**: User reviews and ratings
- **Admin Panel**: Administrative features

## Technical Implementation

### Architecture
```
app/swagger/
├── swagger_ui.py          # Main Swagger UI implementation
├── models.py             # OpenAPI schema models (future)
├── auth_routes.py        # Authentication endpoint docs (future)
├── future_routes.py      # Placeholder route docs (future)
└── __init__.py          # Flask-RESTX configuration (if needed)
```

### Key Components

#### 1. OpenAPI 3.0 Specification
- **Complete API spec** with request/response schemas
- **Security schemes** for JWT authentication
- **Comprehensive models** for all data structures
- **Future endpoint placeholders** for development roadmap

#### 2. Swagger UI Integration
- **Interactive documentation** with live testing capabilities
- **Custom styling** with CamRent branding
- **Authentication support** for secured endpoints
- **Expandable sections** for better organization

#### 3. ReDoc Interface
- **Clean, readable format** for documentation review
- **Mobile-responsive design**
- **Advanced schema visualization**
- **Professional presentation** for stakeholders

#### 4. Postman Collection
- **Auto-generated collection** from OpenAPI spec
- **Environment variables** for easy testing
- **Authentication setup** with token management
- **Example requests** with sample data

## Usage Guide

### For Developers

#### 1. Exploring the API
1. Visit http://localhost:5000/docs/ for interactive documentation
2. Review available endpoints and their requirements
3. Use the "Try it out" feature to test endpoints live
4. Check request/response examples and schemas

#### 2. Authentication Testing
1. Use `/api/auth/signup` to create a test account
2. Use `/api/auth/login` to get a JWT token
3. Click "Authorize" in Swagger UI and enter: `Bearer <your-token>`
4. Test protected endpoints like `/api/auth/profile`

#### 3. Using Postman
1. Download collection from `/docs/postman`
2. Import into Postman
3. Set `baseUrl` variable to your server URL
4. Run authentication requests to set `accessToken` variable
5. Test protected endpoints automatically

### For API Consumers

#### 1. Integration Planning
- Review the OpenAPI spec at `/docs/openapi.json`
- Use ReDoc at `/docs/redoc` for clean documentation reading
- Download Postman collection for testing and integration

#### 2. Authentication Flow
```bash
# 1. Register a new user
curl -X POST http://localhost:5000/api/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{"email": "user@example.com", "password": "SecurePass123", "first_name": "John", "last_name": "Doe"}'

# 2. Login to get token
curl -X POST http://localhost:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email": "user@example.com", "password": "SecurePass123"}'

# 3. Use token for protected endpoints
curl -X GET http://localhost:5000/api/auth/profile \\
  -H "Authorization: Bearer <your-jwt-token>"
```

## Customization and Extension

### Adding New Endpoints
When implementing new features:

1. **Add endpoint documentation** to `get_openapi_spec()` in `swagger_ui.py`
2. **Define request/response models** in the schemas section
3. **Include authentication requirements** for protected endpoints
4. **Add examples and descriptions** for better usability
5. **Update tags and organization** for logical grouping

### Example: Adding a Gear Endpoint
```python
"/api/gear": {
    "get": {
        "tags": ["Gear Management"],
        "summary": "List all available gear",
        "description": "Retrieve a paginated list of available gear items",
        "parameters": [
            {
                "name": "category",
                "in": "query",
                "description": "Filter by gear category",
                "schema": {"type": "string", "enum": ["camera", "lens", "lighting"]}
            }
        ],
        "responses": {
            "200": {
                "description": "List of gear items",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/GearListResponse"}
                    }
                }
            }
        }
    }
}
```

### Styling Customization
The Swagger UI includes custom CSS for WeRent branding:
- Custom color scheme with brand colors
- Enhanced topbar with application name
- Responsive design for mobile viewing
- Visual indicators for "Coming Soon" endpoints

## Development Workflow

### Documentation-First Approach
1. **Design API endpoints** in OpenAPI spec first
2. **Review with stakeholders** using ReDoc interface
3. **Test with Postman collection** before implementation
4. **Implement actual endpoints** matching the documented spec
5. **Validate implementation** against documentation

### Keeping Documentation in Sync
- **Update OpenAPI spec** when adding/modifying endpoints
- **Test documentation changes** in development environment
- **Review documentation** in pull requests
- **Validate examples** and schemas regularly

## Best Practices

### Documentation Quality
- **Comprehensive descriptions** for all endpoints
- **Realistic examples** in request/response schemas
- **Clear error handling** documentation
- **Consistent naming conventions** across the API

### Security Documentation
- **Clear authentication requirements** for each endpoint
- **Security scheme documentation** with examples
- **Permission level descriptions** (user vs admin)
- **Rate limiting information** when applicable

### Version Management
- **Semantic versioning** for API changes
- **Deprecation notices** for old endpoints
- **Migration guides** for breaking changes
- **Changelog maintenance** in documentation

## Troubleshooting

### Common Issues

#### 1. Documentation Not Loading
- Check Flask server is running on correct port
- Verify `swagger_bp` is registered in routes
- Check for Python import errors in swagger modules

#### 2. Authentication Not Working in Swagger UI
- Ensure JWT token format is correct: `Bearer <token>`
- Verify token is not expired
- Check token was obtained from `/api/auth/login`

#### 3. OpenAPI Spec Errors
- Validate JSON syntax in specification
- Check schema references are correct
- Ensure all required fields are documented

### Development Debugging
```bash
# Check if swagger blueprint is registered
curl -I http://localhost:5000/docs/

# Validate OpenAPI spec
curl http://localhost:5000/docs/openapi.json | python -m json.tool

# Test specific endpoint documentation
curl http://localhost:5000/docs/openapi.json | grep -A 10 "/api/auth/login"
```

## Future Enhancements

### Planned Features
- **API versioning support** (v1, v2, etc.)
- **Rate limiting documentation** 
- **Webhook documentation** for event notifications
- **SDK generation** from OpenAPI spec
- **Performance metrics** integration
- **API testing automation** with documented examples

### Integration Possibilities
- **CI/CD validation** of OpenAPI spec
- **Documentation generation** for external sites
- **Mock server generation** for frontend development
- **Client library generation** for multiple languages

## Conclusion

The WeRent API documentation system provides a comprehensive, professional, and developer-friendly way to explore, test, and integrate with the API. With multiple interfaces, live testing capabilities, and extensive customization options, it serves both current development needs and future growth requirements.

For questions or improvements to the documentation system, please refer to the [CONTRIBUTING.md](./CONTRIBUTING.md) file or contact the development team.
