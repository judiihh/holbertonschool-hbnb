from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return new_user, 201

    @api.response(200, 'List of users retrieved')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return users, 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user['id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email']
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        updated_user = facade.update_user(user_id, api.payload)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {
            'id': updated_user['id'],
            'first_name': updated_user['first_name'],
            'last_name': updated_user['last_name'],
            'email': updated_user['email']
        }, 200
