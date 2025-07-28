"""
Item service for business logic operations.
Handles item management, availability, and item-related operations.
"""

from datetime import datetime
from app.services.base_service import BaseService
from app.models.item import Item


class ItemService(BaseService):
    """Service class for Item model business logic."""

    def __init__(self):
        """Initialize ItemService."""
        super().__init__(Item)

    def create_item(self, name, type, size, gender, brand, color, quantity, product_code, description, price_per_day, user_id):
        """Create a new item with all required model fields."""
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
        self.save(item)
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

    def update_item_details(self, item_id, **kwargs):
        """Update item details (image updates handled separately)."""
        item = self.get_by_id(item_id)
        if item:
            # Only allow certain fields to be updated (exclude image_base64)
            allowed_fields = ['title', 'description', 'price_per_day', 'category']
            update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
            return self.update(item, **update_data)
        return None

    def get_categories_with_counts(self):
        """Get all categories with item counts."""
        from sqlalchemy import func

        result = Item.query.with_entities(
            Item.category,
            func.count(Item.id).label('count')
        ).group_by(Item.category).all()

        return [{'category': cat, 'count': count} for cat, count in result]
