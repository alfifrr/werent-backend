# Profile Image Update Documentation

## Overview

The WeRent Backend API provides profile image upload functionality using Base64 encoding. This endpoint allows authenticated users to upload and update their profile images with automatic compression and optimization.

## Authentication

This endpoint requires:
- **JWT Authentication**: Valid access token in `Authorization: Bearer <token>` header

## Base URL

- **Development**: `http://localhost:5000/api/auth`
- **Production**: `https://api.werent.com/api/auth`

---

## Profile Image Update Endpoint

### Update Profile Image

**Endpoint**: `PUT /api/auth/profile/image`

**Description**: Upload and update user profile image using Base64 encoded image data.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "profile_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/4A=="
}
```

**Parameters**:
- `profile_image` (string, required): Base64 encoded image data with data URI prefix

**Image Requirements**:
- **Supported Formats**: JPEG, PNG, WebP
- **Size Limit**: Maximum 10MB (base64 encoded)
- **Encoding**: Must be valid Base64 with data URI prefix
- **Format Example**: `data:image/jpeg;base64,<base64_data>`

**Success Response** (200):
```json
{
  "success": true,
  "message": "Profile image updated successfully",
  "data": {
    "user": {
      "id": 26,
      "email": "user@werent.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "+1234567890",
      "is_admin": false,
      "is_verified": false,
      "is_active": true,
      "uuid": "56e0fbfa-99a3-4999-be0f-c97692cf8650",
      "created_at": "Wed, 23 Jul 2025 23:19:35 GMT",
      "updated_at": "Wed, 23 Jul 2025 23:30:12 GMT",
      "profile_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD..."
    },
    "image_info": {
      "original_size": 1048576,
      "compressed_size": 442250,
      "compression_ratio": "58% reduction",
      "format": "JPEG",
      "dimensions": "800x600"
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
      "profile_image": ["Profile image is required"]
    }
  }
}
```

*Invalid Image Format (400)*:
```json
{
  "success": false,
  "error": "Invalid image format or data",
  "error_code": "INVALID_IMAGE",
  "details": {
    "message": "Unsupported image format. Supported formats: JPEG, PNG, WebP"
  }
}
```

*Authentication Required (401)*:
```json
{
  "success": false,
  "error": "Authentication required",
  "error_code": "UNAUTHORIZED"
}
```

---

## Image Processing Features

### Automatic Compression
- **Smart Compression**: Automatically reduces file size while maintaining quality
- **Typical Reduction**: 40-60% size reduction
- **Quality Optimization**: Maintains visual quality for web display
- **Format Preservation**: Keeps original format (JPEG, PNG, WebP)

### Validation & Security
- **Format Validation**: Ensures uploaded data is a valid image
- **Size Limits**: Prevents oversized uploads
- **Data Sanitization**: Validates Base64 encoding
- **Error Handling**: Comprehensive error messages for troubleshooting

### Response Information
The successful response includes detailed information about the image processing:
- `original_size`: Size of the uploaded image in bytes
- `compressed_size`: Size after compression in bytes
- `compression_ratio`: Percentage reduction achieved
- `format`: Detected image format (JPEG, PNG, WebP)
- `dimensions`: Image width and height

---

## Usage Examples

### JavaScript/Frontend Integration

```javascript
// Function to convert file to base64
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

// Upload profile image
async function uploadProfileImage(imageFile, token) {
  try {
    // Convert file to base64
    const base64Image = await fileToBase64(imageFile);
    
    // Send to API
    const response = await fetch('/api/auth/profile/image', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        profile_image: base64Image
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Image uploaded successfully:', result.data.image_info);
      return result.data.user;
    } else {
      console.error('Upload failed:', result.error);
      return null;
    }
  } catch (error) {
    console.error('Upload error:', error);
    return null;
  }
}

// Usage
const fileInput = document.getElementById('imageInput');
const token = localStorage.getItem('authToken');

fileInput.addEventListener('change', async (event) => {
  const file = event.target.files[0];
  if (file) {
    const updatedUser = await uploadProfileImage(file, token);
    if (updatedUser) {
      // Update UI with new profile image
      document.getElementById('profileImg').src = updatedUser.profile_image;
    }
  }
});
```

### Curl Example

```bash
# Get authentication token
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@werent.com", "password": "UserPass123!"}' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print(data['data']['access_token'])")

# Upload profile image (example with small test image)
curl -X PUT http://localhost:5000/api/auth/profile/image \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/4A=="
  }'
```

### Python Example

```python
import base64
import requests
from PIL import Image
from io import BytesIO

def upload_profile_image(image_path, token, api_url="http://localhost:5000"):
    """Upload profile image using Python."""
    
    # Read and encode image
    with open(image_path, 'rb') as image_file:
        # Convert to base64
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Detect image format
        with Image.open(image_path) as img:
            format_name = img.format.lower()
            
        # Create data URI
        data_uri = f"data:image/{format_name};base64,{image_data}"
    
    # Prepare request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'profile_image': data_uri
    }
    
    # Send request
    response = requests.put(
        f"{api_url}/api/auth/profile/image",
        json=payload,
        headers=headers
    )
    
    return response.json()

# Usage
token = "your_jwt_token_here"
result = upload_profile_image("profile.jpg", token)

if result.get('success'):
    print("Upload successful!")
    print(f"Compression: {result['data']['image_info']['compression_ratio']}")
else:
    print(f"Upload failed: {result.get('error')}")
```

---

## Error Handling

### Common Error Scenarios

1. **Invalid Base64 Data**:
   - Missing data URI prefix (`data:image/...;base64,`)
   - Corrupted Base64 encoding
   - Non-image data

2. **Unsupported Format**:
   - Image formats other than JPEG, PNG, WebP
   - Invalid or corrupted image files

3. **Size Limitations**:
   - Base64 encoded data exceeding 10MB limit
   - Empty or missing image data

4. **Authentication Issues**:
   - Missing Authorization header
   - Invalid or expired JWT token
   - Malformed token format

### Best Practices

1. **Client-Side Validation**:
   - Check file type before upload
   - Validate file size limits
   - Preview image before sending

2. **Error Handling**:
   - Implement retry logic for network errors
   - Show user-friendly error messages
   - Log detailed errors for debugging

3. **Performance**:
   - Compress images client-side when possible
   - Show upload progress for large files
   - Cache uploaded images locally

4. **Security**:
   - Validate JWT tokens properly
   - Sanitize file inputs
   - Implement rate limiting for uploads

---

## Database Storage

Profile images are stored as Base64 encoded strings in the `users` table:

```sql
-- User table structure (relevant fields)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    profile_image TEXT,  -- Base64 encoded image data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Storage Considerations**:
- **Base64 Overhead**: ~33% larger than binary storage
- **Database Size**: Monitor database growth with image uploads
- **Query Performance**: Consider indexing strategies for large datasets
- **Backup**: Ensure backups include Base64 image data

---

## Integration with Frontend

### React Integration Example

```jsx
import React, { useState } from 'react';

const ProfileImageUpload = ({ userToken, onImageUpdate }) => {
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState(null);

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Create preview
    const previewUrl = URL.createObjectURL(file);
    setPreview(previewUrl);

    // Upload image
    setUploading(true);
    try {
      const base64 = await fileToBase64(file);
      const response = await fetch('/api/auth/profile/image', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${userToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ profile_image: base64 })
      });

      const result = await response.json();
      
      if (result.success) {
        onImageUpdate(result.data.user);
        console.log('Compression achieved:', result.data.image_info.compression_ratio);
      } else {
        alert('Upload failed: ' + result.error);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed');
    } finally {
      setUploading(false);
      URL.revokeObjectURL(previewUrl);
    }
  };

  return (
    <div className="profile-image-upload">
      <input
        type="file"
        accept="image/jpeg,image/png,image/webp"
        onChange={handleFileSelect}
        disabled={uploading}
      />
      {preview && (
        <img src={preview} alt="Preview" style={{ maxWidth: '200px' }} />
      )}
      {uploading && <p>Uploading...</p>}
    </div>
  );
};
```

---

## Security Considerations

1. **Authentication**: Always verify JWT tokens
2. **Input Validation**: Validate Base64 format and image data
3. **File Type Verification**: Ensure uploaded data is actually an image
4. **Size Limits**: Prevent DoS attacks through large uploads
5. **Rate Limiting**: Implement upload frequency limits
6. **Content Scanning**: Consider malware scanning for production

## Performance Optimization

1. **Compression**: Automatic server-side compression reduces storage
2. **Caching**: Implement CDN or caching for profile images
3. **Async Processing**: Consider background processing for large images
4. **Database Optimization**: Monitor query performance with Base64 data

## Testing

The profile image upload endpoint has been thoroughly tested with:
- ✅ Valid JPEG images
- ✅ Valid PNG images
- ✅ Base64 encoding validation
- ✅ Authentication requirements
- ✅ Compression functionality
- ✅ Error handling scenarios
- ✅ Database persistence
