import pytest
from flask import url_for
from app.models.ticketing import Ticketing
from app.schemas.ticketing_schema import CreateTicketRequest, AddMessageRequest, TicketResponse
from app.services.ticketing_service import TicketingService
from app.models import User

# pytest tests/test_ticketing.py -v -s --cov=. --cov-report term-missing

# --- INTEGRATION TESTS: ROUTES ---


def test_create_ticket_route(client, db, booking_factory, auth_headers):
    # Use the user created by user_token/auth_headers fixture
    user = User.query.filter_by(email='user@werent.com').first()
    assert user is not None, "Test user not found in DB. Ensure user_token/auth_headers fixture runs first."
    booking = booking_factory(user=user)
    payload = {
        "message": "My item is broken!",
        "booking_id": booking.id
        # Do NOT set user_id; route will set it from JWT
    }
    response = client.post(
        "/api/tickets",
        json=payload,
        headers=auth_headers
    )
    assert response.status_code in (200, 201)
    data = response.get_json()["data"]
    assert "My item is broken!" in data["chat_content"]
    assert not data["is_resolved"]


def test_get_ticket_route(client, user_token, auth_headers, ticket_factory):
    from app.models import User
    user = User.query.filter_by(email='user@werent.com').first()
    assert user is not None, "Test user not found in DB."
    ticket = ticket_factory(user=user)
    response = client.get(f"/api/tickets/{ticket.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["id"] == ticket.id


def test_add_message_route(client, user_token, auth_headers, ticket_factory):

    user = User.query.filter_by(email='user@werent.com').first()
    assert user is not None, "Test user not found in DB."
    ticket = ticket_factory(user=user)
    payload = {"message": "Follow-up question."}
    response = client.post(f"/api/tickets/{ticket.id}/message", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert "Follow-up question." in data["chat_content"]


def test_resolve_ticket_route(client, admin_token, ticket_factory):
    ticket = ticket_factory()
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.patch(f"/api/tickets/{ticket.id}/resolve", headers=headers)
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["ticket"]["is_resolved"] is True


def test_reopen_ticket_route(client, admin_token, resolved_ticket):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.patch(f"/api/tickets/{resolved_ticket.id}/reopen", headers=headers)
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["ticket"]["is_resolved"] is False


def test_get_user_tickets_route(client, user_token, auth_headers, ticket_factory):
    from app.models import User
    user = User.query.filter_by(email='user@werent.com').first()
    assert user is not None, "Test user not found in DB."
    ticket = ticket_factory(user=user)
    response = client.get(f"/api/tickets/user/{ticket.user_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()["data"]["tickets"]
    found = any(ticket_dict.get("id") == ticket.id for ticket_dict in data)
    assert found, f"Ticket with id {ticket.id} not found in response: {data}"


def test_get_open_tickets_route(client, admin_token, open_ticket):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/tickets/open", headers=headers)
    assert response.status_code == 200
    data = response.get_json()["data"]["tickets"]
    found = any(ticket_dict.get("id") == open_ticket.id for ticket_dict in data)
    assert found, f"Ticket with id {open_ticket.id} not found in response: {data}"


def test_get_resolved_tickets_route(client, admin_token, resolved_ticket):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/tickets/resolved", headers=headers)
    assert response.status_code == 200
    data = response.get_json()["data"]["tickets"]
    found = any(ticket_dict.get("id") == resolved_ticket.id for ticket_dict in data)
    assert found, f"Ticket with id {resolved_ticket.id} not found in response: {data}"


def test_get_ticket_stats_route(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/tickets/stats", headers=headers)
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert "total_tickets" in data
    assert "open_tickets" in data
    assert "resolved_tickets" in data

# --- UNIT TESTS: SERVICE & SCHEMA ---

def test_ticketing_service_create_and_resolve(ticket_factory, user_factory, booking_factory):
    user = user_factory()
    booking = booking_factory(user=user)
    service = TicketingService()
    ticket = service.create_ticket(user.id, "Issue here", booking.id)
    assert ticket.user_id == user.id
    assert ticket.booking_id == booking.id
    assert "Issue here" in ticket.chat_content
    assert not ticket.is_resolved
    ticket = service.resolve_ticket(ticket.id)
    assert ticket.is_resolved


def test_schema_create_ticket_validation():
    # Valid
    req = CreateTicketRequest(user_id=1, message="Help!", booking_id=2)
    assert req.user_id == 1
    # Invalid message
    with pytest.raises(ValueError):
        CreateTicketRequest(user_id=1, message="   ")
    # Invalid booking_id
    with pytest.raises(ValueError):
        CreateTicketRequest(user_id=1, message="Valid", booking_id=0)


def test_schema_add_message_validation():
    # Valid
    req = AddMessageRequest(message="Hello")
    assert req.message == "Hello"
    # Invalid
    with pytest.raises(ValueError):
        AddMessageRequest(message="   ")


def test_ticket_model_to_dict(ticket_factory):
    ticket = ticket_factory()
    d = ticket.to_dict()
    assert d["id"] == ticket.id
    assert d["user_id"] == ticket.user_id
    assert isinstance(d["chat_content"], str)
    assert "created_at" in d
    assert "updated_at" in d
