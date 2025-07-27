"""
Pytest tests for item routes in WeRent Backend API.
Covers CRUD operations, permissions, and authentication.

pytest tests/test_item_routes.py -v -s --cov=. --cov-report term-missing
"""
import json


class TestItemRoutes:
    # --- Coverage extension tests ---
    def test_create_item_invalid_payload(self, client, admin_token):
        # Missing required field
        item_data = {
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAM_INVALID',
            'description': 'Missing name',
            'price_per_day': 100.0,
            'images': []
        }
        resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 422
        data = resp.get_json()
        assert not data['success']

    def test_create_item_invalid_image(self, client, admin_token):
        # Invalid base64 image
        item_data = {
            'name': 'Invalid Image',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAM_IMG',
            'description': 'This description is valid.',
            'price_per_day': 100.0,
            'images': ['not_base64']
        }
        resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert (
            "Invalid image in images array: not a valid base64-encoded image"
            in data["error"]
        )

    def test_create_item_image_without_data_url(self, client, admin_token):
        # Valid base64, no data URL prefix
        # 1x1 transparent PNG
        img_str = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII="
        item_data = {
            'name': 'With Image',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAM_IMG2',
            'description': 'Image no data URL',
            'price_per_day': 100.0,
            'images': [img_str]
        }
        resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code in (200, 201)
        data = resp.get_json()
        assert data['success']

    def test_create_item_duplicate_product_code(self, client, admin_token):
        item_data = {
            'name': 'DupCode',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'CAMDUP',
            'description': 'Firstabcdfefaea',
            'price_per_day': 100.0,
            'images': []
        }
        # Create first item
        resp1 = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp1.status_code in (200, 201)
        # Try creating duplicate
        item_data['description'] = 'Second dwadwdadwad'
        resp2 = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp2.status_code == 400
        data = resp2.get_json()
        assert 'Product code already exists' in data['error']

    def test_get_item_not_found(self, client):
        resp = client.get('/items/999999')
        assert resp.status_code == 404
        data = resp.get_json()
        assert not data['success']
        assert 'not found' in data['error'].lower()

    def test_update_item_not_found(self, client, admin_token):
        update_data = {'name': 'DoesNotExist'}
        resp = client.put(
            '/items/999999',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 404
        data = resp.get_json()
        assert not data['success']

    def test_delete_item_not_found(self, client, admin_token):
        resp = client.delete(
            '/items/999999',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 404
        data = resp.get_json()
        assert not data['success']

    def test_update_item_invalid_image(self, client, admin_token):
        # Create item
        item_data = {
            'name': 'UpdImg',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'UPDIMG',
            'description': 'Upd img dwadwadwad',
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
        # Try update with invalid image
        update_data = {'images': ['not_base64']}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'not a valid base64-encoded image' in data['error']

    def test_update_item_image_without_data_url(self, client, admin_token):
        # Create item
        img_str = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII="
        item_data = {
            'name': 'UpdImg2',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'UPDIMG2',
            'description': 'Upd img2 wawdad',
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
        # Update with valid base64, no data url
        update_data = {'images': [img_str]}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success']

    def test_update_item_invalid_payload(self, client, admin_token):
        # Create item
        item_data = {
            'name': 'UpdInvalid',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'UPDINV',
            'description': 'Upd inv dwawdw',
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
        # Update with invalid payload
        update_data = {'price_per_day': 'not_a_number'}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert resp.status_code == 422
        data = resp.get_json()
        assert not data['success']

    def test_force_update_db_exception(self, client, admin_token, monkeypatch):
        # Create item
        item_data = {
            'name': 'ForceExc',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'FORCEEXC',
            'description': 'Force exc dwawda',
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
        # Patch db.session.commit to raise only during update
        def raise_exc():
            raise Exception('Simulated DB error')
        with monkeypatch.context() as m:
            m.setattr('app.db.session.commit', raise_exc)
            update_data = {'name': 'ShouldFail'}
            resp = client.put(
                f'/items/{item_id}',
                data=json.dumps(update_data),
                content_type='application/json',
                headers={'Authorization': f'Bearer {admin_token}'}
            )
            assert resp.status_code == 500
            data = resp.get_json()
            assert not data['success']

    def test_force_delete_db_exception(self, client, admin_token, monkeypatch):
        # Create item
        item_data = {
            'name': 'ForceDelExc',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Canon',
            'color': 'Black',
            'quantity': 1,
            'product_code': 'FORCEDELEXC',
            'description': 'Force del exc dwawda',
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
        # Patch db.session.commit to raise only during delete
        def raise_exc():
            raise Exception('Simulated DB error')
        with monkeypatch.context() as m:
            m.setattr('app.db.session.commit', raise_exc)
            resp = client.delete(
                f'/items/{item_id}',
                headers={'Authorization': f'Bearer {admin_token}'}
            )
            assert resp.status_code == 500
            data = resp.get_json()
            assert not data['success']


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
