"""
Review model for CamRent Backend API.
Handles reviews and ratings for items.
"""

from datetime import datetime
from app.extensions import db


class Review(db.Model):
    """Review model for item ratings and comments."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 rating
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Foreign keys
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    item = db.relationship('Item', back_populates='reviews')
    user = db.relationship('User', back_populates='written_reviews')

    def __repr__(self):
        """String representation of Review object."""
        return f'<Review {self.rating}/5 for {self.item.title} by {self.user.name}>'

    def to_dict(self):
        """Convert review object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'item_id': self.item_id,
            'user_id': self.user_id
        }
