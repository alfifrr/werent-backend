"""
Image model for CamRent Backend API.
Handles item images.
"""

from app.extensions import db


class Image(db.Model):
    """Image model for item images."""

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)

    # Foreign key
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    item = db.relationship('Item', back_populates='images')

    def __repr__(self):
        """String representation of Image object."""
        return f'<Image {self.url}>'

    def to_dict(self):
        """Convert image object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'url': self.url,
            'order': self.order,
            'item_id': self.item_id
        }
