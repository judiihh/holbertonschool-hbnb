from app import db
from app.models.user import User

class UserRepository:
    """Repository for performing CRUD operations on User entities using SQLAlchemy."""

    def add(self, user):
        """Adds a new user and commits the session."""
        db.session.add(user)
        db.session.commit()
        return user

    def get(self, user_id):
        """Retrieves a user by their ID."""
        return User.query.get(user_id)

    def get_by_email(self, email):
        """Retrieves a user by their email address."""
        return User.query.filter_by(email=email).first()

    def update(self):
        """Commits any pending changes."""
        db.session.commit()

    def delete(self, user):
        """Deletes a user and commits the session."""
        db.session.delete(user)
        db.session.commit()

    def list(self):
        """Lists all users."""
        return User.query.all()
