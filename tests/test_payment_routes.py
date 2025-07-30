from app.models.user import User

# All tests here use client, db, user_factory, booking_factory, payment_factory, admin_token, user_token, auth_headers

# pytest tests/test_payment_routes.py -v -s --cov=. --cov-report term-missing

class TestPaymentRoutes:
    def test_create_payment_success(self, client, db, user_factory, booking_factory, auth_headers):
        from app.models.booking import Booking
        
        # Setup test user
        user = User.query.filter_by(email="user@werent.com").first()
        assert user is not None, "Test user not found in DB."
        
        # Ensure user is verified
        if not user.is_verified:
            user.is_verified = True
            user.save() if hasattr(user, 'save') else db.session.commit()
            
        # Create a booking with initial status
        booking = booking_factory(user=user, status="PENDING", is_paid=False)
        db.session.commit()
        
        # Prepare payment payload
        payload = {
            "booking_id": [booking.id],
            "total_price": 123.45,
            "payment_method": "CC",
            "payment_type": "RENT"
        }
        
        # Make payment request
        response = client.post("/payments/", json=payload, headers=auth_headers)
        
        # Debug if needed
        if response.status_code != 201:
            print(response.get_json(), "DEBUG"*10)
            
        # Verify response
        assert response.status_code == 201
        data = response.get_json()["data"]
        assert data["total_price"] == 123.45
        assert data["payment_method"] == "CC"
        
        # Verify booking status was updated
        db.session.refresh(booking)
        assert booking.status.value == "PAID"  # Compare with enum value
        assert booking.is_paid is True

    def test_create_payment_fail_unverified_user(self, client, db, user_factory, booking_factory, make_auth_headers):
        user = user_factory(is_verified=False)
        db.session.commit()
        booking = booking_factory(user=user)
        payload = {
            "booking_id": [booking.id],
            "total_price": 123.45,
            "payment_method": "CC",
            "payment_type": "RENT"
        }
        headers = make_auth_headers(user)
        response = client.post("/payments/", json=payload, headers=headers)
        assert response.status_code == 400

    def test_get_payment_owner(self, client, db, payment_factory, auth_headers):
        user = User.query.filter_by(email="user@werent.com").first()
        assert user is not None
        if not user.is_verified:
            user.is_verified = True
            user.save() if hasattr(user, 'save') else db.session.commit()
        payment = payment_factory(user=user)
        response = client.get(f"/payments/{payment.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()["data"]
        assert data["id"] == payment.id

    def test_get_payment_admin(self, client, payment_factory, admin_token, admin_user):
        payment = payment_factory(user=admin_user)
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get(f"/payments/{payment.id}", headers=headers)
        assert response.status_code == 200

    def test_get_payment_unauthorized(self, client, db, payment_factory, user_factory, make_auth_headers, auth_headers):
        owner = User.query.filter_by(email="user@werent.com").first()
        assert owner is not None
        if not owner.is_verified:
            owner.is_verified = True
            owner.save() if hasattr(owner, 'save') else db.session.commit()
        other = user_factory()
        db.session.commit()
        payment = payment_factory(user=owner)
        headers = make_auth_headers(other)
        response = client.get(f"/payments/{payment.id}", headers=headers)
        assert response.status_code == 401 or response.status_code == 403

    def test_update_payment_owner(self, client, db, payment_factory, auth_headers):
        user = User.query.filter_by(email="user@werent.com").first()
        assert user is not None
        if not user.is_verified:
            user.is_verified = True
            user.save() if hasattr(user, 'save') else db.session.commit()
        payment = payment_factory(user=user)
        payload = {"total_price": 555.55}
        response = client.put(f"/payments/{payment.id}", json=payload, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()["data"]
        assert data["total_price"] == 555.55

    def test_update_payment_admin(self, client, payment_factory, admin_token, admin_user):
        payment = payment_factory(user=admin_user)
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {"total_price": 777.77}
        response = client.put(f"/payments/{payment.id}", json=payload, headers=headers)
        assert response.status_code == 200
        data = response.get_json()["data"]
        assert data["total_price"] == 777.77

    def test_update_payment_unauthorized(self, client, db, payment_factory, user_factory, make_auth_headers, auth_headers):
        owner = User.query.filter_by(email="user@werent.com").first()
        assert owner is not None
        if not owner.is_verified:
            owner.is_verified = True
            owner.save() if hasattr(owner, 'save') else db.session.commit()
        other = user_factory()
        db.session.commit()
        payment = payment_factory(user=owner)
        headers = make_auth_headers(other)
        payload = {"total_price": 123.45}
        response = client.put(f"/payments/{payment.id}", json=payload, headers=headers)
        assert response.status_code == 401 or response.status_code == 403

    def test_delete_payment_owner(self, client, db, payment_factory, auth_headers):
        user = User.query.filter_by(email="user@werent.com").first()
        assert user is not None
        if not user.is_verified:
            user.is_verified = True
            user.save() if hasattr(user, 'save') else db.session.commit()
        payment = payment_factory(user=user)
        response = client.delete(f"/payments/{payment.id}", headers=auth_headers)
        assert response.status_code == 200

    def test_delete_payment_admin(self, client, payment_factory, admin_token, admin_user):
        payment = payment_factory(user=admin_user)
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.delete(f"/payments/{payment.id}", headers=headers)
        assert response.status_code == 200

    def test_delete_payment_unauthorized(self, client, db, payment_factory, user_factory, make_auth_headers, auth_headers):
        owner = User.query.filter_by(email="user@werent.com").first()
        assert owner is not None
        if not owner.is_verified:
            owner.is_verified = True
            owner.save() if hasattr(owner, 'save') else db.session.commit()
        other = user_factory()
        db.session.commit()
        payment = payment_factory(user=owner)
        headers = make_auth_headers(other)
        response = client.delete(f"/payments/{payment.id}", headers=headers)
        assert response.status_code == 401 or response.status_code == 403

    def test_get_all_payments_admin(self, client, admin_token):
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/payments/", headers=headers)
        assert response.status_code == 200
        data = response.get_json()["data"]
        assert isinstance(data, list)

    def test_get_all_payments_non_admin(self, client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/payments/", headers=headers)
        assert response.status_code == 401 or response.status_code == 403

    def test_get_payments_by_user_self(self, client, db, payment_factory, auth_headers):
        user = User.query.filter_by(email="user@werent.com").first()
        assert user is not None
        if not user.is_verified:
            user.is_verified = True
            user.save() if hasattr(user, 'save') else db.session.commit()
        payment = payment_factory(user=user)
        response = client.get(f"/payments/user/{user.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()["data"]
        assert isinstance(data, list)
        assert any(p["id"] == payment.id for p in data)

    def test_get_payments_by_user_admin(self, client, db, payment_factory, admin_token, admin_user, auth_headers):
        user = User.query.filter_by(email="user@werent.com").first()
        assert user is not None
        if not user.is_verified:
            user.is_verified = True
            user.save() if hasattr(user, 'save') else db.session.commit()
        payment = payment_factory(user=user)
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get(f"/payments/user/{user.id}", headers=headers)
        assert response.status_code == 200
        data = response.get_json()["data"]
        assert isinstance(data, list)
        assert any(p["id"] == payment.id for p in data)

    def test_get_payments_by_user_unauthorized(self, client, db, payment_factory, user_factory, make_auth_headers, auth_headers):
        owner = User.query.filter_by(email="user@werent.com").first()
        assert owner is not None
        if not owner.is_verified:
            owner.is_verified = True
            owner.save() if hasattr(owner, 'save') else db.session.commit()
        other = user_factory()
        db.session.commit()
        payment = payment_factory(user=owner)
        headers = make_auth_headers(other)
        response = client.get(f"/payments/user/{owner.id}", headers=headers)
        assert response.status_code == 401 or response.status_code == 403
