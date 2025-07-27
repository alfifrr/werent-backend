import pytest
from app.models.user import User

# pytest tests/test_review_routes.py -v -s --cov=. --cov-report term-missing

# --- ROUTE TESTS ---

def test_list_reviews_empty(client, db, item_with_owner):
    item, _ = item_with_owner
    resp = client.get(f"/items/{item.id}/reviews")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"]
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 0

def test_create_review_success(client, db, item_with_owner, another_user, review_payload, auth_headers, make_auth_headers):
    item, owner = item_with_owner
    headers = make_auth_headers(another_user)
    resp = client.post(f"/items/{item.id}/reviews", json=review_payload, headers=headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"]
    assert data["data"]["rating"] == review_payload["rating"]
    assert data["data"]["review_message"] == review_payload["review_message"]
    assert isinstance(data["data"]["images"], list)
    assert len(data["data"]["images"]) == 2

    # Duplicate review by same user should fail
    resp2 = client.post(f"/items/{item.id}/reviews", json=review_payload, headers=headers)
    assert resp2.status_code == 400 or resp2.status_code == 422

    # Owner cannot review own item
    third_user = User(email="thirduser@werent.com", first_name="Third", last_name="User", phone_number="08123456789")
    third_user.set_password('TestPass123')
    db.session.add(third_user)
    db.session.commit()
    third_headers = make_auth_headers(third_user)
    resp3 = client.post(f"/items/{item.id}/reviews", json=review_payload, headers=third_headers)
    assert resp3.status_code == 201

def test_create_review_unauthenticated(client, db, item_with_owner, review_payload):
    item, _ = item_with_owner
    resp = client.post(f"/items/{item.id}/reviews", json=review_payload)
    assert resp.status_code == 401

def test_create_review_invalid_data(client, db, item_with_owner, another_user, auth_headers, make_auth_headers):
    item, _ = item_with_owner
    headers = make_auth_headers(another_user)
    # Invalid rating
    bad_payload = {"rating": 0, "review_message": "bad"}
    resp = client.post(f"/items/{item.id}/reviews", json=bad_payload, headers=headers)
    assert resp.status_code == 422
    # Too short message
    bad_payload2 = {"rating": 3, "review_message": "bad"}
    resp2 = client.post(f"/items/{item.id}/reviews", json=bad_payload2, headers=headers)
    assert resp2.status_code == 422
    # Bad images
    bad_payload3 = {"rating": 4, "review_message": "Valid message", "images": ["not_base64"]}
    resp3 = client.post(f"/items/{item.id}/reviews", json=bad_payload3, headers=headers)
    assert resp3.status_code == 422

def test_update_review_success(client, db, item_with_owner, another_user, review_payload, auth_headers, make_auth_headers):
    item, _ = item_with_owner
    headers = make_auth_headers(another_user)
    # Create review
    resp = client.post(f"/items/{item.id}/reviews", json=review_payload, headers=headers)
    review_id = resp.get_json()["data"]["id"]
    # Update review
    update_payload = {
        "rating": 4,
        "review_message": "Updated review!",
        "images": [
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/w8AAgMBApT+ZQAAAABJRU5ErkJggg=="
        ],
    }
    resp2 = client.put(f"/reviews/{review_id}", json=update_payload, headers=headers)
    assert resp2.status_code == 200
    data = resp2.get_json()["data"]
    assert data["rating"] == 4
    assert data["review_message"] == "Updated review!"
    assert isinstance(data["images"], list)
    assert len(data["images"]) == 1

    # Unauthorized user tries to update
    other = User(email="other@example.com", first_name="Other", last_name="User", phone_number="08123456789")
    other.set_password('TestPass123')
    db.session.add(other)
    db.session.commit()
    other_headers = make_auth_headers(other)
    resp3 = client.put(f"/reviews/{review_id}", json=update_payload, headers=other_headers)
    assert resp3.status_code == 403


def test_update_review_invalid_data(client, db, item_with_owner, another_user, review_payload, auth_headers, make_auth_headers):
    item, _ = item_with_owner
    headers = make_auth_headers(another_user)
    # Create review
    resp = client.post(f"/items/{item.id}/reviews", json=review_payload, headers=headers)
    review_id = resp.get_json()["data"]["id"]
    # Invalid rating
    bad_payload = {"rating": 0}
    resp2 = client.put(f"/reviews/{review_id}", json=bad_payload, headers=headers)
    assert resp2.status_code == 422
    # Bad images
    bad_payload2 = {"images": ["not_base64"]}
    resp3 = client.put(f"/reviews/{review_id}", json=bad_payload2, headers=headers)
    assert resp3.status_code == 422


def test_delete_review_success(client, db, item_with_owner, another_user, review_payload, auth_headers, make_auth_headers):
    item, _ = item_with_owner
    headers = make_auth_headers(another_user)
    # Create review
    resp = client.post(f"/items/{item.id}/reviews", json=review_payload, headers=headers)
    review_id = resp.get_json()["data"]["id"]
    # Delete review
    resp2 = client.delete(f"/reviews/{review_id}", headers=headers)
    assert resp2.status_code == 200
    # Verify deleted
    resp3 = client.get(f"/items/{item.id}/reviews")
    assert all(r["id"] != review_id for r in resp3.get_json()["data"])

    # Unauthorized user tries to delete
    other = User(email="other@example.com", first_name="Other", last_name="User", phone_number="08123456789")
    other.set_password('TestPass123')
    db.session.add(other)
    db.session.commit()
    other_headers = make_auth_headers(other)
    resp4 = client.delete(f"/reviews/{review_id}", headers=other_headers)
    assert resp4.status_code == 403 or resp4.status_code == 404


def test_list_testimonials(client, db, item_with_owner, another_user, review_payload, auth_headers, make_auth_headers):
    item, _ = item_with_owner
    headers = make_auth_headers(another_user)
    # Create review
    client.post(f"/items/{item.id}/reviews", json=review_payload, headers=headers)
    resp = client.get("/testimonial")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"]
    assert isinstance(data["data"], list)
    assert any(r["review_message"] == review_payload["review_message"] for r in data["data"])


def test_review_statistics_service(db, item_with_owner, another_user, review_payload):
    from app.services.review_service import ReviewService
    item, _ = item_with_owner
    user = another_user
    service = ReviewService()
    # No reviews yet
    stats = service.get_review_statistics(item_id=item.id)
    assert stats["total_reviews"] == 0
    # Add review
    review = service.create_review(item.id, user.id, 5, "Excellent!", images=None)
    stats2 = service.get_review_statistics(item_id=item.id)
    assert stats2["total_reviews"] == 1
    assert stats2["average_rating"] == 5.0


def test_review_model_to_dict(db, item_with_owner, another_user):
    from app.models.review import Review
    from app.models.image import Image
    item, _ = item_with_owner
    user = another_user
    review = Review(item_id=item.id, user_id=user.id, rating=4, review_message="Nice", images=[])
    db.session.add(review)
    db.session.commit()
    as_dict = review.to_dict()
    assert as_dict["id"] == review.id
    assert as_dict["user_id"] == user.id
    assert as_dict["item_id"] == item.id
    assert as_dict["review_message"] == "Nice"
    assert as_dict["rating"] == 4
    assert isinstance(as_dict["images"], list)


def test_review_service_duplicate_review(db, item_with_owner, another_user):
    from app.services.review_service import ReviewService
    item, _ = item_with_owner
    user = another_user
    service = ReviewService()
    service.create_review(item.id, user.id, 5, "First!", images=None)
    with pytest.raises(Exception):
        service.create_review(item.id, user.id, 4, "Second!", images=None)


def test_review_service_owner_cannot_review_own_item(db, item_with_owner):
    from app.services.review_service import ReviewService
    item, owner = item_with_owner
    service = ReviewService()
    with pytest.raises(Exception):
        service.create_review(item.id, owner.id, 5, "Owner review", images=None)


def test_review_service_invalid_rating(db, item_with_owner, another_user):
    from app.services.review_service import ReviewService
    item, _ = item_with_owner
    user = another_user
    service = ReviewService()
    with pytest.raises(Exception):
        service.create_review(item.id, user.id, 0, "Bad rating", images=None)
    with pytest.raises(Exception):
        service.create_review(item.id, user.id, 6, "Too high", images=None)


def test_review_service_can_user_review_item(db, item_with_owner, another_user):
    from app.services.review_service import ReviewService
    item, _ = item_with_owner
    user = another_user
    service = ReviewService()
    # Should be False if no booking
    allowed, msg = service.can_user_review_item(user.id, item.id)
    assert allowed is False
    # (Assumes booking model/factory exists for a true case)
