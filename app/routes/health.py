"""
Health check route for WeRent Backend API.
Used for monitoring and deployment verification.
"""

from flask import Blueprint, jsonify
from app.extensions import db
from datetime import datetime
import os

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring service status.
    
    Returns:
        JSON response with service status, database connectivity,
        and basic system information.
    """
    try:
        # Test database connectivity
        db.session.execute('SELECT 1')
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Get environment info
    environment = os.environ.get('FLASK_ENV', 'unknown')
    
    health_data = {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "service": "WeRent Backend API",
        "version": "1.0.0",
        "environment": environment,
        "database": {
            "status": db_status,
            "type": "postgresql" if "postgresql" in str(db.engine.url) else "sqlite"
        },
        "uptime": "Service is running"
    }
    
    status_code = 200 if db_status == "healthy" else 503
    
    return jsonify(health_data), status_code


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """
    Detailed health check with more system information.
    """
    try:
        # Test database with more details
        result = db.session.execute('SELECT version()').fetchone()
        db_version = result[0] if result else "unknown"
        db_status = "healthy"
    except Exception as e:
        db_version = "unavailable"
        db_status = f"unhealthy: {str(e)}"
    
    detailed_data = {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "service": {
            "name": "WeRent Backend API",
            "version": "1.0.0",
            "description": "Outfit rental platform backend service"
        },
        "environment": {
            "flask_env": os.environ.get('FLASK_ENV', 'unknown'),
            "python_version": os.environ.get('PYTHON_VERSION', 'unknown'),
            "port": os.environ.get('PORT', 'unknown')
        },
        "database": {
            "status": db_status,
            "type": "postgresql" if "postgresql" in str(db.engine.url) else "sqlite",
            "version": db_version
        },
        "features": {
            "authentication": "JWT",
            "cors": "enabled",
            "migrations": "flask-migrate"
        }
    }
    
    status_code = 200 if db_status == "healthy" else 503
    
    return jsonify(detailed_data), status_code
