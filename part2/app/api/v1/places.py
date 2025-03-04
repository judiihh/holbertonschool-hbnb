from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

facade = HBnBFacade()  # Initialize the facade

place_model = api.model('Place', {
    'user_id': fields.String(required=True, description='ID of the user who owns the place'),
    'name': fields.String(required=True, description='Name of the place'),
    'description': fields.String(description='Description of the place'),
    'number_rooms': fields.Integer(description='Number of rooms'),
    'number_bathrooms': fields.Integer(description='Number of bathrooms'),
    'max_guest': fields.Integer(description='Maximum guests allowed'),
    'price_by_night': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'amenity_ids': fields.List(fields.String, description='List of associated amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return new_place.__dict__, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [place.__dict__ for place in places], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.__dict__, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place"""
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {'error': 'Place not found'}, 404
        return updated_place.__dict__, 200
