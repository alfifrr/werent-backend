"""
Flask application extensions initialization.
This module initializes all Flask extensions used in the application.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()
mail = Mail()


def init_extensions(app):
    """Initialize Flask extensions with the app instance."""
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=['http://localhost:3000', 'http://localhost:5000'])
    mail.init_app(app)
