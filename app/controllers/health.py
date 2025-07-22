from app.extensions import db
from datetime import datetime
import os

def health_check_controller():
    try:
        # Test database connectivity
        db.session.execute('SELECT 1')
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

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
    return health_data, status_code

def detailed_health_check_controller():
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
    return detailed_data, status_code
