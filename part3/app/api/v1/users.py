from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.auth import admin_required, jwt_required_with_identity

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# For updates, we allow partial data.
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return new_user, 201

    @api.response(200, 'List of users retrieved')
    @api.doc(security='jwt')
    @admin_required()
    def get(self):
        """Get all users - Admin access required"""
        users = facade.get_all_users()
        return users, 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.doc(security='jwt')
    @jwt_required()
    def get(self, user_id):
        """Get a specific user - JWT authentication required"""
        # Get the user ID from JWT identity
        current_user_id = get_jwt_identity()
        # Get the admin status from JWT claims
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Only allow admins or the user themselves to access their details
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized access'}, 403
            
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user, 200

    @api.expect(user_update_model)  # Use update model here (not validate=True so partial updates are allowed)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.doc(security='jwt')
    @jwt_required()
    def put(self, user_id):
        """Update a specific user - JWT authentication required"""
        # Get the user ID from JWT identity
        current_user_id = get_jwt_identity()
        # Get the admin status from JWT claims
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Only allow admins or the user themselves to update their details
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized access'}, 403
            
        updated_user = facade.update_user(user_id, api.payload)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return updated_user, 200
