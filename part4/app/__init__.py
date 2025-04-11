from flask import Flask, render_template, redirect, url_for
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import sys
import os
import datetime

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    """Initialize Flask app with configuration and set up API."""
    app = Flask(__name__)
    
    # Configure the app
    if isinstance(config_class, str):
        app.config.from_object(config_class)
    else:
        app.config.from_object(config_class)
    
    # Enable CORS globally for all routes
    CORS(app, supports_credentials=True)
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Define authorizations for Swagger UI
    authorizations = {
        'jwt': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Type in the value input: Bearer {token}'
        }
    }

    # Create a Blueprint for the API
    from flask import Blueprint
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    
    api = Api(
        blueprint,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        security='jwt',
        authorizations=authorizations,
        doc='/doc'
    )

    # Register blueprint with the app
    app.register_blueprint(blueprint)

    # Import your namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    # Register each namespace at its path
    api.add_namespace(users_ns, path='/v1/users')
    api.add_namespace(amenities_ns, path='/v1/amenities')
    api.add_namespace(places_ns, path='/v1/places')
    api.add_namespace(reviews_ns, path='/v1/reviews')
    api.add_namespace(auth_ns, path='/v1/auth')
    
    # Redirect /api to frontend
    @app.route('/api')
    def api_redirect():
        return redirect(url_for('index'))
    
    # Add frontend routes
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/place/<place_id>')
    def place_details(place_id):
        return render_template('place.html')
    
    @app.route('/add_review/<place_id>')
    def add_review(place_id):
        return render_template('add_review.html')
    
    @app.route('/test')
    def test():
        return render_template('test.html', now=datetime.datetime.now())

    return app
