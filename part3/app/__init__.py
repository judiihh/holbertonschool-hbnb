from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config  # or import a specific config like DevelopmentConfig

# Initialize extensions outside of the factory
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_object=Config):
    """Application Factory for creating a Flask app instance."""
    app = Flask(__name__)
    # Load configuration from the provided config object
    app.config.from_object(config_object)

    # Initialize the extensions with the app instance
    db.init_app(app)
    jwt.init_app(app)

    # Example: register blueprints or routes here
    # from app.routes import main
    # app.register_blueprint(main)

    return app
