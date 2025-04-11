from flask_restx import Namespace, Resource, fields
from app.services import facade  # Import the global facade from app/services/__init__.py

api = Namespace('amenities', description='Amenities endpoints')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Unique ID of the amenity'),
    'name': fields.String(required=True, description='Amenity name')
})

@api.route('/')
class AmenitiesList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve all amenities"""
        return facade.get_all_amenities()

    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = api.payload
        new_amenity = facade.create_amenity(data)
        return new_amenity, 201

@api.route('/<string:amenity_id>')
class AmenityDetail(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Retrieve a single amenity by its ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an existing amenity"""
        data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            api.abort(404, "Amenity not found or update failed")
        return updated_amenity
