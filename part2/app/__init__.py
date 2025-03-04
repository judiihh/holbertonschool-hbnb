from flask import Flask
from flask_restx import Api

# Import your namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# Import your Facade
from app.facade import HBnBFacade

# Create a single facade instance at the top level so it’s available app-wide
facade = HBnBFacade()

def create_app():
    """Initialize Flask app and set up API."""
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )

    # Register each namespace at its path
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
