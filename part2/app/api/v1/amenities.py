from flask_restx import Namespace, Resource, fields
# from facade.amenities_facade import AmenitiesFacade  # example import

api_amenities = Namespace('amenities', description='Amenities endpoints')

# Define what the JSON payload looks like and what is returned
amenity_model = api_amenities.model('Amenity', {
    'id': fields.String(readonly=True, description='Unique ID of the amenity'),
    'name': fields.String(required=True, description='Amenity name')
})

@api_amenities.route('')
class AmenitiesList(Resource):
    @api_amenities.doc('list_amenities')
    @api_amenities.marshal_list_with(amenity_model)
    def get(self):
        """
        Retrieve all amenities
        """
        return AmenitiesFacade.get_all_amenities()

    @api_amenities.doc('create_amenity')
    @api_amenities.expect(amenity_model)
    @api_amenities.marshal_with(amenity_model, code=201)
    def post(self):
        """
        Create a new amenity
        """
        data = api_amenities.payload
        new_amenity = AmenitiesFacade.create_amenity(data)
        return new_amenity, 201


@api_amenities.route('/<string:amenity_id>')
class AmenityDetail(Resource):
    @api_amenities.doc('get_amenity')
    @api_amenities.marshal_with(amenity_model)
    def get(self, amenity_id):
        """
        Retrieve a single amenity by its ID
        """
        amenity = AmenitiesFacade.get_amenity(amenity_id)
        if not amenity:
            api_amenities.abort(404, "Amenity not found")
        return amenity

    @api_amenities.doc('update_amenity')
    @api_amenities.expect(amenity_model)
    @api_amenities.marshal_with(amenity_model)
    def put(self, amenity_id):
        """
        Update an existing amenity
        """
        data = api_amenities.payload
        updated_amenity = AmenitiesFacade.update_amenity(amenity_id, data)
        if not updated_amenity:
            api_amenities.abort(404, "Amenity not found or update failed")
        return updated_amenity

