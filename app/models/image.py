"""
Image model for WeRent Backend API.
Handles images associated with items.
"""

from datetime import datetime
from app.extensions import db


class Image(db.Model):
    """Image model for item images."""

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_base64 = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # Foreign keys
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=True)

    # Relationships
    item = db.relationship('Item', back_populates='images')
    review = db.relationship('Review', back_populates='images')

    def __repr__(self):
        """String representation of Image object."""
        return f'<Image {self.id} for Item {self.item_id}>'

    def to_dict(self):
        """Convert image object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'image_base64': self.image_base64,
            'item_id': self.item_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def find_by_id(cls, image_id):
        """Find image by ID."""
        return db.session.get(cls, image_id)

    @classmethod
    def find_by_item_id(cls, item_id):
        """Find all images for an item."""
        return cls.query.filter_by(item_id=item_id).all()

    def save(self):
        """Save image to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete image from database."""
        db.session.delete(self)
        db.session.commit()
