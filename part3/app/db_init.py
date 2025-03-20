from app import db, create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import os
from werkzeug.security import generate_password_hash

def init_db():
    """Initialize the database by creating all tables"""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if admin user exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            # Create admin user
            admin = User(
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                password='admin123',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")

        print("Database initialized successfully")

if __name__ == "__main__":
    init_db() 
