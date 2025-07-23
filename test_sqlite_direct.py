#!/usr/bin/env python3
"""
Direct SQLite test for Base64 profile image upload.
Tests directly with Flask test client instead of running a separate server.
"""

import os
import sys
import json
import base64
import time
from io import BytesIO
from PIL import Image

# Set test environment before importing app
os.environ['DATABASE_URL'] = 'sqlite:///instance/werent-test.db'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key-for-testing'
os.environ['FLASK_SECRET_KEY'] = 'test-flask-secret-key-for-testing'
os.environ['FLASK_ENV'] = 'testing'

from app import create_app
from app.extensions import db

def create_test_base64_image(size=(150, 150), color=(0, 123, 255)):
    """Create a test Base64 image with specific parameters."""
    img = Image.new('RGB', size, color=color)
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=90)
    
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_data}"

def setup_test_database():
    """Initialize a clean test database."""
    print("🔧 Setting up test database...")
    
    test_db_path = "instance/werent-test.db"
    
    # Remove existing test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print("   ✅ Removed existing test database")
    
    # Create instance directory if it doesn't exist
    os.makedirs("instance", exist_ok=True)
    
    print(f"   📍 Database path: {test_db_path}")
    return True

def test_complete_flow():
    """Test the complete flow using Flask test client."""
    print("\n🧪 Testing complete Base64 profile image flow...")
    
    # Create Flask app
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("   ✅ Database tables created")
        
        # Create test client
        client = app.test_client()
        
        # Generate unique email for this test
        timestamp = int(time.time())
        test_email = f"testuser{timestamp}@werent.com"
        
        # Step 1: Test user registration
        print("\n👤 Testing user registration...")
        user_data = {
            "email": test_email,
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+1234567890"
        }
        
        response = client.post('/api/auth/signup', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        if response.status_code in [200, 201]:
            result = response.get_json()
            if result.get('success'):
                print("   ✅ User registration successful")
                user_id = result['data']['user']['id']
            else:
                print(f"   ❌ Registration failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Registration failed: {response.status_code} - {response.get_data(as_text=True)}")
            return False
        
        # Step 2: Test user login
        print("\n🔑 Testing user login...")
        login_data = {
            "email": test_email,
            "password": "TestPass123!"
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            result = response.get_json()
            if result.get('success'):
                token = result['data']['access_token']
                print("   ✅ Login successful")
            else:
                print(f"   ❌ Login failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Login failed: {response.status_code} - {response.get_data(as_text=True)}")
            return False
        
        # Step 3: Test profile image upload
        print("\n📷 Testing profile image upload...")
        test_image = create_test_base64_image()
        image_size_kb = len(test_image) / 1024
        print(f"   📊 Test image size: {image_size_kb:.1f}KB")
        
        profile_data = {
            "first_name": "Updated",
            "last_name": "TestUser",
            "profile_image": test_image
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.put('/api/auth/profile',
                            data=json.dumps(profile_data),
                            content_type='application/json',
                            headers=headers)
        
        if response.status_code == 200:
            result = response.get_json()
            if result.get('success'):
                user_data = result['data']['user']
                stored_image = user_data.get('profile_image', '')
                stored_size_kb = len(stored_image) / 1024 if stored_image else 0
                
                print("   ✅ Profile image upload successful!")
                print(f"   📊 Stored image size: {stored_size_kb:.1f}KB")
                print(f"   🔄 Compression ratio: {(image_size_kb - stored_size_kb) / image_size_kb * 100:.1f}%")
                print(f"   👤 Updated profile: {user_data.get('first_name')} {user_data.get('last_name')}")
            else:
                print(f"   ❌ Upload failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Upload failed: {response.status_code} - {response.get_data(as_text=True)}")
            return False
        
        # Step 4: Test profile retrieval
        print("\n📥 Testing profile retrieval...")
        
        response = client.get('/api/auth/profile', headers=headers)
        
        if response.status_code == 200:
            result = response.get_json()
            if result.get('success'):
                user_data = result['data']['user']
                profile_image = user_data.get('profile_image', '')
                
                if profile_image:
                    image_size_kb = len(profile_image) / 1024
                    print(f"   ✅ Profile image retrieved successfully!")
                    print(f"   📊 Retrieved image size: {image_size_kb:.1f}KB")
                    
                    # Verify it's valid Base64
                    if profile_image.startswith('data:image/'):
                        print("   ✅ Image has correct data URL format")
                    
                else:
                    print("   ❌ No profile image found in retrieved data")
                    return False
            else:
                print(f"   ❌ Retrieval failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Retrieval failed: {response.status_code} - {response.get_data(as_text=True)}")
            return False
        
        # Step 5: Verify database storage
        print("\n💾 Verifying database storage...")
        
        from app.models import User
        user = User.query.filter_by(email=test_email).first()
        
        if user and user.profile_image:
            image_size_kb = len(user.profile_image) / 1024
            print(f"   ✅ Found profile image in database for {user.email}")
            print(f"   📊 Database stored size: {image_size_kb:.1f}KB")
            
            if user.profile_image.startswith('data:image/'):
                print("   ✅ Stored data has correct format")
            else:
                print("   ⚠️  Stored data might be missing data URL prefix")
        else:
            print("   ❌ No profile images found in database")
            return False
        
        # Step 6: Test image removal
        print("\n🗑️  Testing profile image removal...")
        
        removal_data = {"profile_image": ""}
        
        response = client.put('/api/auth/profile',
                            data=json.dumps(removal_data),
                            content_type='application/json',
                            headers=headers)
        
        if response.status_code == 200:
            result = response.get_json()
            if result.get('success'):
                user_data = result['data']['user']
                profile_image = user_data.get('profile_image')
                
                if not profile_image:
                    print("   ✅ Profile image removed successfully!")
                else:
                    print("   ❌ Profile image still present after removal")
                    return False
            else:
                print(f"   ❌ Removal failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Removal failed: {response.status_code} - {response.get_data(as_text=True)}")
            return False
        
        print("\n🎉 All tests passed! Base64 profile image upload is working perfectly with SQLite!")
        return True

def main():
    """Run the complete test suite."""
    print("🧪 WeRent Base64 Profile Image Upload Test (SQLite - Direct)")
    print("=" * 65)
    
    if not setup_test_database():
        print("\n❌ Test aborted: Database setup failed")
        return False
    
    if test_complete_flow():
        print("\n📋 Test Summary:")
        print("   ✅ SQLite database setup")
        print("   ✅ User registration")
        print("   ✅ User authentication") 
        print("   ✅ Profile image upload")
        print("   ✅ Profile image retrieval")
        print("   ✅ Database storage verification")
        print("   ✅ Profile image removal")
        
        print("\n🚀 Ready for production use!")
        return True
    else:
        print("\n❌ Test failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
