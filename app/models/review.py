"""
Review model for WeRent Backend API.
Handles user reviews and ratings for items.
"""

from datetime import datetime
from app.extensions import db


class Review(db.Model):
    """Review model for item reviews and ratings."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review_message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 star rating
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    images = db.relationship('Image', back_populates='review', cascade='all, delete-orphan')
    def __repr__(self):
        """String representation of Review object."""
        return f'<Review {self.id} - {self.rating} stars for Item {self.item_id}>'

    def to_dict(self):
        """Convert review object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'review_message': self.review_message,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'images': [image.to_dict() for image in self.images] if self.images else []
        }

    @classmethod
    def find_by_id(cls, review_id):
        """Find review by ID."""
        return cls.query.get(review_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        """Find all reviews by a user."""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_item_id(cls, item_id):
        """Find all reviews for an item."""
        return cls.query.filter_by(item_id=item_id).all()

    @classmethod
    def find_by_rating(cls, rating):
        """Find reviews by rating."""
        return cls.query.filter_by(rating=rating).all()

    @classmethod
    def get_average_rating_for_item(cls, item_id):
        """Get average rating for an item."""
        result = db.session.query(db.func.avg(cls.rating)).filter_by(item_id=item_id).scalar()
        return round(result, 2) if result else 0.0

    @classmethod
    def get_rating_distribution_for_item(cls, item_id):
        """Get rating distribution for an item."""
        distribution = {}
        for rating in range(1, 6):
            count = cls.query.filter_by(item_id=item_id, rating=rating).count()
            distribution[rating] = count
        return distribution

    def save(self):
        """Save review to database."""
        db.session.add(self)
        db.session.commit()
        # Update item rating after saving review
        if self.item:
            self.item.update_rating()

    def delete(self):
        """Delete review from database."""
        item = self.item  # Store reference before deletion
        db.session.delete(self)
        db.session.commit()
        # Update item rating after deleting review
        if item:
            item.update_rating()
