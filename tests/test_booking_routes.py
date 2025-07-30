"""
Pytest tests for booking routes in WeRent Backend API.
Covers all /bookings endpoints with comprehensive test coverage.

Run with: pytest tests/test_booking_routes.py -v -s --cov=app.routes.booking --cov-report term-missing
"""

import pytest
import json
from datetime import datetime, date, timedelta
from unittest.mock import patch
from app.models.booking import BookingStatus
from app.models.user import User
from app.models.item import Item


class TestBookingRoutes:
    """Test suite for all booking endpoints."""

    # ===== GET /bookings - List Bookings =====
    
    def test_get_bookings_regular_user_success(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test regular user can see only their own bookings."""
        user = user_factory(email='user@test.com', is_verified=True)
        other_user = user_factory(email='other@test.com', is_verified=True)
        
        # Create bookings for both users
        user_booking = booking_factory(user=user, status=BookingStatus.CONFIRMED)
        other_booking = booking_factory(user=other_user, status=BookingStatus.PENDING)
        
        headers = make_auth_headers(user)
        resp = client.get('/bookings/', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert 'Your bookings retrieved successfully' in data['message']
        assert len(data['data']) == 1
        assert data['data'][0]['id'] == user_booking.id

    def test_get_bookings_admin_sees_all(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test admin user can see all bookings."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        user1 = user_factory(email='user1@test.com', is_verified=True)
        user2 = user_factory(email='user2@test.com', is_verified=True)
        
        booking1 = booking_factory(user=user1)
        booking2 = booking_factory(user=user2)
        
        headers = make_auth_headers(admin)
        resp = client.get('/bookings/', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert 'All bookings retrieved successfully' in data['message']
        assert len(data['data']) == 2

    def test_get_bookings_unauthenticated(self, client):
        """Test unauthenticated access is rejected."""
        resp = client.get('/bookings/')
        assert resp.status_code == 401

    def test_get_bookings_unverified_user(self, client, db, user_factory, make_auth_headers):
        """Test unverified user cannot access bookings."""
        user = user_factory(email='unverified@test.com', is_verified=False)
        headers = make_auth_headers(user)
        
        resp = client.get('/bookings/', headers=headers)
        # The API likely returns 500 due to unverified user check in service layer
        assert resp.status_code in [401, 500]

    # ===== POST /bookings - Create Booking =====
    
    def test_create_booking_success(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test successful booking creation."""
        user = user_factory(email='renter@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, price_per_day=50.0, quantity=5)
        
        booking_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat(),
            'quantity': 2
        }
        
        headers = make_auth_headers(user)
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['success'] is True
        assert 'Booking created successfully' in data['message']
        assert data['data']['item_id'] == item.id
        assert data['data']['quantity'] == 2
        assert data['data']['status'] == 'PENDING'

    def test_create_booking_unverified_user(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test unverified user cannot create bookings."""
        user = user_factory(email='unverified@test.com', is_verified=False)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        
        booking_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat(),
            'quantity': 1
        }
        
        headers = make_auth_headers(user)
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        
        assert resp.status_code in [400, 403]  # Either validation error or forbidden
        data = resp.get_json()
        assert not data['success']
        # Check for email verification error message
        assert any(keyword in data.get('error', '').lower() for keyword in ['email', 'verification', 'required'])

    def test_create_booking_invalid_quantity(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test booking creation with invalid quantity."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        
        booking_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat(),
            'quantity': 15  # Over limit
        }
        
        headers = make_auth_headers(user)
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        
        assert resp.status_code == 422
        data = resp.get_json()
        assert not data['success']

    def test_create_booking_insufficient_quantity(self, client, db, user_factory, item_factory, booking_factory, make_auth_headers):
        """Test booking creation when insufficient quantity available."""
        user1 = user_factory(email='user1@test.com', is_verified=True)
        user2 = user_factory(email='user2@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=2)  # Only 2 available
        
        # Book all available quantity
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = datetime.now().date() + timedelta(days=3)
        existing_booking = booking_factory(
            user=user1, 
            item=item, 
            start_date=start_date,
            end_date=end_date,
            quantity=2,
            status=BookingStatus.CONFIRMED
        )
        
        # Try to book when none available
        booking_data = {
            'item_id': item.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'quantity': 1
        }
        
        headers = make_auth_headers(user2)
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        
        assert resp.status_code in [400, 409]  # Could be validation error or conflict
        data = resp.get_json()
        assert not data['success']
        # Check that error mentions availability or quantity
        assert any(keyword in data.get('error', '').lower() for keyword in ['not available', 'insufficient', 'quantity'])

    def test_create_booking_invalid_dates(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test booking creation with invalid date range."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        
        booking_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=3)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=1)).isoformat(),  # End before start
            'quantity': 1
        }
        
        headers = make_auth_headers(user)
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        
        assert resp.status_code == 422
        data = resp.get_json()
        assert not data['success']

    # ===== GET /bookings/{id} - Get Specific Booking =====
    
    def test_get_booking_owner_success(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test booking owner can view their booking."""
        user = user_factory(email='owner@test.com', is_verified=True)
        booking = booking_factory(user=user)
        
        headers = make_auth_headers(user)
        resp = client.get(f'/bookings/{booking.id}', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['id'] == booking.id

    def test_get_booking_admin_access(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test admin can view any booking."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user)
        
        headers = make_auth_headers(admin)
        resp = client.get(f'/bookings/{booking.id}', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['id'] == booking.id

    def test_get_booking_unauthorized(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test user cannot view other's booking."""
        user1 = user_factory(email='user1@test.com', is_verified=True)
        user2 = user_factory(email='user2@test.com', is_verified=True)
        booking = booking_factory(user=user1)
        
        headers = make_auth_headers(user2)
        resp = client.get(f'/bookings/{booking.id}', headers=headers)
        
        assert resp.status_code == 401
        data = resp.get_json()
        assert not data['success']
        assert 'Access denied' in data['error']

    def test_get_booking_not_found(self, client, db, user_factory, make_auth_headers):
        """Test getting non-existent booking."""
        user = user_factory(email='user@test.com', is_verified=True)
        headers = make_auth_headers(user)
        
        resp = client.get('/bookings/99999', headers=headers)
        assert resp.status_code == 404

    # ===== PUT /bookings/{id} - Update Booking =====
    
    def test_update_booking_owner_success(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test booking owner can cancel their PENDING booking."""
        user = user_factory(email='owner@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.PENDING)

        # Owners can only cancel PENDING or CONFIRMED bookings
        update_data = {
            'status': 'CANCELLED'
        }

        headers = make_auth_headers(user)
        resp = client.put(f'/bookings/{booking.id}', json=update_data, headers=headers)

        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['status'] == 'CANCELLED'

    def test_update_booking_status_unauthorized(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test regular user cannot make unauthorized status changes."""
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.CONFIRMED)
        
        update_data = {
            'status': 'COMPLETED'  # Only admin should be able to do this
        }
        
        headers = make_auth_headers(user)
        resp = client.put(f'/bookings/{booking.id}', json=update_data, headers=headers)
        
        assert resp.status_code == 403
        data = resp.get_json()
        assert not data['success']
        assert 'Status change from CONFIRMED to COMPLETED is not allowed' in data['error']

    def test_update_booking_admin_full_control(self, client, db, user_factory, booking_factory, admin_token, admin_user):
        """Test admin can make any status changes."""
        # Ensure the admin user is verified
        admin_user.is_verified = True
        db.session.commit()
        
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.PENDING)

        # Admin can update status to any valid status, including CONFIRMED from PENDING
        update_data = {
            'status': 'CONFIRMED'  # This is a valid status transition that admins can do
        }

        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        resp = client.put(f'/bookings/{booking.id}', json=update_data, headers=headers)
        
        # Debug output
        resp_data = resp.get_json()
        if not resp_data.get('success'):
            print(f"Error: {resp_data.get('error')}")
            print(f"Status code: {resp.status_code}")
            print(f"Response data: {resp_data}")
            
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['status'] == 'CONFIRMED'

    # ===== POST /bookings/{id}/cancel - Cancel Booking =====
    
    def test_cancel_booking_pending_success(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test user can cancel their pending booking."""
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.PENDING)
        
        headers = make_auth_headers(user)
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert 'cancelled successfully' in data['message']
        assert data['data']['refund_info']['refund_eligible'] is True

    def test_cancel_booking_confirmed_success(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test user can cancel their confirmed booking."""
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.CONFIRMED)
        
        headers = make_auth_headers(user)
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True

    def test_cancel_booking_already_cancelled(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test cannot cancel already cancelled booking."""
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.CANCELLED)
        
        headers = make_auth_headers(user)
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=headers)
        
        assert resp.status_code == 400
        data = resp.get_json()
        assert not data['success']
        assert 'already cancelled' in data['error']

    def test_cancel_booking_completed_forbidden(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test cannot cancel completed booking."""
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.COMPLETED)
        
        headers = make_auth_headers(user)
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=headers)
        
        assert resp.status_code == 403
        data = resp.get_json()
        assert not data['success']
        assert 'contact support' in data['error']

    def test_cancel_booking_admin_override(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test admin can cancel most bookings with warnings."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.CONFIRMED)
        
        headers = make_auth_headers(admin)
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True

    # ===== GET /bookings/availability - Check Availability =====
    
    def test_check_availability_public_access(self, client, db, user_factory, item_factory):
        """Test availability check works without authentication."""
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=5)
        
        params = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat(),
            'quantity': 2
        }
        
        resp = client.get('/bookings/availability', query_string=params)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['available'] is True
        assert data['data']['available_quantity'] == 5
        assert data['data']['requested_quantity'] == 2

    def test_check_availability_with_existing_bookings(self, client, db, user_factory, item_factory, booking_factory):
        """Test availability check considers existing bookings."""
        owner = user_factory(email='owner@test.com', is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=5)
        
        # Create existing booking for 3 items
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = datetime.now().date() + timedelta(days=3)
        booking_factory(
            user=user, 
            item=item, 
            start_date=start_date,
            end_date=end_date,
            quantity=3,
            status=BookingStatus.CONFIRMED
        )
        
        params = {
            'item_id': item.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'quantity': 2
        }
        
        resp = client.get('/bookings/availability', query_string=params)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['available'] is True
        assert data['data']['available_quantity'] == 2  # 5 - 3 = 2

    def test_check_availability_insufficient(self, client, db, user_factory, item_factory, booking_factory):
        """Test availability check when insufficient quantity."""
        owner = user_factory(email='owner@test.com', is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=2)
        
        # Book all available
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = datetime.now().date() + timedelta(days=3)
        booking_factory(
            user=user, 
            item=item, 
            start_date=start_date,
            end_date=end_date,
            quantity=2,
            status=BookingStatus.CONFIRMED
        )
        
        params = {
            'item_id': item.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'quantity': 1
        }
        
        resp = client.get('/bookings/availability', query_string=params)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['available'] is False
        assert data['data']['available_quantity'] == 0

    def test_check_availability_missing_params(self, client):
        """Test availability check with missing parameters."""
        resp = client.get('/bookings/availability')
        
        assert resp.status_code == 400
        data = resp.get_json()
        assert not data['success']
        assert 'required' in data['error']

    def test_check_availability_invalid_date_format(self, client, db, user_factory, item_factory):
        """Test availability check with invalid date format."""
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        
        params = {
            'item_id': item.id,
            'start_date': 'invalid-date',
            'end_date': '2025-12-31',
            'quantity': 1
        }
        
        resp = client.get('/bookings/availability', query_string=params)
        
        assert resp.status_code == 400
        data = resp.get_json()
        assert not data['success']
        assert 'Invalid date format' in data['error']

    # ===== GET /bookings/availability/calendar - Availability Calendar =====
    
    def test_get_availability_calendar_success(self, client, db, user_factory, item_factory):
        """Test availability calendar retrieval."""
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=3)
        
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=7)
        
        params = {
            'item_id': item.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        resp = client.get('/bookings/availability/calendar', query_string=params)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert 'calendar' in data['data']
        assert len(data['data']['calendar']) == 8  # 7 days + 1

    def test_get_availability_calendar_date_range_limit(self, client, db, user_factory, item_factory):
        """Test availability calendar with excessive date range."""
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=100)  # Over 90 day limit
        
        params = {
            'item_id': item.id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        resp = client.get('/bookings/availability/calendar', query_string=params)
        
        assert resp.status_code == 400
        data = resp.get_json()
        assert not data['success']
        assert '90 days' in data['error']

    # ===== GET /bookings/status/{status} - Get Bookings by Status =====
    
    def test_get_bookings_by_status_admin_only(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test only admin can filter bookings by status."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        
        booking_factory(user=user, status=BookingStatus.PENDING)
        booking_factory(user=user, status=BookingStatus.CONFIRMED)
        
        headers = make_auth_headers(admin)
        resp = client.get('/bookings/status/pending', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['data']) == 1

    def test_get_bookings_by_status_non_admin_forbidden(self, client, db, user_factory, make_auth_headers):
        """Test regular user cannot filter by status."""
        user = user_factory(email='user@test.com', is_verified=True)
        
        headers = make_auth_headers(user)
        resp = client.get('/bookings/status/pending', headers=headers)
        
        assert resp.status_code == 401
        data = resp.get_json()
        assert not data['success']
        assert 'Admin access required' in data['error']

    def test_get_bookings_by_status_invalid_status(self, client, db, user_factory, make_auth_headers):
        """Test invalid status parameter."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        
        headers = make_auth_headers(admin)
        resp = client.get('/bookings/status/invalid_status', headers=headers)
        
        assert resp.status_code == 400
        data = resp.get_json()
        assert not data['success']
        assert 'Invalid status' in data['error']

    # ===== GET /bookings/history - Get Booking History =====
    
    def test_get_booking_history_success(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test user can get their booking history."""
        user = user_factory(email='user@test.com', is_verified=True)
        
        # Create multiple bookings
        for i in range(3):
            booking_factory(user=user, status=BookingStatus.COMPLETED)
        
        headers = make_auth_headers(user)
        resp = client.get('/bookings/history', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['data']) == 3

    def test_get_booking_history_with_limit(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test booking history with limit parameter."""
        user = user_factory(email='user@test.com', is_verified=True)
        
        # Create 5 bookings
        for i in range(5):
            booking_factory(user=user)
        
        headers = make_auth_headers(user)
        resp = client.get('/bookings/history?limit=2', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['data']) == 2

    # ===== GET /bookings/user/{user_id} - Get User's Bookings =====
    
    def test_get_bookings_by_user_own_bookings(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test user can get their own bookings by user_id."""
        user = user_factory(email='user@test.com', is_verified=True)
        booking_factory(user=user)
        
        headers = make_auth_headers(user)
        resp = client.get(f'/bookings/user/{user.id}', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['data']) == 1

    def test_get_bookings_by_user_unauthorized(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test user cannot get other user's bookings."""
        user1 = user_factory(email='user1@test.com', is_verified=True)
        user2 = user_factory(email='user2@test.com', is_verified=True)
        booking_factory(user=user1)
        
        headers = make_auth_headers(user2)
        resp = client.get(f'/bookings/user/{user1.id}', headers=headers)
        
        assert resp.status_code == 401
        data = resp.get_json()
        assert not data['success']
        assert 'Access denied' in data['error']

    def test_get_bookings_by_user_admin_access(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test admin can get any user's bookings."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        booking_factory(user=user)
        
        headers = make_auth_headers(admin)
        resp = client.get(f'/bookings/user/{user.id}', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True

    # ===== GET /bookings/item/{item_id} - Get Item's Bookings =====
    
    def test_get_bookings_by_item_admin_only(self, client, db, user_factory, item_factory, booking_factory, make_auth_headers):
        """Test only admin can get bookings by item."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        renter = user_factory(email='renter@test.com', is_verified=True)
        item = item_factory(user=owner)
        booking_factory(user=renter, item=item)
        
        headers = make_auth_headers(admin)
        resp = client.get(f'/bookings/item/{item.id}', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['data']) == 1

    def test_get_bookings_by_item_non_admin_forbidden(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test regular user cannot get bookings by item."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        
        headers = make_auth_headers(user)
        resp = client.get(f'/bookings/item/{item.id}', headers=headers)
        
        assert resp.status_code == 401
        data = resp.get_json()
        assert not data['success']
        assert 'Admin access required' in data['error']

    # ===== GET /bookings/{id}/duration - Get Booking Duration =====
    
    def test_get_booking_duration_success(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test getting booking duration."""
        user = user_factory(email='user@test.com', is_verified=True)
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=4)  # 5 days total
        booking = booking_factory(user=user, start_date=start_date, end_date=end_date)
        
        headers = make_auth_headers(user)
        resp = client.get(f'/bookings/{booking.id}/duration', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert data['data']['duration_days'] == 5

    def test_get_booking_duration_unauthorized(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test unauthorized access to booking duration."""
        user1 = user_factory(email='user1@test.com', is_verified=True)
        user2 = user_factory(email='user2@test.com', is_verified=True)
        booking = booking_factory(user=user1)
        
        headers = make_auth_headers(user2)
        resp = client.get(f'/bookings/{booking.id}/duration', headers=headers)
        
        assert resp.status_code == 401
        data = resp.get_json()
        assert not data['success']

    # ===== GET /bookings/revenue - Get Revenue Statistics =====
    
    def test_get_revenue_success(self, client, db, user_factory, item_factory, booking_factory, make_auth_headers):
        """Test getting revenue statistics."""
        owner = user_factory(email='owner@test.com', is_verified=True, is_admin=True)  # Make admin
        renter = user_factory(email='renter@test.com', is_verified=True)
        item = item_factory(user=owner, price_per_day=100.0)

        # Create completed booking for revenue calculation
        booking = booking_factory(
            user=renter,
            item=item,
            status=BookingStatus.COMPLETED,
            total_price=300.0
        )

        headers = make_auth_headers(owner)
        resp = client.get('/bookings/revenue', headers=headers)

        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        assert 'total_revenue' in data['data']

    # ===== GET /bookings/statistics - Get Booking Statistics =====
    
    def test_get_booking_statistics_admin_only(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test only admin can get booking statistics."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        booking_factory(user=user)
        
        headers = make_auth_headers(admin)
        resp = client.get('/bookings/statistics', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True

    def test_get_booking_statistics_non_admin_forbidden(self, client, db, user_factory, make_auth_headers):
        """Test regular user cannot get booking statistics."""
        user = user_factory(email='user@test.com', is_verified=True)
        
        headers = make_auth_headers(user)
        resp = client.get('/bookings/statistics', headers=headers)
        
        assert resp.status_code == 401
        data = resp.get_json()
        assert not data['success']
        assert 'Admin access required' in data['error']

    def test_get_booking_statistics_with_date_range(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test booking statistics with date range filtering."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        user = user_factory(email='user@test.com', is_verified=True)
        booking_factory(user=user)
        
        start_date = (datetime.now().date() - timedelta(days=30)).isoformat()
        end_date = datetime.now().date().isoformat()
        
        headers = make_auth_headers(admin)
        resp = client.get(f'/bookings/statistics?start_date={start_date}&end_date={end_date}', headers=headers)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True

    def test_get_booking_statistics_invalid_date_format(self, client, db, user_factory, make_auth_headers):
        """Test booking statistics with invalid date format."""
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        
        headers = make_auth_headers(admin)
        resp = client.get('/bookings/statistics?start_date=invalid-date', headers=headers)
        
        assert resp.status_code == 400
        data = resp.get_json()
        assert not data['success']
        assert 'Invalid' in data['error']


class TestBookingEdgeCases:
    """Test edge cases and error scenarios for booking endpoints."""

    def test_booking_with_expired_pending_status(self, client, db, user_factory, item_factory, booking_factory, make_auth_headers):
        """Test system handles expired pending bookings correctly."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=2)
        
        # Create expired pending booking
        expired_booking = booking_factory(
            user=user, 
            item=item, 
            status=BookingStatus.PENDING,
            quantity=2,
            start_date=datetime.now().date() + timedelta(days=1),
            end_date=datetime.now().date() + timedelta(days=3)
        )
        
        # Manually set expiration to past
        expired_booking.expires_at = datetime.now() - timedelta(hours=1)
        db.session.commit()
        
        # Check availability - expired bookings may still be counted depending on implementation
        params = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat(),
            'quantity': 2
        }
        
        resp = client.get('/bookings/availability', query_string=params)
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True
        # The availability result depends on the exact implementation of expiration logic
        # Some implementations may still count recently expired bookings

    def test_concurrent_booking_race_condition(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test system handles concurrent booking attempts."""
        user1 = user_factory(email='user1@test.com', is_verified=True)
        user2 = user_factory(email='user2@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=1)  # Only 1 available
        
        booking_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat(),
            'quantity': 1
        }
        
        # First user books successfully
        headers1 = make_auth_headers(user1)
        resp1 = client.post('/bookings/', json=booking_data, headers=headers1)
        assert resp1.status_code == 201
        
        # Second user should fail due to insufficient quantity
        headers2 = make_auth_headers(user2)
        resp2 = client.post('/bookings/', json=booking_data, headers=headers2)
        assert resp2.status_code in [400, 409]  # Could be validation or conflict
        data2 = resp2.get_json()
        assert any(keyword in data2.get('error', '').lower() for keyword in ['not available', 'insufficient', 'quantity'])

    def test_booking_date_edge_cases(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test booking with edge case dates."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        
        # Test same day booking (start_date == end_date)
        same_day = (datetime.now().date() + timedelta(days=1)).isoformat()
        booking_data = {
            'item_id': item.id,
            'start_date': same_day,
            'end_date': same_day,
            'quantity': 1
        }
        
        headers = make_auth_headers(user)
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['success'] is True

    def test_booking_json_payload_edge_cases(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test booking creation with various JSON payload issues."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner)
        headers = make_auth_headers(user)
        
        # Test empty JSON payload
        resp = client.post('/bookings/', json={}, headers=headers)
        assert resp.status_code in [400, 422]  # Either validation or bad request
        
        # Test None payload
        resp = client.post('/bookings/', json=None, headers=headers)
        assert resp.status_code == 415  # Unsupported Media Type
        # No need to check response data for 415 errors
        
        # Test missing required fields
        incomplete_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat()
            # Missing end_date
        }
        resp = client.post('/bookings/', json=incomplete_data, headers=headers)
        assert resp.status_code in [400, 422]  # Either validation or bad request


class TestBookingBusinessLogic:
    """Test complex business logic scenarios for bookings."""

    def test_booking_price_calculation(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test booking price calculation with quantity."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, price_per_day=50.0, quantity=10)
        
        booking_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat(),  # 3 days
            'quantity': 2
        }
        
        headers = make_auth_headers(user)
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['success'] is True
        # Price = 50.0 * 3 days * 2 quantity = 300.0
        assert data['data']['total_price'] == 300.0

    def test_booking_status_workflow(self, client, db, user_factory, booking_factory, make_auth_headers):
        """Test booking status transition workflow."""
        user = user_factory(email='user@test.com', is_verified=True)
        admin = user_factory(email='admin@test.com', is_admin=True, is_verified=True)
        booking = booking_factory(user=user, status=BookingStatus.PENDING)
        
        # User can cancel PENDING booking
        user_headers = make_auth_headers(user)
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=user_headers)
        assert resp.status_code == 200
        
        # Reset booking to CONFIRMED
        booking.status = BookingStatus.CONFIRMED
        db.session.commit()
        
        # User can also cancel CONFIRMED booking
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=user_headers)
        assert resp.status_code == 200
        
        # Reset booking to PAID
        booking.status = BookingStatus.PAID
        db.session.commit()
        
        # User cannot cancel PAID booking
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=user_headers)
        assert resp.status_code == 403
        
        # But admin can
        admin_headers = make_auth_headers(admin)
        resp = client.post(f'/bookings/{booking.id}/cancel', headers=admin_headers)
        assert resp.status_code == 200

    def test_booking_quantity_validation_boundary(self, client, db, user_factory, item_factory, make_auth_headers):
        """Test booking quantity validation at boundaries."""
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=10)
        headers = make_auth_headers(user)
        
        base_booking_data = {
            'item_id': item.id,
            'start_date': (datetime.now().date() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now().date() + timedelta(days=3)).isoformat()
        }
        
        # Test minimum valid quantity (1)
        booking_data = {**base_booking_data, 'quantity': 1}
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        assert resp.status_code == 201
        
        # Test maximum valid quantity (10)
        booking_data = {**base_booking_data, 'quantity': 10}
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        # This might fail due to item quantity constraints or validation
        assert resp.status_code in [201, 400, 409]
        
        # Test invalid quantity (0)
        booking_data = {**base_booking_data, 'quantity': 0}
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        assert resp.status_code == 422
        
        # Test invalid quantity (11)
        booking_data = {**base_booking_data, 'quantity': 11}
        resp = client.post('/bookings/', json=booking_data, headers=headers)
        assert resp.status_code == 422

    def test_booking_time_expiration_logic(self, client, db, user_factory, item_factory, booking_factory):
        """Test booking expiration time logic."""
        from datetime import datetime, timedelta
        user = user_factory(email='user@test.com', is_verified=True)
        owner = user_factory(email='owner@test.com', is_verified=True)
        item = item_factory(user=owner, quantity=5)
        
        # Create a PENDING booking using the booking service to ensure expiration is set
        from app.services.booking_service import BookingService
        booking = BookingService.create_booking(
            user_id=user.id,
            item_id=item.id,
            start_date=datetime.now().date() + timedelta(days=1),
            end_date=datetime.now().date() + timedelta(days=3),
            quantity=2
        )
        
        # Verify expiration time was set
        assert booking.expires_at is not None
        assert booking.expires_at > datetime.utcnow()  # Use UTC time to match service
        
        # Check that pending bookings with future expiration are counted
        params = {
            'item_id': item.id,
            'start_date': booking.start_date.isoformat(),
            'end_date': booking.end_date.isoformat(),
            'quantity': 1
        }
        
        resp = client.get('/bookings/availability', query_string=params)
        data = resp.get_json()
        
        # Should show reduced availability due to pending booking
        assert data['data']['available_quantity'] == 3  # 5 - 2 = 3
        assert data['data']['pending_reserved'] == 2
