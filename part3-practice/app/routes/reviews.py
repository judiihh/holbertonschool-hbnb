from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.review import Review
from app.models.place import Place

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/v1/reviews')

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    """Create a review for a place. Enforce restrictions on ownership and duplicates."""
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    place_id = data.get("place_id")
    rating = data.get("rating")
    comment = data.get("comment", "")

    if not place_id or rating is None:
        return jsonify({"msg": "Missing required fields: place_id and rating"}), 400

    # Verify the place exists
    place = Place.query.get(place_id)
    if not place:
        return jsonify({"msg": "Place not found"}), 404

    # Prevent users from reviewing their own place
    if place.owner_id == current_user_id:
        return jsonify({"msg": "You cannot review your own place"}), 403

    # Prevent duplicate reviews: check if this user already reviewed the place
    existing_review = Review.query.filter_by(user_id=current_user_id, place_id=place_id).first()
    if existing_review:
        return jsonify({"msg": "You have already reviewed this place"}), 403

    new_review = Review(user_id=current_user_id, place_id=place_id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review. Only the review's owner can update it."""
    current_user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user_id:
        return jsonify({"msg": "Not authorized to update this review"}), 403

    data = request.get_json() or {}
    review.rating = data.get("rating", review.rating)
    review.comment = data.get("comment", review.comment)
    db.session.commit()
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review. Only the review's owner can delete it."""
    current_user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user_id:
        return jsonify({"msg": "Not authorized to delete this review"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review deleted"}), 200

# Public endpoint: GET all reviews (no JWT required)
@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200
