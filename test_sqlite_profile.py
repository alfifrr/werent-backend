#!/usr/bin/env python3
"""
Comprehensive test for Base64 profile image upload with SQLite database.
Tests the complete flow: registration, login, profile upload, and image retrieval.
"""

import os
import sys
import requests
import base64
import json
import time
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load test environment
load_dotenv('.env.test')

# Test configuration
BASE_URL = "http://localhost:5000/api"
TEST_DB_PATH = "instance/werent-test.db"

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
    
    # Remove existing test database
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
        print("   ✅ Removed existing test database")
    
    # Create instance directory if it doesn't exist
    os.makedirs("instance", exist_ok=True)
    
    # Set environment variable before importing app
    os.environ['DATABASE_URL'] = f'sqlite:///{TEST_DB_PATH}'
    os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key-for-testing'
    os.environ['FLASK_SECRET_KEY'] = 'test-flask-secret-key-for-testing'
    
    # Initialize database with Flask app
    try:
        # Import Flask app to create tables
        sys.path.append('.')
        from app import create_app
        
        app = create_app()
        with app.app_context():
            from app.extensions import db
            db.create_all()
            print("   ✅ Test database created with all tables")
            print(f"   📍 Database path: {TEST_DB_PATH}")
            
        return True
    except Exception as e:
        print(f"   ❌ Database setup failed: {e}")
        return False

def start_test_server():
    """Start Flask server for testing."""
    print("🚀 Starting test server...")
    
    import subprocess
    import time
    
    # Start server in background with proper environment
    env = os.environ.copy()
    env.update({
        'DATABASE_URL': f'sqlite:///{TEST_DB_PATH}',
        'JWT_SECRET_KEY': 'test-jwt-secret-key-for-testing',
        'FLASK_SECRET_KEY': 'test-flask-secret-key-for-testing',
        'FLASK_ENV': 'development',
        'DEBUG': 'True'
    })
    
    process = subprocess.Popen(
        ['uv', 'run', 'python', 'main.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code in [200, 503]:  # 503 is also acceptable
                print("   ✅ Test server started successfully")
                return process
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        print(f"   ⏳ Waiting for server... ({attempt + 1}/{max_attempts})")
    
    print("   ❌ Server failed to start")
    process.kill()
    return None

def test_user_registration():
    """Test user registration."""
    print("\n👤 Testing user registration...")
    
    import time
    timestamp = int(time.time())
    
    user_data = {
        "email": f"testuser{timestamp}@werent.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=user_data, timeout=10)
        
        if response.status_code in [200, 201]:
            result = response.json()
            if result.get('success'):
                print("   ✅ User registration successful")
                return True, user_data
            else:
                print(f"   ❌ Registration failed: {result.get('message')}")
                return False, None
        else:
            print(f"   ❌ Registration failed: {response.status_code} - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False, None

def test_user_login(user_data):
    """Test user login and get access token."""
    print("\n🔑 Testing user login...")
    
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                token = result['data']['access_token']
                print("   ✅ Login successful")
                return True, token
            else:
                print(f"   ❌ Login failed: {result.get('message')}")
                return False, None
        else:
            print(f"   ❌ Login failed: {response.status_code} - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False, None

def test_profile_image_upload(token):
    """Test profile image upload."""
    print("\n📷 Testing profile image upload...")
    
    # Create test image
    test_image = create_test_base64_image()
    image_size_kb = len(test_image) / 1024
    print(f"   📊 Test image size: {image_size_kb:.1f}KB")
    
    profile_data = {
        "first_name": "Updated",
        "last_name": "TestUser",
        "profile_image": test_image
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
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
                stored_image = user_data.get('profile_image', '')
                stored_size_kb = len(stored_image) / 1024 if stored_image else 0
                
                print("   ✅ Profile image upload successful!")
                print(f"   📊 Stored image size: {stored_size_kb:.1f}KB")
                print(f"   👤 Updated profile: {user_data.get('first_name')} {user_data.get('last_name')}")
                
                return True, user_data
            else:
                print(f"   ❌ Upload failed: {result.get('message')}")
                return False, None
        else:
            print(f"   ❌ Upload failed: {response.status_code} - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"   ❌ Upload error: {e}")
        return False, None

def test_profile_retrieval(token):
    """Test profile retrieval to verify image is stored."""
    print("\n📥 Testing profile retrieval...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
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
                    
                    return True, user_data
                else:
                    print("   ❌ No profile image found in retrieved data")
                    return False, None
            else:
                print(f"   ❌ Retrieval failed: {result.get('message')}")
                return False, None
        else:
            print(f"   ❌ Retrieval failed: {response.status_code} - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"   ❌ Retrieval error: {e}")
        return False, None

def test_image_removal(token):
    """Test profile image removal."""
    print("\n🗑️  Testing profile image removal...")
    
    removal_data = {"profile_image": ""}
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.put(
            f"{BASE_URL}/auth/profile",
            json=removal_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                user_data = result['data']['user']
                profile_image = user_data.get('profile_image')
                
                if not profile_image:
                    print("   ✅ Profile image removed successfully!")
                    return True
                else:
                    print("   ❌ Profile image still present after removal")
                    return False
            else:
                print(f"   ❌ Removal failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Removal failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Removal error: {e}")
        return False

def verify_database_storage():
    """Verify image is actually stored in SQLite database."""
    print("\n💾 Verifying database storage...")
    
    try:
        import sqlite3
        
        # Connect to test database
        conn = sqlite3.connect(TEST_DB_PATH)
        cursor = conn.cursor()
        
        # Query for users with profile images
        cursor.execute("SELECT email, profile_image FROM users WHERE profile_image IS NOT NULL")
        rows = cursor.fetchall()
        
        if rows:
            email, profile_image = rows[0]
            image_size_kb = len(profile_image) / 1024
            print(f"   ✅ Found profile image in database for {email}")
            print(f"   📊 Database stored size: {image_size_kb:.1f}KB")
            
            # Verify it's valid Base64
            if profile_image.startswith('data:image/'):
                print("   ✅ Stored data has correct format")
            else:
                print("   ⚠️  Stored data might be missing data URL prefix")
                
            conn.close()
            return True
        else:
            print("   ❌ No profile images found in database")
            conn.close()
            return False
            
    except Exception as e:
        print(f"   ❌ Database verification error: {e}")
        return False

def main():
    """Run the complete test suite."""
    print("🧪 WeRent Base64 Profile Image Upload Test (SQLite)")
    print("=" * 60)
    
    # Step 1: Setup test database
    if not setup_test_database():
        print("\n❌ Test aborted: Database setup failed")
        return False
    
    # Step 2: Start test server
    server_process = start_test_server()
    if not server_process:
        print("\n❌ Test aborted: Server startup failed")
        return False
    
    try:
        # Wait a bit more for server to be fully ready
        time.sleep(2)
        
        # Step 3: Test user registration
        reg_success, user_data = test_user_registration()
        if not reg_success:
            return False
        
        # Step 4: Test user login
        login_success, token = test_user_login(user_data)
        if not login_success:
            return False
        
        # Step 5: Test profile image upload
        upload_success, uploaded_data = test_profile_image_upload(token)
        if not upload_success:
            return False
        
        # Step 6: Test profile retrieval
        retrieval_success, retrieved_data = test_profile_retrieval(token)
        if not retrieval_success:
            return False
        
        # Step 7: Verify database storage
        db_success = verify_database_storage()
        if not db_success:
            return False
        
        # Step 8: Test image removal
        removal_success = test_image_removal(token)
        if not removal_success:
            return False
        
        print("\n🎉 All tests passed! Base64 profile image upload is working perfectly with SQLite!")
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
        
    finally:
        # Clean up
        print("\n🧹 Cleaning up...")
        if server_process:
            server_process.kill()
            print("   ✅ Test server stopped")
        
        # Optionally remove test database
        # if os.path.exists(TEST_DB_PATH):
        #     os.remove(TEST_DB_PATH)
        #     print("   ✅ Test database cleaned up")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
