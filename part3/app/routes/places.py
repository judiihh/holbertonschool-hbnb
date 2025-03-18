from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.place import Place

places_bp = Blueprint('places', __name__, url_prefix='/api/v1/places')

@places_bp.route('/', methods=['POST'])
@jwt_required()
def create_place():
    """Create a new place. Only authenticated users can create a place."""
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"msg": "Missing required fields: name and description"}), 400

    new_place = Place(name=name, description=description, owner_id=current_user_id)
    db.session.add(new_place)
    db.session.commit()
    return jsonify(new_place.to_dict()), 201

@places_bp.route('/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Update a place. Only the owner can update their place."""
    current_user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)

    if place.owner_id != current_user_id:
        return jsonify({"msg": "Not authorized to update this place"}), 403

    data = request.get_json() or {}
    place.name = data.get("name", place.name)
    place.description = data.get("description", place.description)
    db.session.commit()
    return jsonify(place.to_dict()), 200

@places_bp.route('/<int:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    """Delete a place. Only the owner can delete their place."""
    current_user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)

    if place.owner_id != current_user_id:
        return jsonify({"msg": "Not authorized to delete this place"}), 403

    db.session.delete(place)
    db.session.commit()
    return jsonify({"msg": "Place deleted"}), 200

# Public endpoint: GET all places (no JWT required)
@places_bp.route('/', methods=['GET'])
def get_places():
    places = Place.query.all()
    return jsonify([place.to_dict() for place in places]), 200
