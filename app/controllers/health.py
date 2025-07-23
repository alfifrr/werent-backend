from app.extensions import db
from datetime import datetime
import os
from sqlalchemy import text


def get_database_info():
    """
    Get database type and appropriate queries based on the current database engine.
    
    This is a best practice for health checks as it:
    - Adapts to different database types automatically
    - Uses appropriate version queries for each database
    - Supports local development (SQLite) and production (PostgreSQL/MySQL)
    - Provides fallback for unknown database types
    
    Returns:
        tuple: (db_type, connectivity_query, version_query)
    """
    db_url_str = str(db.engine.url)
    
    if "postgresql" in db_url_str:
        # PostgreSQL - typically used in production (Heroku, AWS RDS, etc.)
        return "postgresql", "SELECT 1", "SELECT version()"
    elif "mysql" in db_url_str:
        # MySQL/MariaDB - common production database
        return "mysql", "SELECT 1", "SELECT VERSION()"
    elif "sqlite" in db_url_str or "sqlite:///" in db_url_str:
        # SQLite - typically used in local development
        return "sqlite", "SELECT 1", "SELECT sqlite_version()"
    else:
        # Fallback for unknown database types
        return "unknown", "SELECT 1", "SELECT 1"


def health_check_controller():
    try:
        # Test database connectivity with environment-appropriate query
        db_type, connectivity_query, _ = get_database_info()
        db.session.execute(text(connectivity_query))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    environment = os.environ.get('FLASK_ENV', 'unknown')
    db_type, _, _ = get_database_info()
    
    health_data = {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "service": "WeRent Backend API",
        "version": "1.0.0",
        "environment": environment,
        "database": {
            "status": db_status,
            "type": db_type
        },
        "uptime": "Service is running"
    }
    status_code = 200 if db_status == "healthy" else 503
    return health_data, status_code

def detailed_health_check_controller():
    try:
        # Determine database type and use appropriate version query
        db_type, connectivity_query, version_query = get_database_info()
        result = db.session.execute(text(version_query)).fetchone()
        db_version = result[0] if result else "unknown"
        db_status = "healthy"
    except Exception as e:
        db_version = "unavailable"
        db_status = f"unhealthy: {str(e)}"

    db_type, _, _ = get_database_info()
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
            "type": db_type,
            "version": db_version
        },
        "features": {
            "authentication": "JWT",
            "cors": "enabled",
            "migrations": "flask-migrate"
        }
    }
    status_code = 200 if db_status == "healthy" else 503
    return detailed_data, status_code
