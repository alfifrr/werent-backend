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
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
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
        user_dict = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }
        
        if include_sensitive:
            user_dict['is_admin'] = self.is_admin
            
        return user_dict
    
    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email address."""
        return cls.query.filter_by(email=email.lower().strip()).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID."""
        return cls.query.get(user_id)
    
    def save(self):
        """Save user to database."""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete user from database."""
        db.session.delete(self)
        db.session.commit()
    
    def deactivate(self):
        """Deactivate user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def activate(self):
        """Activate user account."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
