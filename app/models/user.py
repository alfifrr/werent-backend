"""
User model for CamRent Backend API.
Handles user authentication and profile management.
"""

from datetime import datetime
from app.extensions import db, bcrypt


class User(db.Model):
    """User model for authentication and profile management."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Changed from first_name/last_name to name
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_verified = db.Column(db.Boolean, default=False)
    avg_rating = db.Column(db.Float, default=0.0)
    profile_image_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # Relationships
    owned_items = db.relationship('Item', foreign_keys='Item.owner_id', back_populates='owner')
    rented_items = db.relationship('Booking', foreign_keys='Booking.renter_id', back_populates='renter')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')
    written_reviews = db.relationship('Review', back_populates='user')

    def __repr__(self):
        """String representation of User object."""
        return f'<User {self.email}>'

    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches user's password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self, include_sensitive=False):
        """Convert user object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'is_verified': self.is_verified,
            'avg_rating': self.avg_rating
        }



