from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models.user import User
from app.models.amenity import Amenity
from app.utils import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

# Endpoint to create new users
@admin_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    is_admin = data.get("is_admin", False)  # Admin status for the new user

    if not all([username, email, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    # Check for uniqueness of email and username
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({"msg": "User with given email or username already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.password = password  # This will hash the password using the model's setter
    # Set the admin flag; ensure your User model has an 'is_admin' attribute
    new_user.is_admin = is_admin

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Endpoint to update any user's details (including email and password)
@admin_bp.route('/users/<int:user_id>', methods=['PATCH'])
@admin_required
def update_user(user_id):
    data = request.get_json() or {}
    user = User.query.get_or_404(user_id)

    # Admin can update username, email, and password.
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]  # Password setter will hash the password

    # Update the admin flag if provided
    if "is_admin" in data:
        user.is_admin = data["is_admin"]

    db.session.commit()
    return jsonify(user.to_dict()), 200

# Endpoint to add a new amenity
@admin_bp.route('/amenities', methods=['POST'])
@admin_required
def create_amenity():
    data = request.get_json() or {}
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"msg": "Amenity name is required"}), 400

    new_amenity = Amenity(name=name, description=description)
    db.session.add(new_amenity)
    db.session.commit()
    return jsonify(new_amenity.to_dict()), 201

# Endpoint to update an existing amenity
@admin_bp.route('/amenities/<int:amenity_id>', methods=['PUT'])
@admin_required
def update_amenity(amenity_id):
    data = request.get_json() or {}
    amenity = Amenity.query.get_or_404(amenity_id)

    if "name" in data:
        amenity.name = data["name"]
    if "description" in data:
        amenity.description = data["description"]

    db.session.commit()
    return jsonify(amenity.to_dict()), 200

# (Optional) Admin endpoint to update any place bypassing ownership restrictions
# from app.models.place import Place
# @admin_bp.route('/places/<int:place_id>', methods=['PATCH'])
# @admin_required
# def admin_update_place(place_id):
#     data = request.get_json() or {}
#     place = Place.query.get_or_404(place_id)
#
#     if "name" in data:
#         place.name = data["name"]
#     if "description" in data:
#         place.description = data["description"]
#
#     db.session.commit()
#     return jsonify(place.to_dict()), 200
