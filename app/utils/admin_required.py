from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.utils.responses import forbidden_response

# Example: expects JWT identity to be a dict with 'role' or similar field
# Adjust the logic below to match your actual user model/JWT structure

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from app.models.user import User
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        if user and getattr(user, 'is_admin', False):
            return fn(*args, **kwargs)
        return forbidden_response('Admin access required')
    return wrapper
