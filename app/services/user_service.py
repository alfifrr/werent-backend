"""
User service for business logic operations.
Handles user authentication, profile management, and user-related operations.
"""

from datetime import datetime
from app.services.base_service import BaseService
from app.models.user import User
from app.extensions import bcrypt


class UserService(BaseService):
    """Service class for User model business logic."""

    def __init__(self):
        """Initialize UserService."""
        super().__init__(User)

    def create_user(self, email, password, first_name, last_name, phone=None):
        """Create a new user with hashed password."""
        user = User()
        user.email = email.lower().strip()
        user.first_name = first_name.strip()
        user.last_name = last_name.strip()
        user.phone_number = phone.strip() if phone else None
        user.set_password(password)
        return self.save(user)

    def authenticate_user(self, email, password):
        """Authenticate user by email and password."""
        user = self.find_by_email(email)
        if user and user.check_password(password):
            return user
        return None

    def find_by_email(self, email):
        """Find user by email address."""
        return User.query.filter_by(email=email.lower().strip()).first()

    def verify_user(self, user_id):
        """Verify user account."""
        user = self.get_by_id(user_id)
        if user:
            user.is_verified = True
            return self.save(user)
        return None

    def unverify_user(self, user_id):
        """Unverify user account."""
        user = self.get_by_id(user_id)
        if user:
            user.is_verified = False
            return self.save(user)
        return None

    def update_password(self, user_id, new_password):
        """Update user password."""
        user = self.get_by_id(user_id)
        if user:
            user.set_password(new_password)
            return self.save(user)
        return None

    def update_profile(self, user_id, **kwargs):
        """Update user profile information."""
        user = self.get_by_id(user_id)
        if user:
            # Only allow certain fields to be updated
            allowed_fields = ['first_name', 'last_name', 'phone']
            update_data = {}
            for k, v in kwargs.items():
                if k in allowed_fields:
                    # Map phone to phone_number for the model
                    if k == 'phone':
                        update_data['phone_number'] = v
                    else:
                        update_data[k] = v
            return self.update(user, **update_data)
        return None

    def calculate_user_rating(self, user_id):
        """Calculate and update user's average rating based on their items' reviews."""
        from app.models.review import Review
        from app.models.item import Item

        user = self.get_by_id(user_id)
        if not user:
            return None

        # Get all reviews for items owned by this user
        user_items_reviews = Review.query.join(Item).filter(Item.owner_id == user_id).all()

        if user_items_reviews:
            avg_rating = sum(review.rating for review in user_items_reviews) / len(user_items_reviews)
            user.avg_rating = round(avg_rating, 2)
        else:
            user.avg_rating = 0.0

        return self.save(user)

    def get_user_stats(self, user_id):
        """Get user statistics including items, bookings, and reviews."""
        user = self.get_by_id(user_id)
        if not user:
            return None

        return {
            'total_items': len(user.owned_items),
            'total_bookings_made': len(user.rented_items),
            'total_reviews_written': len(user.written_reviews),
            'avg_rating': user.avg_rating,
            'is_verified': user.is_verified,
            'member_since': user.created_at.isoformat()
        }

    def get_verified_users(self):
        """Get all verified users."""
        return User.query.filter_by(is_verified=True).all()

    def search_users(self, query):
        """Search users by name or email."""
        return User.query.filter(
            (User.first_name.ilike(f'%{query}%')) |
            (User.last_name.ilike(f'%{query}%')) |
            (User.email.ilike(f'%{query}%'))
        ).all()

    def check_email_exists(self, email):
        """Check if email already exists in database."""
        return self.find_by_email(email) is not None

    def get_user_activity_summary(self, user_id):
        """Get summary of user's recent activity."""
        user = self.get_by_id(user_id)
        if not user:
            return None

        # Get recent items
        recent_items = sorted(user.owned_items, key=lambda x: x.created_at, reverse=True)[:5]

        # Get recent bookings
        recent_bookings = sorted(user.rented_items, key=lambda x: x.created_at, reverse=True)[:5]

        # Get recent reviews
        recent_reviews = sorted(user.written_reviews, key=lambda x: x.created_at, reverse=True)[:5]

        return {
            'recent_items': [item.to_dict() for item in recent_items],
            'recent_bookings': [booking.to_dict() for booking in recent_bookings],
            'recent_reviews': [review.to_dict() for review in recent_reviews]
        }
