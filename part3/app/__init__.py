from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config  # or import a specific config like DevelopmentConfig
from app.routes.auth import auth_bp

# Initialize extensions outside of the factory
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()  # Initialize Flask-Bcrypt

def create_app(config_object=Config):
    """Application Factory for creating a Flask app instance."""
    app = Flask(__name__)
    # Load configuration from the provided config object
    app.config.from_object(config_object)
    # auth_bp blueprint
    app.register_blueprint(auth_bp)


    # Initialize the extensions with the app instance
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)  # Set up Bcrypt with the app

    # Example: register blueprints or routes here
    # from app.routes import main
    # app.register_blueprint(main)

    return app
