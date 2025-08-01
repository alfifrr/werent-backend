"""
Review service for business logic operations.
Handles reviews and ratings for items and users.
"""

from ast import Str
from app.services.base_service import BaseService
from app.models.review import Review
from app.services.item_service import ItemService
from app.services.user_service import UserService
from app.models.image import Image
from app.models.booking import Booking
from app.extensions import db
from app.models.item import Item


class ReviewService(BaseService):
    """Service class for Review model business logic."""

    def get_all_reviews(self):
        """Get all reviews (testimonials) in the system, ordered by creation date descending."""
        return Review.query.order_by(Review.created_at.desc()).all()

    def __init__(self):
        """Initialize ReviewService."""
        super().__init__(Review)

    def create_review(self, item_id, user_id, rating, comment=None, images=None):
        """Create a new review for an item, with optional images."""
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

        # Save review first to get ID and commit it to the database
        db.session.add(review)
        db.session.flush()  # Flush to get the review ID without committing the transaction

        # Handle images
        if images:
            for img_b64 in images:
                image = Image(image_base64=img_b64, review_id=review.id)
                db.session.add(image)
                if not review.images:
                    review.images = []
                review.images.append(image)
        
        # Commit the review and its images
        db.session.commit()
        
        # Now refresh the item to get the latest reviews
        db.session.refresh(item)
        
        # Update item's rating and owner's average rating
        item.update_rating()
        self.update_owner_rating(item.user_id)
        
        # Get the saved review with relationships loaded
        saved_review = self.get_by_id(review.id)

        return saved_review

    def update_review(self, review_id, user_id, rating=None, comment=None, images=None):
        """Update an existing review, including images if provided."""
        review = self.get_by_id(review_id)
        if not review:
            raise ValueError("Review not found")

        if not self.is_valid_rating(rating):
            raise ValueError("Rating must be between 1 and 5")
            
        # Store the old rating to check if it changed
        old_rating = review.rating
        review.rating = rating

        if comment is not None:
            review.review_message = comment.strip() if comment else None

        # Handle image update: if images provided, replace all
        if images is not None:
            # Delete old images
            for img in list(review.images):
                db.session.delete(img)
            review.images = []
            # Add new images
            for img_b64 in images:
                image = Image(image_base64=img_b64, review_id=review.id)
                db.session.add(image)
                review.images.append(image)
        
        # Save changes
        db.session.add(review)
        db.session.commit()
        
        # Only update ratings if the rating actually changed
        if old_rating != rating:
            # Refresh the item to get the latest reviews
            db.session.refresh(review.item)
            # Update item's rating and owner's average rating
            review.item.update_rating()
            self.update_owner_rating(review.item.user_id)
        
        # Get the saved review with relationships loaded
        saved_review = self.get_by_id(review.id)
        return saved_review

    def delete_review(self, review_id, user_id):
        """Delete a review and update the item's rating."""
        # Get the review with its item relationship loaded
        review = (
            db.session.query(Review)
            .options(db.joinedload(Review.item))
            .filter_by(id=review_id)
            .first()
        )
        
        if not review:
            return None

        if str(review.user_id) != str(user_id):
            raise ValueError("You can only delete your own reviews")

        # Store the item and owner ID before deletion
        item = review.item
        owner_id = item.user_id
        
        # Delete the review and its images
        for img in list(review.images):
            db.session.delete(img)
        db.session.delete(review)
        db.session.commit()
        
        # Get a fresh copy of the item to ensure we have the latest state
        fresh_item = db.session.get(Item, item.id)
        
        # Update the item's rating
        fresh_item.update_rating()
        
        # Update the owner's average rating
        self.update_owner_rating(owner_id)
        
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

        # Check if user has completed a booking for this item
        completed_booking = Booking.query.filter_by(
            user_id=user_id,
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
