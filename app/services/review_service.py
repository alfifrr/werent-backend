"""
Review service for business logic operations.
Handles reviews and ratings for items and users.
"""

from datetime import datetime
from app.services.base_service import BaseService
from app.models.review import Review
from app.services.item_service import ItemService
from app.services.user_service import UserService


class ReviewService(BaseService):
    """Service class for Review model business logic."""

    def __init__(self):
        """Initialize ReviewService."""
        super().__init__(Review)

    def create_review(self, item_id, user_id, rating, comment=None):
        """Create a new review for an item."""
        # Validate rating
        if not self.is_valid_rating(rating):
            raise ValueError("Rating must be between 1 and 5")

        # Check if user has already reviewed this item
        existing_review = self.get_user_review_for_item(user_id, item_id)
        if existing_review:
            raise ValueError("You have already reviewed this item")

        # Verify item and user exist
        item_service = ItemService()
        user_service = UserService()

        item = item_service.get_by_id(item_id)
        user = user_service.get_by_id(user_id)

        if not item:
            raise ValueError("Item not found")
        if not user:
            raise ValueError("User not found")

        # Check if user is trying to review their own item
        if item.user_id == user_id:
            raise ValueError("You cannot review your own item")

        review = Review()
        review.item_id = item_id
        review.user_id = user_id
        review.rating = rating
        review.review_message = comment.strip() if comment else None
        review.images = []

        saved_review = self.save(review)
        
        # Update item owner's average rating
        self.update_owner_rating(item.user_id)

        return saved_review

    def update_review(self, review_id, user_id, rating=None, comment=None):
        """Update an existing review."""
        review = self.get_by_id(review_id)

        if not self.is_valid_rating(rating):
            raise ValueError("Rating must be between 1 and 5")
        review.rating = rating

        if comment is not None:
            review.comment = comment.strip() if comment else None

        saved_review = self.save(review)

        # Update item owner's average rating
        self.update_owner_rating(review.item.user_id)

        return saved_review

    def delete_review(self, review_id, user_id):
        """Delete a review (only by the user who wrote it)."""
        review = self.get_by_id(review_id)
        if not review:
            return None

        if review.user_id != user_id:
            raise ValueError("You can only delete your own reviews")

        user_id_owner = review.item.user_id
        self.delete(review)

        # Update item owner's average rating after deletion
        self.update_owner_rating(user_id_owner)

        return True

    def get_reviews_by_item(self, item_id, limit=None):
        """Get all reviews for a specific item."""
        query = Review.query.filter_by(item_id=item_id).order_by(Review.created_at.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_reviews_by_user(self, user_id, limit=None):
        """Get all reviews written by a specific user."""
        query = Review.query.filter_by(user_id=user_id).order_by(Review.created_at.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_user_review_for_item(self, user_id, item_id):
        """Check if user has reviewed a specific item."""
        return Review.query.filter_by(user_id=user_id, item_id=item_id).first()

    def get_item_average_rating(self, item_id):
        """Calculate average rating for an item."""
        from sqlalchemy import func

        result = Review.query.with_entities(
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.id).label('review_count')
        ).filter_by(item_id=item_id).first()

        return {
            'average_rating': round(result.avg_rating, 2) if result.avg_rating else 0.0,
            'review_count': result.review_count
        }

    def get_reviews_by_rating(self, rating):
        """Get all reviews with a specific rating."""
        return Review.query.filter_by(rating=rating).order_by(Review.created_at.desc()).all()

    def get_recent_reviews(self, limit=10):
        """Get most recent reviews across all items."""
        return Review.query.order_by(Review.created_at.desc()).limit(limit).all()

    def get_top_reviews(self, limit=10):
        """Get reviews with highest ratings."""
        return Review.query.order_by(Review.rating.desc(), Review.created_at.desc()).limit(limit).all()

    def update_owner_rating(self, owner_id):
        """Update the average rating for an item owner."""
        from sqlalchemy import func
        from app.models.item import Item
        from app.services.user_service import UserService

        # Get average rating from all reviews of items owned by this user
        result = Review.query.join(Item).filter(
            Item.user_id == owner_id
        ).with_entities(func.avg(Review.rating)).first()

        user_service = UserService()
        user = user_service.get_by_id(owner_id)

        if user:
            user.avg_rating = round(result[0], 2) if result[0] else 0.0
            user_service.save(user)

    def get_review_statistics(self, item_id=None, user_id=None):
        """Get review statistics for an item or user."""
        from sqlalchemy import func

        query = Review.query

        if item_id:
            query = query.filter_by(item_id=item_id)
        elif user_id:
            # Get stats for all items owned by user
            from app.models.item import Item
            query = query.join(Item).filter(Item.user_id == user_id)

        stats = query.with_entities(
            func.count(Review.id).label('total_reviews'),
            func.avg(Review.rating).label('avg_rating'),
            func.min(Review.rating).label('min_rating'),
            func.max(Review.rating).label('max_rating')
        ).first()

        # Get rating distribution
        rating_distribution = {}
        for rating in range(1, 6):
            count = query.filter(Review.rating == rating).count()
            rating_distribution[f'{rating}_star'] = count

        return {
            'total_reviews': stats.total_reviews,
            'average_rating': round(stats.avg_rating, 2) if stats.avg_rating else 0.0,
            'min_rating': stats.min_rating,
            'max_rating': stats.max_rating,
            'rating_distribution': rating_distribution
        }

    def can_user_review_item(self, user_id, item_id):
        """Check if user can review an item (has completed booking, hasn't reviewed yet)."""
        from app.models.booking import Booking
        from app.models.item import Item
        from app.services.item_service import ItemService

        # Check if user has completed a booking for this item
        completed_booking = Booking.query.filter_by(
            renter_id=user_id,
            item_id=item_id,
            status='completed'
        ).first()

        if not completed_booking:
            return False, "You can only review items you have rented and completed"

        # Check if user hasn't already reviewed this item
        existing_review = self.get_user_review_for_item(user_id, item_id)
        if existing_review:
            return False, "You have already reviewed this item"

        # Check if user is not the owner
        item_service = ItemService()
        item = item_service.get_by_id(item_id)
        if item and item.user_id == user_id:
            return False, "You cannot review your own item"

        return True, "User can review this item"

    def get_owner_reviews(self, user_id, limit=None):
        """Get all reviews for items owned by a specific user."""
        from app.models.item import Item

        query = Review.query.join(Item).filter(Item.user_id == user_id).order_by(Review.created_at.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def is_valid_rating(self, rating):
        """Check if rating is valid (1-5)."""
        return isinstance(rating, int) and 1 <= rating <= 5

    def search_reviews(self, query_text, limit=20):
        """Search reviews by comment content."""
        return Review.query.filter(
            Review.comment.ilike(f'%{query_text}%')
        ).order_by(Review.created_at.desc()).limit(limit).all()
