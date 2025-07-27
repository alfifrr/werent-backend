import pytest
from pydantic import ValidationError
from app.schemas.auth_schema import RegisterSchema, LoginSchema

# pytest tests/test_auth_schema.py -v -s --cov=. --cov-report term-missing

def test_register_schema_valid():
    s = RegisterSchema(
        email='schema@werent.com',
        password='ValidPass123',
        first_name='Schema',
        last_name='Test',
        phone_number='0812345678'
    )
    assert s.email == 'schema@werent.com'
    assert s.first_name == 'Schema'

def test_register_schema_invalid_password():
    with pytest.raises(ValidationError) as e:
        RegisterSchema(
            email='schema@werent.com',
            password='short',
            first_name='Schema',
            last_name='Test',
            phone_number='0812345678'
        )
    assert 'at least 8 characters' in str(e.value)

def test_register_schema_invalid_phone():
    with pytest.raises(ValidationError) as e:
        RegisterSchema(
            email='schema@werent.com',
            password='ValidPass123',
            first_name='Schema',
            last_name='Test',
            phone_number='123'
        )
    assert 'between 10-15 digits' in str(e.value)

def test_login_schema_valid():
    s = LoginSchema(email='login@werent.com', password='ValidPass123')
    assert s.email == 'login@werent.com'
    assert s.password == 'ValidPass123'

def test_login_schema_invalid_email():
    with pytest.raises(ValidationError):
        LoginSchema(email='not-an-email', password='ValidPass123')
