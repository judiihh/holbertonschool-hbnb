from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Model for creating a review (all fields required)
review_model = api.model('Review', {
    'user_id': fields.String(required=True, description='ID of the user writing the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating value (e.g., 1-5)'),
})

# Model for updating a review (all fields optional)
review_update_model = api.model('ReviewUpdate', {
    'user_id': fields.String(description='ID of the user writing the review'),
    'place_id': fields.String(description='ID of the place being reviewed'),
    'text': fields.String(description='Review text'),
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        review_data = api.payload
        updated_review = facade.update_review(review_id, review_data)
        if not updated_review:
            return {'error': 'Review not found'}, 404
        return updated_review, 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Review not found'}, 404

@api.route('/place/<string:place_id>')
class PlaceReviews(Resource):
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        return reviews, 200
