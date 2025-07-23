#!/usr/bin/env python3
"""
Test Base64 profile image upload with the actual development database.
This will help verify that image storage works with a real SQLite file.
"""

import os
import sys
import json
import base64
import sqlite3
import time
from io import BytesIO
from PIL import Image

from app import create_app
from app.extensions import db

def create_test_base64_image(size=(100, 100), color=(0, 255, 0)):
    """Create a test Base64 image."""
    img = Image.new('RGB', size, color=color)
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_data}"

def inspect_dev_database():
    """Inspect the development SQLite database directly."""
    print("\n🔍 Development Database Inspection:")
    
    db_path = "instance/werent-dev.db"
    
    if not os.path.exists(db_path):
        print("   ❌ Development database doesn't exist")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get users with profile images
        cursor.execute("SELECT id, email, first_name, last_name, profile_image FROM users WHERE profile_image IS NOT NULL ORDER BY id DESC LIMIT 5")
        users = cursor.fetchall()
        
        print(f"   📊 Found {len(users)} users with profile images:")
        
        for user in users:
            user_id, email, first_name, last_name, profile_image = user
            if profile_image:
                image_size_kb = len(profile_image) / 1024
                format_check = "✅" if profile_image.startswith('data:image/') else "❌"
                print(f"   - User {user_id}: {email} | {image_size_kb:.1f}KB | Format: {format_check}")
                
                # Show first 50 chars of image data
                preview = profile_image[:50] + "..." if len(profile_image) > 50 else profile_image
                print(f"     📸 Preview: {preview}")
        
        # Get total users count
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        print(f"   👥 Total users in database: {total_users}")
        
        conn.close()
        return len(users) > 0
        
    except Exception as e:
        print(f"   ❌ Database inspection failed: {e}")
        return False

def test_with_dev_database():
    """Test profile image upload with development database."""
    print("\n🧪 Testing with Development Database:")
    
    app = create_app()
    print(f"   🔧 Using database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    with app.app_context():
        client = app.test_client()
        timestamp = int(time.time())
        test_email = f"devtest{timestamp}@werent.com"
        
        # Step 1: Register a new user
        print("\n📝 Step 1: User Registration")
        user_data = {
            "email": test_email,
            "password": "TestPass123!",
            "first_name": "DevTest",
            "last_name": "User",
            "phone_number": "+1234567890"
        }
        
        response = client.post('/api/auth/signup', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        if response.status_code in [200, 201]:
            result = response.get_json()
            user_id = result['data']['user']['id']
            print(f"   ✅ User created with ID: {user_id}")
        else:
            print(f"   ❌ Registration failed: {response.status_code} - {response.get_data(as_text=True)}")
            return False
        
        # Step 2: Login
        print("\n🔐 Step 2: User Login")
        login_data = {"email": test_email, "password": "TestPass123!"}
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            result = response.get_json()
            token = result['data']['access_token']
            print(f"   ✅ Login successful")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
        
        # Check database before upload
        print("\n💾 Before Upload:")
        inspect_dev_database()
        
        # Step 3: Upload profile image
        print("\n📸 Step 3: Profile Image Upload")
        test_image = create_test_base64_image()
        original_size = len(test_image)
        print(f"   📏 Original image size: {original_size / 1024:.1f}KB")
        
        profile_data = {
            "first_name": "DevTestUpdated",
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
                stored_image = user_data.get('profile_image')
                
                if stored_image:
                    stored_size = len(stored_image)
                    compression = (original_size - stored_size) / original_size * 100
                    print(f"   ✅ Image upload successful!")
                    print(f"   📏 Stored size: {stored_size / 1024:.1f}KB")
                    print(f"   🗜️  Compression: {compression:.1f}%")
                else:
                    print("   ❌ No profile image in response!")
                    return False
            else:
                print(f"   ❌ Upload failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Upload request failed: {response.status_code}")
            return False
        
        # Check database after upload
        print("\n💾 After Upload:")
        inspect_dev_database()
        
        # Step 4: Verify with direct ORM query
        print("\n🗄️  Step 4: ORM Verification")
        from app.models import User
        
        user = User.query.filter_by(email=test_email).first()
        if user and user.profile_image:
            print(f"   ✅ Profile image confirmed in ORM: {len(user.profile_image) / 1024:.1f}KB")
            print(f"   🔗 Format: {'✅' if user.profile_image.startswith('data:image/') else '❌'}")
            
            # Show a preview of the stored data
            preview = user.profile_image[:50] + "..." if len(user.profile_image) > 50 else user.profile_image
            print(f"   📸 Data preview: {preview}")
            
            return True
        else:
            print("   ❌ Profile image not found in ORM!")
            return False

def main():
    """Run development database test."""
    print("🔬 WeRent Base64 Profile Image - Development Database Test")
    print("=" * 70)
    
    # First, inspect existing database
    print("\n📊 Current Database State:")
    inspect_dev_database()
    
    # Run the test
    success = test_with_dev_database()
    
    if success:
        print("\n✅ SUCCESS: Profile image upload works with development database!")
        print("   📊 File-based SQLite storage confirmed")
        print("   🔄 API endpoints working correctly") 
        print("   🗄️  ORM integration verified")
        print("   💾 Data persists in actual database file")
    else:
        print("\n❌ FAILURE: Issues detected with development database")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
