"""
Test configuration for WeRent Backend API.
Provides fixtures and setup for testing the Flask application.
"""

import pytest
from app import create_app
from app.extensions import db as db_ext
from app.models import User, Item
from app.models.item import ItemType, Size, Gender
import json
import random
import string
from app.models.ticketing import Ticketing
from app.models.booking import Booking, BookingStatus
from datetime import datetime, timedelta, UTC


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app(config_name='testing')
    
    with app.app_context():
        db_ext.create_all()
        yield app
        db_ext.drop_all()

@pytest.fixture
def db(app):
    """Yield the db object in the app context for tests that need direct db access."""
    with app.app_context():
        yield db_ext


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test runner for the app's CLI commands."""
    return app.test_cli_runner()

@pytest.fixture
def review_payload():
    # 1x1 transparent PNG base64 string
    img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/w8AAgMBApT+ZQAAAABJRU5ErkJggg=="
    return {
        "rating": 5,
        "review_message": "Great product!",
        "images": [img_base64, img_base64]
    }

@pytest.fixture
def user_factory(db):
    def _factory(**kwargs):
        # Generate a unique email for each user
        rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = kwargs.get('email', f'user_{rand_str}@werent.com')
        user = User(
            email=email,
            first_name=kwargs.get('first_name', 'Test'),
            last_name=kwargs.get('last_name', 'User'),
            phone_number=kwargs.get('phone_number', '0812345678'),
            is_admin=kwargs.get('is_admin', False),
            is_verified=kwargs.get('is_verified', True),
            is_active=kwargs.get('is_active', True)
        )
        password = kwargs.get('password', 'TestPass123')
        user.set_password(password)
        db.session.add(user)
        db_ext.session.commit()
        return user
    return _factory

@pytest.fixture
def item_factory(db):
    def _factory(user=None, **kwargs):
        if user is None:
            # Create a user if not provided
            user = User(
                email=f'item_owner_{"".join(random.choices(string.ascii_lowercase + string.digits, k=8))}@werent.com',
                first_name='Owner',
                last_name='User',
                phone_number='0812345678',
                is_admin=False,
                is_verified=True,
                is_active=True
            )
            user.set_password('OwnerPass123')
            db.session.add(user)
            db_ext.session.commit()
        # Generate unique product code
        product_code = kwargs.get('product_code', 'PCODE' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
        item = Item(
            name=kwargs.get('name', 'Test Item'),
            type=kwargs.get('type', ItemType.DRESS),
            size=kwargs.get('size', Size.M),
            gender=kwargs.get('gender', Gender.UNISEX),
            brand=kwargs.get('brand', 'TestBrand'),
            color=kwargs.get('color', 'Red'),
            quantity=kwargs.get('quantity', 1),
            product_code=product_code,
            description=kwargs.get('description', 'A test item.'),
            price_per_day=kwargs.get('price_per_day', 100.0),
            user_id=user.id
        )
        db.session.add(item)
        db_ext.session.commit()
        return item
    return _factory

@pytest.fixture
def item_with_owner(db, item_factory, user_factory):
    owner = user_factory()
    item = item_factory(user=owner)
    db_ext.session.commit()
    return item, owner

@pytest.fixture
def another_user(db, user_factory):
    user = user_factory()
    db_ext.session.commit()
    return user

@pytest.fixture
def booking_factory(db, item_factory, user_factory):
    def _factory(user=None, item=None, **kwargs):
        if user is None:
            user = user_factory()
        if item is None:
            item = item_factory(user=user)
        start_date = kwargs.get('start_date', datetime.now(UTC).date())
        end_date = kwargs.get('end_date', start_date + timedelta(days=2))
        booking = Booking(
            user_id=user.id,
            item_id=item.id,
            start_date=start_date,
            end_date=end_date,
            total_price=item.price_per_day * 3,
            status=kwargs.get('status', BookingStatus.CONFIRMED),
            is_paid=kwargs.get('is_paid', True)
        )
        db.session.add(booking)
        db_ext.session.commit()
        return booking
    return _factory

@pytest.fixture
def ticket_factory(db, user_factory, booking_factory):
    def _factory(user=None, booking=None, chat_content='Initial message', is_resolved=False, **kwargs):
        if user is None:
            user = user_factory()
        if booking is None:
            booking = booking_factory(user=user)
        ticket = Ticketing(
            user_id=user.id,
            booking_id=booking.id,
            chat_content=chat_content,
            is_resolved=is_resolved,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        db.session.add(ticket)
        db_ext.session.commit()
        return ticket
    return _factory

@pytest.fixture
def resolved_ticket(ticket_factory):
    return ticket_factory(is_resolved=True)

@pytest.fixture
def open_ticket(ticket_factory):
    return ticket_factory(is_resolved=False)


@pytest.fixture
def admin_user(app):
    """Create an admin user for testing."""
    with app.app_context():
        user = User(
            email='admin@werent.com',
            first_name='Admin',
            last_name='User',
            phone_number='08123456789',
            is_admin=True
        )
        user.set_password('AdminPass123')
        user.save()
        yield user
        # Clean up: rollback if needed before further DB ops
        from app import db
        try:
            db.session.rollback()
        except Exception:
            pass
        from app.models import Item
        Item.query.filter_by(user_id=user.id).delete()
        db_ext.session.commit()
        user.delete()

@pytest.fixture
def admin_token(client, admin_user):
    """Get JWT token for admin user."""
    response = client.post('/api/auth/login', data=json.dumps({
        'email': 'admin@werent.com',
        'password': 'AdminPass123'
    }), content_type='application/json')
    assert response.status_code == 200
    return response.get_json()['data']['access_token']

@pytest.fixture
def user_token(client):
    """Get JWT token for a regular user."""
    # Register user
    client.post('/api/auth/signup', data=json.dumps({
        'email': 'user@werent.com',
        'password': 'UserPass123',
        'first_name': 'Regular',
        'last_name': 'User',
        'phone': '0811111111'
    }), content_type='application/json')
    # Login user
    response = client.post('/api/auth/login', data=json.dumps({
        'email': 'user@werent.com',
        'password': 'UserPass123'
    }), content_type='application/json')
    assert response.status_code == 200
    return response.get_json()['data']['access_token']

@pytest.fixture
def auth_headers(user_token):
    """Fixture that returns Authorization headers for a regular user."""
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture
def make_auth_headers(db, client):
    """Return a function that generates auth headers for any user by logging them in."""
    def _make(user):
        resp = client.post('/api/auth/login', json={
            'email': user.email,
            'password': 'TestPass123',  # Assumes user_factory uses this password
        })
        assert resp.status_code == 200
        token = resp.get_json()['data']['access_token']
        return {"Authorization": f"Bearer {token}"}
    return _make
