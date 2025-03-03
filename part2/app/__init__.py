from flask import Flask
from flask_restx import Api

def create_app():
    """Initialize Flask app and set up API."""
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # API placeholders (endpoints will be added later)

    return app
