from flask_restx import Namespace, Resource, fields
from app.facade import HBnBFacade  # Import your combined Facade

api = Namespace('amenities', description='Amenities endpoints')
facade = HBnBFacade()  # Single Facade instance

# Define what the JSON payload looks like and what is returned
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Unique ID of the amenity'),
    'name': fields.String(required=True, description='Amenity name')
})

@api.route('')
class AmenitiesList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """
        Retrieve all amenities
        """
        return facade.get_all_amenities()

    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """
        Create a new amenity
        """
        data = api.payload
        new_amenity = facade.create_amenity(data)
        return new_amenity, 201


@api.route('/<string:amenity_id>')
class AmenityDetail(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """
        Retrieve a single amenity by its ID
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """
        Update an existing amenity
        """
        data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            api.abort(404, "Amenity not found or update failed")
        return updated_amenity
