from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_bp.route('/', methods=['POST'])
def register_user():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    # Create the new user and hash the password using the model's setter
    user = User(username=username, email=email)
    user.password = password  # This triggers the password setter and hashes the password

    # Save the user to the database
    db.session.add(user)
    db.session.commit()

    # Respond with the created user's data, excluding the password_hash
    return jsonify(user.to_dict()), 201
