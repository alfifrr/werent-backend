"""
Message service for business logic operations.
Handles messaging between users and conversation management.
"""

from datetime import datetime
from sqlalchemy import or_
from app.services.base_service import BaseService
from app.models.message import Message


class MessageService(BaseService):
    """Service class for Message model business logic."""

    def __init__(self):
        """Initialize MessageService."""
        super().__init__(Message)

    def send_message(self, sender_id, receiver_id, content):
        """Send a new message between users."""
        if sender_id == receiver_id:
            raise ValueError("Cannot send message to yourself")

        # Verify users exist
        from app.services.user_service import UserService
        user_service = UserService()

        sender = user_service.get_by_id(sender_id)
        receiver = user_service.get_by_id(receiver_id)

        if not sender:
            raise ValueError("Sender not found")
        if not receiver:
            raise ValueError("Receiver not found")

        message = Message()
        message.sender_id = sender_id
        message.receiver_id = receiver_id
        message.content = content.strip()

        return self.save(message)

    def get_conversation(self, user1_id, user2_id, limit=50):
        """Get conversation between two users."""
        return Message.query.filter(
            ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
            ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
        ).order_by(Message.sent_at.desc()).limit(limit).all()

    def get_user_conversations(self, user_id):
        """Get all conversations for a user with latest message."""
        from sqlalchemy import and_, or_, func
        from app.models.user import User

        # Subquery to get the latest message for each conversation
        latest_messages = Message.query.filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        ).order_by(Message.sent_at.desc()).all()

        # Group by conversation partner
        conversations = {}
        for message in latest_messages:
            partner_id = message.receiver_id if message.sender_id == user_id else message.sender_id

            if partner_id not in conversations:
                conversations[partner_id] = {
                    'partner_id': partner_id,
                    'latest_message': message.to_dict(),
                    'unread_count': 0
                }

        # Count unread messages for each conversation
        for partner_id in conversations.keys():
            unread_count = Message.query.filter(
                Message.sender_id == partner_id,
                Message.receiver_id == user_id,
                Message.is_read == False
            ).count()
            conversations[partner_id]['unread_count'] = unread_count

        return list(conversations.values())

    def mark_conversation_as_read(self, user_id, partner_id):
        """Mark all messages from a partner as read."""
        messages = Message.query.filter(
            Message.sender_id == partner_id,
            Message.receiver_id == user_id,
            Message.is_read == False
        ).all()

        for message in messages:
            message.is_read = True

        from app.extensions import db
        db.session.commit()

        return len(messages)

    def mark_message_as_read(self, message_id, user_id):
        """Mark a specific message as read (only if user is the receiver)."""
        message = self.get_by_id(message_id)
        if not message:
            return None

        if message.receiver_id != user_id:
            raise ValueError("You can only mark messages sent to you as read")

        message.is_read = True
        return self.save(message)

    def get_unread_messages(self, receiver_id):
        """Get all unread messages for a user."""
        return Message.query.filter_by(
            receiver_id=receiver_id,
            is_read=False
        ).order_by(Message.sent_at.desc()).all()

    def get_unread_count(self, receiver_id):
        """Get count of unread messages for a user."""
        return Message.query.filter_by(
            receiver_id=receiver_id,
            is_read=False
        ).count()

    def get_sent_messages(self, sender_id, limit=50):
        """Get messages sent by a user."""
        return Message.query.filter_by(sender_id=sender_id).order_by(
            Message.sent_at.desc()
        ).limit(limit).all()

    def get_received_messages(self, receiver_id, limit=50):
        """Get messages received by a user."""
        return Message.query.filter_by(receiver_id=receiver_id).order_by(
            Message.sent_at.desc()
        ).limit(limit).all()

    def delete_message(self, message_id, user_id):
        """Delete a message (only sender can delete)."""
        message = self.get_by_id(message_id)
        if not message:
            return None

        if message.sender_id != user_id:
            raise ValueError("You can only delete messages you sent")

        self.delete(message)
        return True

    def search_messages(self, user_id, query, limit=20):
        """Search messages for a user by content."""
        return Message.query.filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id),
            Message.content.ilike(f'%{query}%')
        ).order_by(Message.sent_at.desc()).limit(limit).all()

    def get_message_statistics(self, user_id):
        """Get message statistics for a user."""
        sent_count = Message.query.filter_by(sender_id=user_id).count()
        received_count = Message.query.filter_by(receiver_id=user_id).count()
        unread_count = self.get_unread_count(user_id)

        return {
            'messages_sent': sent_count,
            'messages_received': received_count,
            'unread_messages': unread_count,
            'total_conversations': len(self.get_user_conversations(user_id))
        }

    def get_recent_messages(self, user_id, hours=24, limit=10):
        """Get recent messages for a user within specified hours."""
        from datetime import timedelta

        cutoff_time = datetime.now() - timedelta(hours=hours)

        return Message.query.filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id),
            Message.sent_at >= cutoff_time
        ).order_by(Message.sent_at.desc()).limit(limit).all()

    def block_user_messages(self, user_id, blocked_user_id):
        """Block messages from a specific user (implementation depends on requirements)."""
        # This would typically involve a separate blocked_users table
        # For now, we'll just return a placeholder
        pass

    def validate_message_content(self, content):
        """Validate message content."""
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")

        if len(content) > 1000:  # Assuming max message length
            raise ValueError("Message content too long (max 1000 characters)")

        return content.strip()
