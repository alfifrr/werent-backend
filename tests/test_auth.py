import pytest
from unittest.mock import patch

# pytest tests/test_auth.py -v -s --cov=. --cov-report term-missing

# --- Registration ---
def test_signup_success(client, db):
    payload = {
        'email': 'newuser@werent.com',
        'password': 'ValidPass123',
        'first_name': 'New',
        'last_name': 'User',
        'phone_number': '0812345678',
    }
    resp = client.post('/api/auth/signup', json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['success'] is True
    assert 'user' in data['data']
    assert data['data']['user']['email'] == payload['email']
    assert data['data']['user']['is_verified'] is False

@pytest.mark.parametrize('field,value,err', [
    ('email', 'notanemail', 'value is not a valid email address'),
    ('password', 'short', 'at least 8 characters'),
    ('first_name', '', 'String should have at least 1 character'),
    ('last_name', '', 'String should have at least 1 character'),
    ('phone_number', '123', 'between 10-15 digits'),
])
def test_signup_invalid_fields(client, db, field, value, err):
    payload = {
        'email': 'user@werent.com',
        'password': 'ValidPass123',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '0812345678',
    }
    payload[field] = value
    resp = client.post('/api/auth/signup', json=payload)
    assert resp.status_code in (400, 422)
    data = resp.get_json()
    assert not data['success']
    field_errors = data.get('details', {}).get('field_errors', {})
    print('DEBUG field_errors:', field_errors)
    assert any(err in msg for msgs in field_errors.values() for msg in (msgs if isinstance(msgs, list) else [msgs]))

def test_signup_duplicate_email(client, db, user_factory):
    user_factory(email='dupe@werent.com')
    payload = {
        'email': 'dupe@werent.com',
        'password': 'ValidPass123',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '0812345678',
    }
    resp = client.post('/api/auth/signup', json=payload)
    assert resp.status_code == 409
    data = resp.get_json()
    assert not data['success']
    assert 'already registered' in data['error']

# --- Login ---
def test_login_success(client, db, user_factory):
    user = user_factory(email='login@werent.com', password='LoginPass123')
    resp = client.post('/api/auth/login', json={'email': user.email, 'password': 'LoginPass123'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success']
    assert 'access_token' in data['data']
    assert 'refresh_token' in data['data']
    assert data['data']['user']['email'] == user.email

def test_login_invalid_password(client, db, user_factory):
    user = user_factory(email='fail@werent.com', password='RightPass123')
    resp = client.post('/api/auth/login', json={'email': user.email, 'password': 'WrongPass'})
    assert resp.status_code == 401
    data = resp.get_json()
    assert not data['success']
    assert 'Invalid email or password' in data['error']

def test_login_unregistered_email(client, db):
    resp = client.post('/api/auth/login', json={'email': 'nouser@werent.com', 'password': 'AnyPass123'})
    assert resp.status_code == 401
    data = resp.get_json()
    assert not data['success']
    assert 'Invalid email or password' in data['error']

def test_login_deactivated_user(client, db, user_factory):
    user = user_factory(email='deact@werent.com', is_active=False)
    resp = client.post('/api/auth/login', json={'email': user.email, 'password': 'TestPass123'})
    assert resp.status_code == 401
    data = resp.get_json()
    assert not data['success']
    assert 'deactivated' in data['error']

# --- Profile ---
def test_get_profile_authorized(client, db, user_factory, make_auth_headers):
    user = user_factory(email='profile@werent.com')
    headers = make_auth_headers(user)
    resp = client.get('/api/auth/profile', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success']
    assert data['data']['user']['email'] == user.email

def test_get_profile_unauthorized(client, db):
    resp = client.get('/api/auth/profile')
    assert resp.status_code == 401

def test_update_profile_success(client, db, user_factory, make_auth_headers, test_images):
    user = user_factory()
    headers = make_auth_headers(user)
    
    # Test updating regular fields
    update_data = {'first_name': 'Updated', 'phone_number': '0812999999'}
    resp = client.put('/api/auth/profile', json=update_data, headers=headers)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.get_json()}"
    data = resp.get_json()
    assert data['success']
    assert data['data']['user']['first_name'] == 'Updated'
    assert data['data']['user']['phone_number'] == '0812999999'
    
    # Test updating with a new profile image (raw base64)
    update_data = {'profile_image': test_images[0]}
    resp = client.put('/api/auth/profile', json=update_data, headers=headers)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.get_json()}"
    data = resp.get_json()
    assert data['success']
    assert data['data']['user']['profile_image'] == test_images[0]
    
    # Test updating with a new profile image (data URL)
    update_data = {'profile_image': test_images[1]}
    resp = client.put('/api/auth/profile', json=update_data, headers=headers)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.get_json()}"
    data = resp.get_json()
    assert data['success']
    assert data['data']['user']['profile_image'] == test_images[1]
    
    # Test that setting profile_image to None changes the existing image to None
    update_data = {'profile_image': None}
    resp = client.put('/api/auth/profile', json=update_data, headers=headers)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.get_json()}"
    data = resp.get_json()
    assert data['success']
    # Profile image should be None when set to None
    assert data['data']['user']['profile_image'] is None
    
    # Test deleting profile image by setting to empty string
    # First set an image
    client.put('/api/auth/profile', json={'profile_image': test_images[0]}, headers=headers)
    # Then delete it with empty string
    resp = client.put('/api/auth/profile', json={'profile_image': ''}, headers=headers)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.get_json()}"
    data = resp.get_json()
    assert data['success']
    # Empty string in the request should clear the image (set to None in response)
    # The controller converts empty string to None for profile_image
    assert data['data']['user']['profile_image'] is None
    
    # Test deleting profile image with empty request body
    # First set an image
    client.put('/api/auth/profile', json={'profile_image': test_images[0]}, headers=headers)
    # Then send empty body
    resp = client.put('/api/auth/profile', json={}, headers=headers)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.get_json()}"
    data = resp.get_json()
    assert data['success']
    # Profile image should be None with empty body
    assert data['data']['user']['profile_image'] is None

def test_update_profile_invalid(client, db, user_factory, make_auth_headers, test_images):
    user = user_factory()
    headers = make_auth_headers(user)
    
    # Test with invalid phone number
    resp = client.put('/api/auth/profile', json={'phone_number': '123'}, headers=headers)
    assert resp.status_code == 422  # Pydantic returns 422 for validation errors
    data = resp.get_json()
    assert not data['success']
    assert 'phone_number' in str(data['details'])
    
    # Test with invalid image format
    invalid_images = [
        'not_an_image',
        'data:image/jpeg;base64,invalid_base64',
        'data:text/plain;base64,SGVsbG8gV29ybGQ=',  # Not an image
        'data:image/unsupported;base64,SGVsbG8gV29ybGQ=',  # Unsupported format
    ]
    
    for img in invalid_images:
        resp = client.put('/api/auth/profile', json={'profile_image': img}, headers=headers)
        assert resp.status_code == 422, f"Expected 422 for invalid image: {img}"
        data = resp.get_json()
        assert not data['success']
        assert 'profile_image' in str(data['details']), f"Expected profile_image error in response: {data}"
    
    # Test with empty first name
    resp = client.put('/api/auth/profile', json={'first_name': ''}, headers=headers)
    assert resp.status_code == 422  # Pydantic returns 422 for validation errors
    data = resp.get_json()
    assert not data['success']
    assert 'first_name' in str(data['details'])

def test_update_profile_unauthorized(client, db):
    resp = client.put('/api/auth/profile', json={'first_name': 'ShouldFail'})
    assert resp.status_code == 401

# --- Refresh Token ---
def test_refresh_token_success(client, db, user_factory):
    user = user_factory(email='refresh@werent.com')
    # Login to get refresh token
    login_resp = client.post('/api/auth/login', json={'email': user.email, 'password': 'TestPass123'})
    tokens = login_resp.get_json()['data']
    headers = {'Authorization': f"Bearer {tokens['refresh_token']}"}
    resp = client.post('/api/auth/refresh', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success']
    assert 'access_token' in data['data']

def test_refresh_token_deactivated(client, db, user_factory):
    user = user_factory(email='refreshfail@werent.com', is_active=False)
    login_resp = client.post('/api/auth/login', json={'email': user.email, 'password': 'TestPass123'})
    login_data = login_resp.get_json()
    assert not login_data['success']
    assert 'deactivated' in login_data['error']

# --- Email Verification ---
def test_verify_email_success(client, db, user_factory):
    user = user_factory(email='verify@werent.com', is_verified=False)
    resp = client.get(f'/api/auth/verify-email/{user.uuid}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success']
    assert data['data']['verified'] is True

def test_verify_email_invalid(client, db):
    resp = client.get('/api/auth/verify-email/invalid-uuid')
    assert resp.status_code == 404
    data = resp.get_json()
    assert not data['success']
    assert 'verification link' in data['error']

def test_verify_email_already_verified(client, db, user_factory):
    user = user_factory(email='already@werent.com', is_verified=True)
    resp = client.get(f'/api/auth/verify-email/{user.uuid}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success']
    assert data['data']['verified'] is True

# --- Resend Verification ---
def test_resend_verification_success(client, db, user_factory, make_auth_headers):
    user = user_factory(email='resend@werent.com', is_verified=False)
    headers = make_auth_headers(user)
    with patch('app.services.email_service.EmailService.send_verification_email', return_value=True):
        resp = client.post('/api/auth/resend-verification', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success']
    assert data['data']['email_sent'] is True or 'Verification email sent' in data['message']

def test_resend_verification_already_verified(client, db, user_factory, make_auth_headers):
    user = user_factory(email='verified@werent.com', is_verified=True)
    headers = make_auth_headers(user)
    resp = client.post('/api/auth/resend-verification', headers=headers)
    assert resp.status_code == 400
    data = resp.get_json()
    assert not data['success']
    assert 'already verified' in data['error']

def test_resend_verification_unauthorized(client, db):
    resp = client.post('/api/auth/resend-verification')
    assert resp.status_code == 401
