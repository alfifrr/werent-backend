#!/usr/bin/env python3
"""
Detailed inspection test for Base64 profile image upload.
This test will specifically examine database storage and image persistence.
"""

import os
import sys
import json
import base64
import sqlite3
import time
from io import BytesIO
from PIL import Image

# Set test environment
test_db_path = "instance/werent-detailed-test.db"
os.environ['DATABASE_URL'] = f'sqlite:///{test_db_path}'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key-for-testing'
os.environ['FLASK_SECRET_KEY'] = 'test-flask-secret-key-for-testing'
os.environ['FLASK_ENV'] = 'testing'

from app import create_app
from app.extensions import db

def create_test_base64_image(size=(100, 100), color=(255, 0, 0)):
    """Create a test Base64 image."""
    img = Image.new('RGB', size, color=color)
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_data}"

def inspect_database_directly():
    """Inspect the SQLite database directly."""
    print("\n🔍 Direct Database Inspection:")
    
    db_path = "instance/werent-detailed-test.db"
    
    if not os.path.exists(db_path):
        print("   ❌ Test database doesn't exist")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute("SELECT id, email, first_name, last_name, profile_image FROM users")
        users = cursor.fetchall()
        
        print(f"   📊 Found {len(users)} users in database:")
        
        for user in users:
            user_id, email, first_name, last_name, profile_image = user
            image_status = "❌ NULL" if profile_image is None else f"✅ {len(profile_image)} chars"
            print(f"   - User {user_id}: {email} | Image: {image_status}")
            
            if profile_image:
                # Check if it's valid Base64
                if profile_image.startswith('data:image/'):
                    print(f"     📸 Valid data URL format")
                    print(f"     📏 Image size: {len(profile_image) / 1024:.1f}KB")
                else:
                    print(f"     ⚠️  Invalid format: {profile_image[:50]}...")
        
        conn.close()
        return len(users) > 0
        
    except Exception as e:
        print(f"   ❌ Database inspection failed: {e}")
        return False

def test_detailed_flow():
    """Test with detailed logging at each step."""
    print("\n🧪 Detailed Base64 Profile Image Test:")
    
    # Ensure clean test database path
    test_db_path = "instance/werent-detailed-test.db"
    
    # Set environment variables BEFORE creating app
    os.environ['DATABASE_URL'] = f'sqlite:///{test_db_path}'
    
    app = create_app()
    app.config['TESTING'] = True
    
    # Verify the database URL is correct
    print(f"   🔧 Database URL: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    with app.app_context():
        # Clean database
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print(f"   🗑️  Removed existing test database: {test_db_path}")
        
        db.drop_all()
        db.create_all()
        print("   ✅ Fresh database created")
        
        client = app.test_client()
        timestamp = int(time.time())
        test_email = f"detailed{timestamp}@werent.com"
        
        # Step 1: Register user
        print("\n📝 Step 1: User Registration")
        user_data = {
            "email": test_email,
            "password": "TestPass123!",
            "first_name": "Detailed",
            "last_name": "Test",
            "phone_number": "+1234567890"
        }
        
        response = client.post('/api/auth/signup', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        if response.status_code in [200, 201]:
            result = response.get_json()
            user_id = result['data']['user']['id']
            print(f"   ✅ User created with ID: {user_id}")
            print(f"   📧 Email: {test_email}")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            return False
        
        # Check database after registration
        inspect_database_directly()
        
        # Step 2: Login
        print("\n🔐 Step 2: User Login")
        login_data = {"email": test_email, "password": "TestPass123!"}
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            result = response.get_json()
            token = result['data']['access_token']
            print(f"   ✅ Login successful, token length: {len(token)}")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
        
        # Step 3: Upload profile image
        print("\n📸 Step 3: Profile Image Upload")
        test_image = create_test_base64_image()
        original_size = len(test_image)
        print(f"   📏 Original image size: {original_size / 1024:.1f}KB")
        
        profile_data = {
            "first_name": "DetailedUpdated",
            "profile_image": test_image
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        
        print("   📤 Sending profile update request...")
        response = client.put('/api/auth/profile',
                            data=json.dumps(profile_data),
                            content_type='application/json',
                            headers=headers)
        
        print(f"   📨 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.get_json()
            print(f"   📋 Response success: {result.get('success')}")
            
            if result.get('success'):
                user_data = result['data']['user']
                stored_image = user_data.get('profile_image')
                
                if stored_image:
                    stored_size = len(stored_image)
                    compression = (original_size - stored_size) / original_size * 100
                    print(f"   ✅ Image upload successful!")
                    print(f"   📏 Stored size: {stored_size / 1024:.1f}KB")
                    print(f"   🗜️  Compression: {compression:.1f}%")
                    print(f"   🔗 Format check: {'✅' if stored_image.startswith('data:image/') else '❌'}")
                else:
                    print("   ❌ No profile image in response!")
                    print(f"   📄 Full response: {json.dumps(result, indent=2)}")
                    return False
            else:
                print(f"   ❌ Upload failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Upload request failed: {response.get_data(as_text=True)}")
            return False
        
        # Step 4: Check database immediately after upload
        print("\n💾 Step 4: Database Check After Upload")
        inspect_database_directly()
        
        # Step 5: Retrieve profile
        print("\n📥 Step 5: Profile Retrieval")
        response = client.get('/api/auth/profile', headers=headers)
        
        if response.status_code == 200:
            result = response.get_json()
            if result.get('success'):
                user_data = result['data']['user']
                retrieved_image = user_data.get('profile_image')
                
                if retrieved_image:
                    print(f"   ✅ Profile retrieved successfully!")
                    print(f"   📏 Retrieved size: {len(retrieved_image) / 1024:.1f}KB")
                    print(f"   🔗 Format: {'✅' if retrieved_image.startswith('data:image/') else '❌'}")
                else:
                    print("   ❌ No profile image in retrieved data!")
                    return False
            else:
                print(f"   ❌ Retrieval failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Retrieval request failed: {response.status_code}")
            return False
        
        # Step 6: Final database inspection
        print("\n🔍 Step 6: Final Database Inspection")
        inspect_database_directly()
        
        # Step 7: Test with Flask ORM
        print("\n🗄️  Step 7: ORM Database Check")
        from app.models import User
        
        user = User.query.filter_by(email=test_email).first()
        if user:
            print(f"   ✅ User found via ORM: {user.email}")
            if user.profile_image:
                print(f"   ✅ Profile image exists in ORM: {len(user.profile_image) / 1024:.1f}KB")
                print(f"   🔗 Format: {'✅' if user.profile_image.startswith('data:image/') else '❌'}")
            else:
                print("   ❌ No profile image in ORM!")
                return False
        else:
            print("   ❌ User not found via ORM!")
            return False
        
        print("\n🎉 All detailed tests passed!")
        return True

def main():
    """Run detailed inspection test."""
    print("🔬 WeRent Base64 Profile Image - Detailed Inspection Test")
    print("=" * 70)
    
    success = test_detailed_flow()
    
    if success:
        print("\n✅ SUCCESS: Profile image upload is working correctly!")
        print("   📊 Database storage confirmed")
        print("   🔄 API endpoints working") 
        print("   🗄️  ORM integration verified")
    else:
        print("\n❌ FAILURE: Issues detected with profile image upload")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
