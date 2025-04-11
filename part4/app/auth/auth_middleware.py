from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt

def admin_required():
    """
    Decorator to verify that the JWT token is present and the user is an admin.
    If the token is missing or invalid, or the user is not an admin, the decorated
    route will return a 403 Forbidden error.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify that the JWT is present and valid
            verify_jwt_in_request()
            
            # Get the claims from the JWT
            claims = get_jwt()
            
            # Check if the user is an admin
            if not claims.get('is_admin', False):
                return {'error': 'Admin access required'}, 403
            
            # If the user is an admin, execute the decorated function
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def jwt_required_with_identity():
    """
    Decorator to verify that the JWT token is present and extract the user_id.
    This decorator simplifies accessing the user_id in routes.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify that the JWT is present and valid
            verify_jwt_in_request()
            
            # Get the user_id from the JWT identity
            user_id = get_jwt_identity()
            
            # Add the user_id to the kwargs
            kwargs['user_id'] = user_id
            
            # Execute the decorated function
            return fn(*args, **kwargs)
        return decorator
    return wrapper 