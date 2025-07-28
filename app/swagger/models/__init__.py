"""
Swagger models package for WeRent Backend API.
Organized model definitions for API documentation.
"""

from .base import create_base_models
from .user import create_user_models
from .auth import create_auth_models
from .admin import create_admin_models
from .image import create_image_models
from .future import create_future_models

def create_swagger_models(api):
    """Create and register all Swagger models with the API instance."""
    
    # Create base models
    base_models = create_base_models(api)
    
    # Create user models
    user_models = create_user_models(api)
    
    # Create auth models (depends on user_model)
    auth_models = create_auth_models(api, user_models['user_model'])
    
    # Create admin models (depends on user_model and base fields)
    admin_models = create_admin_models(
        api, 
        user_models['user_model'], 
        base_models['success_field'], 
        base_models['message_field']
    )
    
    # Create image models (depends on user_model and base fields)
    image_models = create_image_models(
        api, 
        user_models['user_model'], 
        base_models['success_field'], 
        base_models['message_field']
    )
    
    # Create future models
    future_models = create_future_models(api)
    
    # Combine all models into a single dictionary
    all_models = {}
    all_models.update(base_models)
    all_models.update(user_models)
    all_models.update(auth_models)
    all_models.update(admin_models)
    all_models.update(image_models)
    all_models.update(future_models)
    
    return all_models
