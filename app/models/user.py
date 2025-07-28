"""
User model for WeRent Backend API.
Handles user authentication and profile management.
"""

import uuid as uuid_lib
from datetime import datetime
from app.extensions import db, bcrypt


class User(db.Model):
    """User model for authentication and profile management."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid_lib.uuid4()),
    )
    profile_image = db.Column(db.Text, nullable=True)  # Base64 encoded image
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Relationships
    items = db.relationship("Item", foreign_keys="Item.user_id", back_populates="user")
    bookings = db.relationship(
        "Booking",
        foreign_keys="Booking.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    payments = db.relationship(
        "Payment",
        foreign_keys="Payment.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    tickets = db.relationship(
        "Ticketing",
        foreign_keys="Ticketing.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    reviews = db.relationship(
    "Review", foreign_keys="Review.user_id", back_populates="user"
)

    def __repr__(self):
        """String representation of User object."""
        return f"<User {self.email}>"

    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """Check if provided password matches user's password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"

    def to_dict(self, include_sensitive=False):
        """Convert user object to dictionary for JSON serialization."""
        data = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "profile_image": self.profile_image,
            "is_admin": self.is_admin,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "uuid": self.uuid,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_sensitive:
            data["password_hash"] = self.password_hash

        return data

    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID."""
        return db.session.get(cls, user_id)

    @classmethod
    def find_by_email(cls, email):
        """Find user by email."""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        """Find user by UUID."""
        return cls.query.filter_by(uuid=uuid).first()

    def save(self):
        """Save user to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete user from database."""
        db.session.delete(self)
        db.session.commit()
