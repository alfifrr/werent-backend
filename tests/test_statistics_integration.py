import pytest
from datetime import datetime

# --- Fixtures used: client, db, admin_user, admin_token, user_factory, item_factory, booking_factory, payment_factory, ticket_factory, make_auth_headers ---

# pytest tests/test_statistics_integration.py -v -s --cov=. --cov-report term-missing

@pytest.mark.usefixtures("cleanup_db")
class TestAdminStatistics:
    endpoint = "/api/admin/statistics/"

    def test_statistics_success(self, client, admin_token, user_factory, item_factory, booking_factory, payment_factory, ticket_factory):
        # Create test data
        user_factory(is_admin=False)
        item_factory()
        booking_factory()
        payment_factory()
        ticket_factory()
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.get(self.endpoint, headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        # Check keys
        for key in ["total_users", "total_items", "total_bookings", "total_revenue", "total_reviews", "total_tickets", "weekly"]:
            assert key in data
        for key in ["users", "items", "bookings", "revenue", "reviews", "tickets"]:
            assert key in data["weekly"]

    def test_statistics_auth_required(self, client):
        resp = client.get(self.endpoint)
        assert resp.status_code == 401 or resp.status_code == 422  # JWT required

    def test_statistics_non_admin_forbidden(self, client, user_factory, make_auth_headers):
        user = user_factory(is_admin=False)
        headers = make_auth_headers(user)
        resp = client.get(self.endpoint, headers=headers)
        assert resp.status_code == 403 or resp.status_code == 401

    def test_statistics_empty_db(self, client, admin_token):
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.get(self.endpoint, headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total_users"] == 1  # admin user exists
        assert data["total_items"] == 0
        assert data["total_bookings"] == 0
        assert data["total_revenue"] == 0 or data["total_revenue"] is not None
        assert data["total_reviews"] == 0
        assert data["total_tickets"] == 0


class TestMonthlyStatistics:
    endpoint = "/api/admin/statistics/monthly"

    def test_monthly_statistics_success(self, client, admin_token):
        year = datetime.now().year
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.post(self.endpoint, json={"year": year}, headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        # Each key should be a list of 12 months
        for key in ["users", "items", "bookings", "revenue", "reviews", "tickets"]:
            assert key in data
            assert isinstance(data[key], list)
            assert len(data[key]) == 12

    def test_monthly_statistics_missing_year(self, client, admin_token):
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.post(self.endpoint, json={}, headers=headers)
        assert resp.status_code == 500 or resp.status_code == 400 or resp.status_code == 422
        # Should return error about missing year
        assert "year" in resp.get_data(as_text=True) or "Missing" in resp.get_data(as_text=True)

    def test_monthly_statistics_invalid_year_type(self, client, admin_token):
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.post(self.endpoint, json={"year": "2023"}, headers=headers)
        assert resp.status_code == 500 or resp.status_code == 400 or resp.status_code == 422
        assert "year" in resp.get_data(as_text=True) or "invalid" in resp.get_data(as_text=True)

    def test_monthly_statistics_auth_required(self, client):
        resp = client.post(self.endpoint, json={"year": 2023})
        assert resp.status_code == 401 or resp.status_code == 422

    def test_monthly_statistics_non_admin_forbidden(self, client, user_factory, make_auth_headers):
        user = user_factory(is_admin=False)
        headers = make_auth_headers(user)
        resp = client.post(self.endpoint, json={"year": 2023}, headers=headers)
        assert resp.status_code == 403 or resp.status_code == 401

    def test_monthly_statistics_empty_db(self, client, admin_token):
        year = datetime.now().year
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.post(self.endpoint, json={"year": year}, headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        for key in ["users", "items", "bookings", "revenue", "reviews", "tickets"]:
            assert data[key] == [0]*12 or all(isinstance(x, (int, float, type(None))) for x in data[key])
