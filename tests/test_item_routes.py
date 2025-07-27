"""
Pytest tests for item routes in WeRent Backend API.
Covers CRUD operations, permissions, and authentication.
uv run pytest tests/test_item_routes.py -v -s --cov=. --cov-report term-missing
pytest tests/test_item_routes.py -v -s --cov=. --cov-report term-missing
pytest tests/test_item_routes.py -v -s --cov=. --cov-report term-missing --tb=long
"""
import json


class TestItemRoutes:
    def test_list_items(self, client):
        resp = client.get('/items')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'data' in data

    def test_create_item_admin(self, client, admin_token):
        item_data = {
            'name': 'Test Camera',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAM123',
            'description': 'A camera for testing purposes',
            'price_per_day': 100.0,
            'images': []
        }
        resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code in (200, 201)
        data = resp.get_json()
        assert data['success'] is True
        assert 'id' in data['data']

    def test_create_item_non_admin(self, client, user_token):
        item_data = {
            'name': 'Test Camera',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAM123',
            'description': 'A camera for testing purposes',
            'price_per_day': 100.0,
            'images': []
        }
        resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert resp.status_code == 403  # Forbidden

    def test_create_item_unauthenticated(self, client):
        item_data = {
            'name': 'Test Camera',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAM123',
            'description': 'A camera for testing purposes',
            'price_per_day': 100.0,
            'images': []
        }
        resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json'
        )
        assert resp.status_code == 401  # Unauthorized

    def test_get_item(self, client, admin_token):
        # First, create item as admin
        item_data = {
            'name': 'Test Camera',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAM123',
            'description': 'A camera for testing purposes',
            'price_per_day': 100.0,
            'images': []
        }
        create_resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        item_id = create_resp.get_json()['data']['id']
        # Now, fetch it
        resp = client.get(f'/items/{item_id}')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['data']['id'] == item_id

    def test_update_item_admin(self, client, admin_token):
        # Create item
        item_data = {
            'name': 'Old Camera',
            'type': 'Dress',
            'size': 'L',
            'gender': 'UNISEX',
            'brand': 'Nikon',
            'color': 'Silver',
            'quantity': 1,
            'product_code': 'CAM456',
            'description': 'Old desc for update',
            'price_per_day': 50.0,
            'images': []
        }
        create_resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        item_id = create_resp.get_json()['data']['id']
        # Update
        update_data = {'name': 'New Name'}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 200
        data = resp.get_json()['data']
        assert data['name'] == 'New Name'

    def test_update_item_non_admin(self, client, user_token, admin_token):
        # Create item as admin
        item_data = {
            'name': 'Old Camera',
            'type': 'Dress',
            'size': 'L',
            'gender': 'UNISEX',
            'brand': 'Nikon',
            'color': 'Silver',
            'quantity': 1,
            'product_code': 'CAM456',
            'description': 'Old desc for update',
            'price_per_day': 50.0,
            'images': []
        }
        create_resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        item_id = create_resp.get_json()['data']['id']
        # Try update as non-admin
        update_data = {'title': 'Hacked Title'}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert resp.status_code == 403

    def test_delete_item_admin(self, client, admin_token):
        # Create item
        item_data = {
            'name': 'To Delete',
            'type': 'Dress',
            'size': 'S',
            'gender': 'UNISEX',
            'brand': 'Sony',
            'color': 'White',
            'quantity': 1,
            'product_code': 'CAM789',
            'description': 'desc for delete',
            'price_per_day': 10.0,
            'images': []
        }
        create_resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        item_id = create_resp.get_json()['data']['id']
        # Delete
        resp = client.delete(
            f'/items/{item_id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success'] is True

    def test_delete_item_non_admin(self, client, user_token, admin_token):
        # Create item as admin
        item_data = {
            'name': 'To Delete',
            'type': 'Dress',
            'size': 'S',
            'gender': 'UNISEX',
            'brand': 'Sony',
            'color': 'White',
            'quantity': 1,
            'product_code': 'CAM789',
            'description': 'desc for delete',
            'price_per_day': 10.0,
            'images': []
        }
        create_resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        item_id = create_resp.get_json()['data']['id']
        # Try delete as non-admin
        resp = client.delete(
            f'/items/{item_id}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert resp.status_code == 403
