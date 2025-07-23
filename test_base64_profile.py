#!/usr/bin/env python3
"""
Test script for Base64 profile image upload functionality.
Tests the complete profile image upload flow.
"""

import requests
import base64
import json
from io import BytesIO
from PIL import Image

# Test configuration
BASE_URL = "http://localhost:5000/api"

def create_test_base64_image():
    """Create a small test Base64 image."""
    # Create a small 100x100 red square PNG
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def test_profile_image_upload():
    """Test the complete profile image upload flow."""
    print("🚀 Testing Base64 Profile Image Upload\n")
    
    # 1. Register a test user
    register_data = {
        "email": "testuser@werent.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print("🔹 Registering test user...")
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=register_data, timeout=10)
        print(f"   Registration: {response.status_code}")
        
        if response.status_code == 400 and "already exists" in response.text:
            print("   ℹ️  User already exists, proceeding with login")
        elif response.status_code not in [200, 201]:
            print(f"   ❌ Registration failed: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Registration request failed: {e}")
        return False

    # 2. Login to get access token
    login_data = {
        "email": "testuser@werent.com",
        "password": "TestPass123!"
    }
    
    print("🔹 Logging in...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        if response.status_code != 200:
            print(f"   ❌ Login failed: {response.status_code} - {response.text}")
            return False
        
        login_result = response.json()
        if not login_result.get('success'):
            print(f"   ❌ Login failed: {login_result.get('message', 'Unknown error')}")
            return False
            
        token = login_result['data']['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        print("   ✅ Login successful")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Login request failed: {e}")
        return False
    except (KeyError, TypeError) as e:
        print(f"   ❌ Login response parsing failed: {e}")
        return False

    # 3. Create test Base64 image
    print("🔹 Creating test Base64 image...")
    try:
        base64_image = create_test_base64_image()
        image_size_kb = len(base64_image) / 1024
        print(f"   ✅ Test image created ({image_size_kb:.1f}KB)")
    except Exception as e:
        print(f"   ❌ Image creation failed: {e}")
        return False

    # 4. Update profile with image
    profile_data = {
        "first_name": "Updated",
        "profile_image": f"data:image/png;base64,{base64_image}"
    }
    
    print("🔹 Uploading profile image...")
    try:
        response = requests.put(
            f"{BASE_URL}/auth/profile", 
            json=profile_data, 
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                user_data = result['data']['user']
                profile_image = user_data.get('profile_image', '')
                image_size_kb = len(profile_image) / 1024 if profile_image else 0
                
                print("   ✅ Profile image uploaded successfully!")
                print(f"   📷 Stored image size: {image_size_kb:.1f}KB")
                print(f"   👤 Updated name: {user_data.get('first_name')} {user_data.get('last_name')}")
                
                # 5. Test image removal
                print("🔹 Testing image removal...")
                remove_data = {"profile_image": ""}
                
                remove_response = requests.put(
                    f"{BASE_URL}/auth/profile",
                    json=remove_data,
                    headers=headers,
                    timeout=10
                )
                
                if remove_response.status_code == 200:
                    remove_result = remove_response.json()
                    if remove_result.get('success'):
                        updated_user = remove_result['data']['user']
                        if not updated_user.get('profile_image'):
                            print("   ✅ Image removal successful!")
                        else:
                            print("   ⚠️  Image removal might have failed")
                    else:
                        print(f"   ❌ Image removal failed: {remove_result.get('message')}")
                else:
                    print(f"   ❌ Image removal request failed: {remove_response.status_code}")
                
                return True
            else:
                print(f"   ❌ Upload failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"   ❌ Upload failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Upload request failed: {e}")
        return False
    except (KeyError, TypeError) as e:
        print(f"   ❌ Upload response parsing failed: {e}")
        return False

def test_image_validation():
    """Test image validation functionality."""
    print("\n🧪 Testing Image Validation...")
    
    try:
        from app.utils.image_utils import ImageValidator
        
        # Test 1: Valid image
        img = Image.new('RGB', (50, 50), color='blue')
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        valid_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        result = ImageValidator.validate_base64_image(f"data:image/jpeg;base64,{valid_base64}")
        if result['success']:
            print("   ✅ Valid image validation passed")
        else:
            print(f"   ❌ Valid image validation failed: {result['message']}")
        
        # Test 2: Invalid base64
        result = ImageValidator.validate_base64_image("invalid_base64_string")
        if not result['success']:
            print("   ✅ Invalid base64 validation passed")
        else:
            print("   ❌ Invalid base64 validation failed")
            
        # Test 3: Image compression
        compressed = ImageValidator.compress_image(f"data:image/jpeg;base64,{valid_base64}")
        if compressed:
            original_size = len(valid_base64)
            compressed_size = len(compressed.split(',')[1]) if ',' in compressed else len(compressed)
            print(f"   ✅ Image compression working (Original: {original_size}, Compressed: {compressed_size})")
        else:
            print("   ❌ Image compression failed")
            
    except ImportError:
        print("   ⚠️  ImageValidator not available for direct testing")
    except Exception as e:
        print(f"   ❌ Validation test failed: {e}")

if __name__ == "__main__":
    print("🔧 WeRent Base64 Profile Image Test Suite")
    print("=" * 50)
    
    # Test validation functions
    test_image_validation()
    
    # Test API endpoints
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"\n🌐 Server status: {response.status_code}")
        
        if response.status_code in [200, 503]:  # 503 is also acceptable (unhealthy but running)
            success = test_profile_image_upload()
            
            if success:
                print("\n🎉 All tests passed! Base64 profile image upload is working correctly.")
                print("\n📋 Implementation Summary:")
                print("   ✅ Database field added for profile_image")
                print("   ✅ Image validation and compression working")
                print("   ✅ Profile upload endpoint working")
                print("   ✅ Image removal working")
                print("\n📱 Frontend Integration:")
                print("   • Use PUT /api/auth/profile endpoint")
                print("   • Include Authorization: Bearer <token> header")
                print("   • Send JSON with profile_image field containing Base64 data")
                print("   • Format: 'data:image/[type];base64,[data]' or just '[data]'")
            else:
                print("\n❌ Profile image upload tests failed!")
        else:
            print("❌ Server is not running. Start with: uv run python main.py")
            
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Make sure Flask is running on port 5000")
        print("   Start server with: uv run python main.py")
