from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_bp.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    """
    Update user details.
    Only the authenticated user can update their own details.
    Fields such as email and password are not allowed to be updated here.
    """
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "Not authorized to update this user"}), 403

    data = request.get_json() or {}
    user = User.query.get_or_404(user_id)

    # Only update allowed fields (e.g., username, first_name, last_name)
    if "username" in data:
        user.username = data["username"]
    # Add other allowed fields as needed, for example:
    # if "first_name" in data:
    #     user.first_name = data["first_name"]

    db.session.commit()
    return jsonify(user.to_dict()), 200
