"""
Ticketing model for WeRent Backend API.
Handles support tickets and customer service.
"""

from datetime import datetime
from app.extensions import db


class Ticketing(db.Model):
    """Ticketing model for support tickets."""

    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    chat_content = db.Column(db.Text, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)  # Optional - ticket might not be booking-related

    # Relationships
    user = db.relationship('User', back_populates='tickets')
    booking = db.relationship('Booking', back_populates='tickets')

    def __repr__(self):
        """String representation of Ticketing object."""
        status = "Resolved" if self.is_resolved else "Open"
        return f'<Ticket {self.id} - {status} - User {self.user_id}>'

    def to_dict(self):
        """Convert ticket object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'booking_id': self.booking_id,
            'chat_content': self.chat_content,
            'is_resolved': self.is_resolved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def resolve(self):
        """Mark ticket as resolved."""
        self.is_resolved = True
        self.updated_at = datetime.now()
        self.save()

    def reopen(self):
        """Reopen a resolved ticket."""
        self.is_resolved = False
        self.updated_at = datetime.now()
        self.save()

    def add_message(self, message):
        """Add a message to the ticket."""
        current_content = self.chat_content or ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = f"\n[{timestamp}] {message}"
        self.chat_content = current_content + new_message
        self.updated_at = datetime.now()
        self.save()

    @classmethod
    def find_by_id(cls, ticket_id):
        """Find ticket by ID."""
        return db.session.get(cls, ticket_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        """Find all tickets for a user."""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_booking_id(cls, booking_id):
        """Find tickets related to a specific booking."""
        return cls.query.filter_by(booking_id=booking_id).all()

    @classmethod
    def find_open_tickets(cls):
        """Find all open (unresolved) tickets."""
        return cls.query.filter_by(is_resolved=False).all()

    @classmethod
    def find_resolved_tickets(cls):
        """Find all resolved tickets."""
        return cls.query.filter_by(is_resolved=True).all()

    def save(self):
        """Save ticket to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete ticket from database."""
        db.session.delete(self)
        db.session.commit()
