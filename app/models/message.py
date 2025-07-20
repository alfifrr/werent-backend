"""
Message model for CamRent Backend API.
Handles messaging between users.
"""

from datetime import datetime
from app.extensions import db


class Message(db.Model):
    """Message model for user communication."""

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.now)
    is_read = db.Column(db.Boolean, default=False)

    # Foreign keys
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')

    def __repr__(self):
        """String representation of Message object."""
        return f'<Message from {self.sender.name} to {self.receiver.name}>'

    def to_dict(self):
        """Convert message object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'content': self.content,
            'sent_at': self.sent_at.isoformat(),
            'is_read': self.is_read,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id
        }
