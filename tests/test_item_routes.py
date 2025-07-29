"""
Pytest tests for item routes in WeRent Backend API.
Covers CRUD operations, permissions, and authentication.

pytest tests/test_item_routes.py -v -s --cov=. --cov-report term-missing
"""
import json
from app.models.image import Image


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
        # Test various invalid image formats
        invalid_images = [
            'not_base64',  # Not base64
            'data:image/png;base64,invalid_base64',  # Invalid base64
            'data:image/invalid;base64,SGVsbG8gV29ybGQh',  # Invalid MIME type
            'data:text/plain;base64,SGVsbG8gV29ybGQh'  # Not an image
        ]
        
        for img in invalid_images:
            item_data = {
                'name': f'Invalid Image - {img[:10]}...',
                'type': 'Dress',
                'size': 'M',
                'gender': 'UNISEX',
                'brand': 'Canon',
                'color': 'Black',
                'quantity': 1,
                'product_code': f'INVALID_{hash(img) % 10000}',
                'description': 'Testing invalid image format',
                'price_per_day': 100.0,
                'images': [img]
            }
            resp = client.post(
                '/items',
                data=json.dumps(item_data),
                content_type='application/json',
                headers={'Authorization': f'Bearer {admin_token}'}
            )
            # Expecting 422 for validation errors
            assert resp.status_code == 422, f"Expected 422 for image: {img}"
            data = resp.get_json()
            assert "error" in data, f"Expected error in response for image: {img}"
            assert "validation" in str(data["error"]).lower(), f"Expected validation error for image: {img}"

    def test_create_item_with_images(self, client, admin_token, test_images):
        """Test creating an item with various image formats."""
        item_data = {
            'name': 'Item With Multiple Images',
            'type': 'Dress',
            'size': 'M',
            'gender': 'UNISEX',
            'brand': 'Test Brand',
            'color': 'Red',
            'quantity': 1,
            'product_code': 'IMG_TEST_1',
            'description': 'Item with multiple image formats',
            'price_per_day': 150.0,
            'images': test_images  # Includes raw base64 and data URL formats
        }
        
        # Create item with images
        resp = client.post(
            '/items',
            data=json.dumps(item_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert resp.status_code in (200, 201)
        data = resp.get_json()
        assert data['success']
        assert 'data' in data
        assert 'images' in data['data']
        assert len(data['data']['images']) == len(test_images)
        
        # Verify image URLs are properly formatted
        for img in data['data']['images']:
            assert 'id' in img
            assert 'image_base64' in img
            assert img['image_base64'].startswith('data:image/')
            assert 'created_at' in img

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

    def test_update_item_with_images(self, client, admin_token, test_images, item_factory):
        """Test updating an item with new images."""
        # First create an item without images
        item = item_factory()  # Call the factory function
        item_id = item.id
        
        # Update item with new images
        update_data = {
            'name': 'Updated With Images',
            'description': 'Now with images!',
            'images': test_images[:2]  # Use first two test images
        }
        
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success']
        assert 'data' in data
        assert 'images' in data['data']
        assert len(data['data']['images']) == 2  # Should have exactly 2 images
        
        # Verify the images were saved correctly
        for img in data['data']['images']:
            assert 'id' in img
            assert 'image_base64' in img
            assert img['image_base64'].startswith('data:image/')
        
        # Verify other fields were updated
        assert data['data']['name'] == 'Updated With Images'
        assert data['data']['description'] == 'Now with images!'
        
        # Test updating with different set of images (should replace existing ones)
        update_data = {
            'images': [test_images[2]]  # Use the third test image
        }
        
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success']
        assert len(data['data']['images']) == 1  # Should now have only 1 image
        assert data['data']['images'][0]['image_base64'].startswith('data:image/')
        
        # Test removing all images
        update_data = {
            'images': []
        }
        
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['success']
        assert 'images' in data['data']
        assert len(data['data']['images']) == 0  # Should have no images now

    def test_update_item_not_owner(self, client, user_token, item_factory, admin_token):
        """Test that non-owners cannot update an item."""
        # Create an item owned by admin
        item = item_factory()  # Call the factory function
        
        # Try to update as a different user
        update_data = {'name': 'Unauthorized Update'}
        resp = client.put(
            f'/items/{item.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        
        assert resp.status_code == 403
        data = resp.get_json()
        assert not data['success']
        assert 'admin access required' in data['error'].lower()

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

    def test_update_item_invalid_image(self, client, admin_token, item_factory):
        # Create item using factory
        item = item_factory()
        item_id = item.id
        
        # Try update with invalid image
        update_data = {'images': ['not_base64']}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        # The API should return 422 for invalid image data
        assert resp.status_code == 422
        data = resp.get_json()
        assert 'error' in data
        assert 'One or more images are not valid base64 images' in data['error']

    def test_update_item_image_without_data_url(self, client, admin_token, item_factory):
        # Create item using factory
        item = item_factory()
        item_id = item.id
        
        # Update with valid base64, no data url
        img_str = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Kk2cAAAAASUVORK5CYII="
        update_data = {'images': [img_str]}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        # Expect 200 for successful update
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

    def test_force_update_db_exception(self, client, admin_token, monkeypatch, item_factory):
        # Create item using factory
        item = item_factory()
        item_id = item.id
        
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
            # Expect 500 for server error
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

    def test_update_item_admin(self, client, admin_token, item_factory):
        # Create item using factory
        item = item_factory()
        item_id = item.id
        
        # Update
        update_data = {'name': 'New Name'}
        resp = client.put(
            f'/items/{item_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        # Expect 200 for successful update
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
