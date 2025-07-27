"""
Authentication route tests for WeRent Backend API.
"""

import json
from app.models import User


class TestAuth:
    """Test cases for authentication endpoints."""
    
    def test_signup_success(self, client):
        """Test successful user registration."""
        data = {
            'email': 'test@werent.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890'
        }
        
        response = client.post('/api/auth/signup', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['success'] is True
        assert 'access_token' in json_data['data']
        assert json_data['data']['user']['email'] == 'test@werent.com'
    
    def test_signup_missing_fields(self, client):
        """Test signup with missing required fields."""
        data = {
            'email': 'test@werent.com'
            # Missing password, first_name, last_name
        }
        
        response = client.post('/api/auth/signup',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 422
        json_data = response.get_json()
        assert json_data['success'] is False
        assert 'field_errors' in json_data['details']
    
    def test_signup_invalid_email(self, client):
        """Test signup with invalid email format."""
        data = {
            'email': 'invalid-email',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        response = client.post('/api/auth/signup',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 422
        json_data = response.get_json()
        assert 'email' in json_data['details']['field_errors']
    
    def test_login_success(self, client):
        """Test successful user login."""
        # First create a user
        user = User(
            email='test@werent.com',
            first_name='John',
            last_name='Doe'
        )
        user.set_password('TestPass123')
        user.save()
        
        # Try to login
        data = {
            'email': 'test@werent.com',
            'password': 'TestPass123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert 'access_token' in json_data['data']
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        data = {
            'email': 'nonexistent@werent.com',
            'password': 'WrongPass123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 401
        json_data = response.get_json()
        assert json_data['success'] is False
