"""
Base service class for common database operations.
All service classes should inherit from this base class.
"""

from app.extensions import db


class BaseService:
    """Base service class with common CRUD operations."""

    def __init__(self, model_class):
        """Initialize service with model class."""
        self.model_class = model_class

    def save(self, instance):
        """Save instance to database."""
        db.session.add(instance)
        db.session.commit()
        return instance

    def delete(self, instance):
        """Delete instance from database."""
        db.session.delete(instance)
        db.session.commit()

    def get_by_id(self, instance_id):
        """Get instance by ID."""
        return self.model_class.query.get(instance_id)

    def get_all(self):
        """Get all instances."""
        return self.model_class.query.all()

    def create(self, **kwargs):
        """Create new instance."""
        instance = self.model_class(**kwargs)
        return self.save(instance)

    def update(self, instance, **kwargs):
        """Update instance with new data."""
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return self.save(instance)

    def delete_by_id(self, instance_id):
        """Delete instance by ID."""
        instance = self.get_by_id(instance_id)
        if instance:
            self.delete(instance)
        return instance
