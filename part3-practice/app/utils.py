from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Ensure a JWT is present in the request
        verify_jwt_in_request()
        # Retrieve JWT claims
        claims = get_jwt()
        # Check if the "is_admin" claim is set to True
        if not claims.get("is_admin", False):
            return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper
