"""
Item model for WeRent Backend API.
Handles rental items and their details.
"""

import enum
from datetime import datetime
from app.extensions import db


class ItemType(enum.Enum):
    """Enum for outfit item types."""
    DRESS = "Dress"
    TOP = "Top"
    BOTTOM = "Bottom"
    OUTERWEAR = "Outerwear"
    SHOES = "Shoes"
    ACCESSORY = "Accessory"
    JEWELRY = "Jewelry"
    BAG = "Bag"
    FORMAL_WEAR = "Formal Wear"
    COSTUME = "Costume"
    OTHER = "Other"


class Size(enum.Enum):
    """Standard clothing sizes."""
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    XXXL = "XXXL"
    ONE_SIZE = "One Size"


class Gender(enum.Enum):
    """Gender categories for outfits."""
    MENS = "Men's"
    WOMENS = "Women's"
    UNISEX = "Unisex"
    KIDS = "Kids"


class Item(db.Model):
    """Item model for outfit rental management."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(ItemType), nullable=False)
    size = db.Column(db.Enum(Size), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    brand = db.Column(db.String(100))
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product_code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='items')
    images = db.relationship('Image', back_populates='item', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='item')
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        """String representation of Item object."""
        return f'<Item {self.name}>'

    def to_dict(self):
        """Convert item object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value if self.type else None,
            'size': self.size.value if self.size else None,
            'gender': self.gender.value if self.gender else None,
            'brand': self.brand,
            'color': self.color,
            'product_code': self.product_code,
            'description': self.description,
            'price_per_day': self.price_per_day,
            'quantity': self.quantity,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
            'images': [image.url for image in self.images] if self.images else []
        }

    @classmethod
    def find_by_id(cls, item_id):
        """Find item by ID."""
        return cls.query.get(item_id)

    @classmethod
    def find_by_product_code(cls, product_code):
        """Find item by product code."""
        return cls.query.filter_by(product_code=product_code).first()

    @classmethod
    def find_by_type(cls, item_type):
        """Find items by type."""
        return cls.query.filter_by(type=item_type).all()

    @classmethod
    def find_available_items(cls):
        """Find all available items."""
        return cls.query.filter_by(status='available').all()

    def save(self):
        """Save item to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete item from database."""
        db.session.delete(self)
        db.session.commit()

    def update_rating(self):
        """Update item rating based on reviews."""
        if self.reviews:
            total_rating = sum(review.rating for review in self.reviews)
            self.rating = total_rating / len(self.reviews)
        else:
            self.rating = 0.0
        self.save()
