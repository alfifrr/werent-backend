# Swagger Server Configuration

## Overview

The Swagger UI now includes both development and production server URLs in the server selection dropdown, allowing users to test the API against different environments directly from the documentation.

## Server URLs

### Development
- **URL:** `http://localhost:5000`
- **Description:** Development server (localhost)
- **Usage:** For local development and testing

### Production  
- **URL:** `https://werent-backend-api.onrender.com`
- **Description:** Production server (Render deployment)
- **Usage:** For production API testing

## Features

### 🔄 **Environment-Aware Ordering**
- **Development:** Localhost appears first in dropdown
- **Production:** Production server appears first in dropdown

### 📱 **Postman Collection Integration**
- Postman collection automatically uses the appropriate base URL
- Development: `http://localhost:5000`
- Production: `https://werent-backend-api.onrender.com`

### 🛠 **Easy Configuration**
Server URLs are centrally managed in `app/swagger/swagger_ui.py`:

```python
def get_server_urls():
    """Returns environment-appropriate server URLs"""
    # Development server
    servers.append({
        "url": "http://localhost:5000",
        "description": "Development server (localhost)"
    })
    
    # Production server
    production_url = "https://werent-backend-api.onrender.com"
    servers.append({
        "url": production_url,
        "description": "Production server (Render deployment)"
    })
```

## Usage

### 📖 **Swagger Documentation Access**
- **Development:** http://localhost:5000/docs
- **Production:** https://werent-backend-api.onrender.com/docs

### 🎯 **Server Selection**
1. Open Swagger UI documentation
2. Look for the "Servers" dropdown at the top
3. Select desired environment:
   - `http://localhost:5000` for development
   - `https://werent-backend-api.onrender.com` for production
4. All API calls will now use the selected server

### 📋 **Postman Collection**
- **Download:** Visit `/docs/postman` endpoint
- **Base URL:** Automatically configured based on environment
- **Variables:** Pre-configured with `baseUrl`, `accessToken`, `refreshToken`

## Environment Variables

The configuration automatically detects the environment using:

```bash
FLASK_ENV=production  # For production
FLASK_ENV=development # For development (default)
```

## Best Practices

### ✅ **Benefits**
- Users can test against both environments without changing URLs
- Documentation stays synchronized with deployment
- Postman collections work out-of-the-box
- Environment-specific defaults improve UX

### 🔧 **Maintenance**
- Update production URL in `get_server_urls()` function
- Environment detection is automatic
- No need to manually update multiple places

## Testing

The configuration can be tested locally:

```python
# Test in different environments
os.environ['FLASK_ENV'] = 'development'  # localhost first
os.environ['FLASK_ENV'] = 'production'   # production first
```

---

**✅ Server configuration complete!** 

Users can now switch between development and production APIs directly from the Swagger UI dropdown.
