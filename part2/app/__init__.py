from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app():
    """Initialize Flask app and set up API."""
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    return app
