import pytest
from app.services.user_service import UserService
from app.models.user import User
from app.extensions import db as db_ext

# pytest tests/test_user_service.py -v -s --cov=. --cov-report term-missing

@pytest.fixture
def service():
    return UserService()

@pytest.fixture
def user(db):
    u = User(
        email='service@werent.com',
        first_name='Service',
        last_name='User',
        phone_number='0812345678',
        is_admin=False,
        is_verified=False,
        is_active=True
    )
    u.set_password('ServicePass123')
    db_ext.session.add(u)
    db_ext.session.commit()
    return u

def test_create_user(service, db):
    user = service.create_user('svc@werent.com', 'SvcPass123', 'Svc', 'User', '0812345678')
    assert user.id is not None
    assert user.email == 'svc@werent.com'
    assert user.check_password('SvcPass123')

def test_authenticate_user(service, user):
    assert service.authenticate_user(user.email, 'ServicePass123')
    assert service.authenticate_user(user.email, 'WrongPass') is None

def test_find_by_email_and_uuid(service, user):
    assert service.find_by_email(user.email).id == user.id
    assert service.find_by_uuid(user.uuid).id == user.id

def test_update_profile(service, user):
    updated = service.update_profile(user.id, first_name='Updated', phone_number='0812999999')
    assert updated.first_name == 'Updated'
    assert updated.phone_number == '0812999999'

def test_check_email_exists(service, user):
    assert service.check_email_exists(user.email)
    assert not service.check_email_exists('nope@werent.com')
