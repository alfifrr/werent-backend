"""
Image service for business logic operations.
Handles image management for items.
"""

from app.services.base_service import BaseService
from app.models.image import Image


class ImageService(BaseService):
    """Service class for Image model business logic."""

    def __init__(self):
        """Initialize ImageService."""
        super().__init__(Image)

    def add_image_to_item(self, item_id, url, order=0):
        """Add a new image to an item."""
        # Verify item exists
        from app.services.item_service import ItemService
        item_service = ItemService()
        item = item_service.get_by_id(item_id)

        if not item:
            raise ValueError("Item not found")

        # If no order specified, set it to the next available order
        if order == 0:
            max_order = Image.query.filter_by(item_id=item_id).order_by(Image.order.desc()).first()
            order = (max_order.order + 1) if max_order else 1

        image = Image()
        image.item_id = item_id
        image.url = url
        image.order = order

        return self.save(image)

    def get_images_by_item(self, item_id):
        """Get all images for a specific item, ordered by order field."""
        return Image.query.filter_by(item_id=item_id).order_by(Image.order).all()

    def update_image_order(self, image_id, new_order):
        """Update the order of an image."""
        image = self.get_by_id(image_id)
        if not image:
            return None

        image.order = new_order
        return self.save(image)

    def reorder_images(self, item_id, image_order_list):
        """Reorder all images for an item based on list of image IDs."""
        # image_order_list should be a list of image IDs in the desired order
        for index, image_id in enumerate(image_order_list, 1):
            image = self.get_by_id(image_id)
            if image and image.item_id == item_id:
                image.order = index
                self.save(image)

    def delete_image(self, image_id, user_id):
        """Delete an image (only by item owner)."""
        image = self.get_by_id(image_id)
        if not image:
            return None

        # Check if user is the owner of the item
        from app.services.item_service import ItemService
        item_service = ItemService()
        item = item_service.get_by_id(image.item_id)

        if not item or item.owner_id != user_id:
            raise ValueError("You can only delete images from your own items")

        self.delete(image)

        # Reorder remaining images to close gaps
        remaining_images = self.get_images_by_item(image.item_id)
        for index, img in enumerate(remaining_images, 1):
            if img.order != index:
                img.order = index
                self.save(img)

        return True

    def set_primary_image(self, image_id, user_id):
        """Set an image as the primary image (order = 1) for an item."""
        image = self.get_by_id(image_id)
        if not image:
            return None

        # Check if user is the owner of the item
        from app.services.item_service import ItemService
        item_service = ItemService()
        item = item_service.get_by_id(image.item_id)

        if not item or item.owner_id != user_id:
            raise ValueError("You can only modify images from your own items")

        # Get current primary image
        current_primary = Image.query.filter_by(item_id=image.item_id, order=1).first()

        if current_primary and current_primary.id != image.id:
            # Swap orders
            current_primary.order = image.order
            self.save(current_primary)

        image.order = 1
        return self.save(image)

    def get_primary_image(self, item_id):
        """Get the primary image (order = 1) for an item."""
        return Image.query.filter_by(item_id=item_id, order=1).first()

    def count_images_by_item(self, item_id):
        """Count total images for an item."""
        return Image.query.filter_by(item_id=item_id).count()

    def validate_image_url(self, url):
        """Validate image URL format."""
        import re

        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(url):
            raise ValueError("Invalid URL format")

        # Check if URL ends with image extension
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        if not any(url.lower().endswith(ext) for ext in image_extensions):
            raise ValueError("URL must point to an image file")

        return True

    def bulk_add_images(self, item_id, image_urls):
        """Add multiple images to an item at once."""
        # Verify item exists
        from app.services.item_service import ItemService
        item_service = ItemService()
        item = item_service.get_by_id(item_id)

        if not item:
            raise ValueError("Item not found")

        # Get the current highest order
        max_order = Image.query.filter_by(item_id=item_id).order_by(Image.order.desc()).first()
        current_order = (max_order.order if max_order else 0)

        created_images = []
        for url in image_urls:
            # Validate each URL
            self.validate_image_url(url)

            current_order += 1
            image = Image()
            image.item_id = item_id
            image.url = url
            image.order = current_order

            created_images.append(self.save(image))

        return created_images

    def update_image_url(self, image_id, new_url, user_id):
        """Update image URL."""
        image = self.get_by_id(image_id)
        if not image:
            return None

        # Check if user is the owner of the item
        from app.services.item_service import ItemService
        item_service = ItemService()
        item = item_service.get_by_id(image.item_id)

        if not item or item.owner_id != user_id:
            raise ValueError("You can only modify images from your own items")

        # Validate new URL
        self.validate_image_url(new_url)

        image.url = new_url
        return self.save(image)

    def get_image_statistics(self):
        """Get overall image statistics."""
        from sqlalchemy import func

        stats = Image.query.with_entities(
            func.count(Image.id).label('total_images'),
            func.count(func.distinct(Image.item_id)).label('items_with_images')
        ).first()

        return {
            'total_images': stats.total_images,
            'items_with_images': stats.items_with_images
        }
