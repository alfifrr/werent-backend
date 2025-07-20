"""
Category model for CamRent Backend API.
Handles item categories (optional - can be used for better organization).
"""

from app.extensions import db


class Category(db.Model):
    """Category model for item categorization."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        """String representation of Category object."""
        return f'<Category {self.name}>'

    def to_dict(self):
        """Convert category object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active
        }
