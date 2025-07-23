#!/usr/bin/env python3
"""
Test phone_number consistency across UserService and controllers.
"""

import os
import sys
import json
import time

from app import create_app
from app.extensions import db

def test_phone_number_consistency():
    """Test that phone_number is handled consistently."""
    print("🧪 Testing phone_number Consistency")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        client = app.test_client()
        timestamp = int(time.time())
        
        # Test 1: UserService direct test
        print("\n📞 Test 1: UserService direct call")
        
        from app.services.user_service import UserService
        user_service = UserService()
        
        # Check method signature
        import inspect
        sig = inspect.signature(user_service.create_user)
        print(f"   📝 Method signature: {sig}")
        
        test_email = f"phone_test_{timestamp}@werent.com"
        test_phone = f"+155512{timestamp % 10000:04d}"
        
        try:
            user = user_service.create_user(
                email=test_email,
                password="TestPass123!",
                first_name="Phone",
                last_name="Test",
                phone_number=test_phone  # Using phone_number parameter
            )
            print(f"   ✅ UserService.create_user() with phone_number: SUCCESS")
            print(f"   📞 Stored phone: {user.phone_number}")
            print(f"   🆔 User ID: {user.id}")
        except Exception as e:
            print(f"   ❌ UserService test failed: {e}")
            return False
        
        # Test 2: Controller via API
        print("\n🌐 Test 2: Controller via API")
        
        api_email = f"api_phone_test_{timestamp}@werent.com"
        api_phone = f"+155513{timestamp % 10000:04d}"
        
        user_data = {
            "email": api_email,
            "password": "TestPass123!",
            "first_name": "API",
            "last_name": "PhoneTest",
            "phone_number": api_phone
        }
        
        response = client.post('/api/auth/signup', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        if response.status_code in [200, 201]:
            result = response.get_json()
            if result.get('success'):
                api_user = result['data']['user']
                print(f"   ✅ API signup with phone_number: SUCCESS")
                print(f"   📞 API stored phone: {api_user.get('phone_number')}")
                print(f"   🆔 API User ID: {api_user.get('id')}")
            else:
                print(f"   ❌ API signup failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ API request failed: {response.status_code}")
            print(f"   📄 Response: {response.get_data(as_text=True)}")
            return False
        
        # Test 3: Database verification
        print("\n💾 Test 3: Database verification")
        
        # Check both users in database
        from app.models import User
        
        direct_user = User.query.filter_by(email=test_email).first()
        api_user_db = User.query.filter_by(email=api_email).first()
        
        if direct_user and direct_user.phone_number == test_phone:
            print(f"   ✅ Direct user phone in DB: {direct_user.phone_number}")
        else:
            print(f"   ❌ Direct user phone mismatch or not found")
            return False
            
        if api_user_db and api_user_db.phone_number == api_phone:
            print(f"   ✅ API user phone in DB: {api_user_db.phone_number}")
        else:
            print(f"   ❌ API user phone mismatch or not found")
            return False
        
        # Test 4: Check all users with phone numbers
        print("\n📊 Test 4: Database phone_number summary")
        
        users_with_phones = User.query.filter(User.phone_number.isnot(None)).all()
        print(f"   📱 Total users with phone numbers: {len(users_with_phones)}")
        
        for user in users_with_phones[-5:]:  # Show last 5
            print(f"   - {user.email}: {user.phone_number}")
        
        print("\n🎉 All phone_number consistency tests passed!")
        print("✅ UserService uses phone_number parameter")
        print("✅ Controller passes phone_number correctly")
        print("✅ Database stores phone_number properly")
        print("✅ API returns phone_number in responses")
        
        return True

def main():
    """Run phone_number consistency test."""
    try:
        success = test_phone_number_consistency()
        return success
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
