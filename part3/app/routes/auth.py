from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint. Expects JSON with 'username' and 'password'.
    Returns a JWT token upon successful authentication.
    """
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # Find user by username (you might also support login via email)
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Optionally, embed additional claims such as is_admin if available
        additional_claims = {}
        if hasattr(user, "is_admin"):
            additional_claims["is_admin"] = user.is_admin

        # Create a JWT token using the user id as the identity
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Example of a protected endpoint.
    Only accessible if a valid JWT is provided in the Authorization header.
    """
    current_user_id = get_jwt_identity()
    # You can fetch user details if needed:
    # user = User.query.get(current_user_id)
    return jsonify(logged_in_as=current_user_id), 200
