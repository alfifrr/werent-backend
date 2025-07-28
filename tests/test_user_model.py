import pytest
from app.models.user import User
from app.extensions import db as db_ext

# pytest tests/test_user_model.py -v -s --cov=. --cov-report term-missing

@pytest.fixture
def user(db):
    u = User(
        email='model@werent.com',
        first_name='Model',
        last_name='User',
        phone_number='0812345678',
        is_admin=False,
        is_verified=False,
        is_active=True
    )
    u.set_password('ModelPass123')
    db_ext.session.add(u)
    db_ext.session.commit()
    return u

def test_password_hash_and_check(user):
    assert user.check_password('ModelPass123')
    assert not user.check_password('WrongPass')

def test_full_name(user):
    assert user.full_name == 'Model User'

def test_to_dict_no_sensitive(user):
    d = user.to_dict()
    assert d['email'] == user.email
    assert 'password_hash' not in d

def test_to_dict_with_sensitive(user):
    d = user.to_dict(include_sensitive=True)
    assert 'password_hash' in d

def test_save_and_delete(user, db):
    uid = user.id
    user.delete()
    assert User.find_by_id(uid) is None

def test_find_by_email_and_uuid(user):
    by_email = User.find_by_email(user.email)
    by_uuid = User.find_by_uuid(user.uuid)
    assert by_email.id == user.id
    assert by_uuid.id == user.id
