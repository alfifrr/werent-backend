"""
Item service for business logic operations.
Handles item management, availability, and item-related operations.
"""

from app.services.base_service import BaseService
from app.models.item import Item
from app.models.image import Image
from app.extensions import db


class ItemService(BaseService):
    """Service class for Item model business logic."""

    def __init__(self):
        """Initialize ItemService."""
        super().__init__(Item)

    def save_item_images(self, item_id, images):
        """
        Save multiple images for an item.
        
        Args:
            item_id (int): ID of the item to save images for
            images (list): List of base64-encoded image strings
            
        Returns:
            list: List of saved image objects
        """
        saved_images = []
        for img in images:
            # Ensure the image has the data URL prefix
            if not img.startswith('data:image'):
                img = f'data:image/jpeg;base64,{img}'
                
            # Create and save the image
            image = Image(
                image_base64=img,
                item_id=item_id
            )
            db.session.add(image)
            saved_images.append(image)
            
        db.session.commit()
        return saved_images
        
    def create_item(self, name, type, size, gender, brand, color, quantity, product_code, description, price_per_day, user_id, images=None):
        """
        Create a new item with all required model fields and optional images.
        
        Args:
            name (str): Item name
            type (str): Item type/category
            size (str): Item size
            gender (str): Item gender
            brand (str, optional): Item brand
            color (str, optional): Item color
            quantity (int): Available quantity
            product_code (str): Unique product code
            description (str): Item description
            price_per_day (float): Price per day
            user_id (int): ID of the user creating the item
            images (list, optional): List of base64-encoded images
            
        Returns:
            Item: The created item with images loaded
        """
        item = Item(
            name=name,
            type=type,
            size=size,
            gender=gender,
            brand=brand,
            color=color,
            quantity=quantity,
            product_code=product_code,
            description=description,
            price_per_day=price_per_day,
            user_id=user_id
        )
        
        # Save the item first to get an ID
        self.save(item)
        
        # Save images if provided
        if images:
            self.save_item_images(item.id, images)
            
        # Refresh the item to include the images in the response
        db.session.refresh(item)
        return item

    def get_available_items(self):
        """Get all items (status filter removed)."""
        return Item.query.all()

    def get_items_by_owner(self, user_id):
        """Get all items owned by a specific user."""
        return Item.query.filter_by(user_id=user_id).all()

    def get_items_by_category(self, category):
        """Get items by category."""
        return Item.query.filter_by(category=category).all()

    def search_items(self, query):
        """Search items by title or description."""
        return Item.query.filter(
            (Item.title.ilike(f'%{query}%')) |
            (Item.description.ilike(f'%{query}%'))
        ).all()


    def mark_as_rented(self, item_id):
        """Mark item as rented."""
        return self.update_item_status(item_id, 'rented')

    def mark_as_available(self, item_id):
        """Mark item as available."""
        return self.update_item_status(item_id, 'available')

    def mark_as_maintenance(self, item_id):
        """Mark item as under maintenance."""
        return self.update_item_status(item_id, 'maintenance')

    def is_item_available(self, item_id):
        """Check if item is available for booking."""
        item = self.get_by_id(item_id)
        return item and item.status == 'available'

    def calculate_item_rating(self, item_id):
        """Calculate average rating for an item."""
        item = self.get_by_id(item_id)
        if not item or not item.reviews:
            return 0.0

        total_rating = sum(review.rating for review in item.reviews)
        return round(total_rating / len(item.reviews), 2)

    def get_item_stats(self, item_id):
        """Get item statistics."""
        item = self.get_by_id(item_id)
        if not item:
            return None

        return {
            'total_bookings': len(item.bookings),
            'total_reviews': len(item.reviews),
            'average_rating': self.calculate_item_rating(item_id),
            'total_images': len(item.images),
            'status': item.status,
            'created_at': item.created_at.isoformat()
        }

    def get_popular_items(self, limit=10):
        """Get most popular items based on booking count."""
        from sqlalchemy import func
        from app.models.booking import Booking

        return Item.query.join(Booking).group_by(Item.id).order_by(
            func.count(Booking.id).desc()
        ).limit(limit).all()

    def get_top_rated_items(self, limit=10):
        """Get top rated items."""
        from sqlalchemy import func
        from app.models.review import Review

        return Item.query.join(Review).group_by(Item.id).order_by(
            func.avg(Review.rating).desc()
        ).limit(limit).all()

    def get_recently_added_items(self, limit=10):
        """Get recently added items."""
        return Item.query.order_by(Item.created_at.desc()).limit(limit).all()

    def filter_items(self, category=None, min_price=None, max_price=None, status='available'):
        """Filter items by various criteria."""
        query = Item.query


        if category:
            query = query.filter_by(category=category)

        if min_price is not None:
            query = query.filter(Item.price_per_day >= min_price)

        if max_price is not None:
            query = query.filter(Item.price_per_day <= max_price)

        return query.all()

    def get_item_availability_calendar(self, item_id, start_date, end_date):
        """Get item availability for a date range."""
        from app.models.booking import Booking

        item = self.get_by_id(item_id)
        if not item:
            return None

        # Get all confirmed bookings for this item in the date range
        conflicting_bookings = Booking.query.filter(
            Booking.item_id == item_id,
            Booking.status == 'confirmed',
            Booking.start_date <= end_date,
            Booking.end_date >= start_date
        ).all()

        return {
            'item_id': item_id,
            'is_available': len(conflicting_bookings) == 0,
            'conflicting_bookings': [booking.to_dict() for booking in conflicting_bookings]
        }

    def update_item(self, item_id, **kwargs):
        """
        Update an item and optionally its images.
        
        Args:
            item_id (int): ID of the item to update
            **kwargs: Item fields to update, including optional 'images' list
            
        Returns:
            Item: The updated item with images loaded, or None if not found
        """
        item = self.get_by_id(item_id)
        if not item:
            return None
            
        # Handle image updates if provided
        images = kwargs.pop('images', None)
        if images is not None:
            # Delete existing images
            Image.query.filter_by(item_id=item_id).delete()
            # Save new images
            self.save_item_images(item_id, images)
            
        # Update other fields
        allowed_fields = ['name', 'type', 'size', 'gender', 'brand', 'color', 
                         'quantity', 'product_code', 'description', 'price_per_day']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        updated_item = self.update(item, **update_data)
        if updated_item:
            # Refresh to include the updated images in the response
            db.session.refresh(updated_item)
        return updated_item
        
    def update_item_details(self, item_id, **kwargs):
        """
        Update item details (legacy method, consider using update_item instead).
        
        This is kept for backward compatibility but delegates to update_item.
        """
        return self.update_item(item_id, **kwargs)

    def get_categories_with_counts(self):
        """Get all categories with item counts."""
        from sqlalchemy import func

        result = Item.query.with_entities(
            Item.category,
            func.count(Item.id).label('count')
        ).group_by(Item.category).all()

        return [{'category': cat, 'count': count} for cat, count in result]
