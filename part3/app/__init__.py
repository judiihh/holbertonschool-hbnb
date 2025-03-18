from app.routes.places import places_bp
from app.routes.reviews import reviews_bp
from app.routes.users import users_bp
from app.routes.auth import auth_bp  # from JWT auth setup

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(users_bp)

    return app
