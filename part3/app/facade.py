from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User

class UserFacade:
    """Facade for user operations using a repository for persistence."""

    def __init__(self, repository=None):
        # Allow dependency injection of a repository; default to SQLAlchemyRepository.
        self.repository = repository or SQLAlchemyRepository()

    def create_user(self, username, email, password):
        # Create a new user instance.
        user = User(username=username, email=email)
        user.password = password  # Triggers the password setter to hash the password.
        # Persist the user using the repository.
        return self.repository.add(user)

    def get_user(self, user_id):
        # Retrieve a user by ID.
        return self.repository.get(User, user_id)

    def update_user(self, user):
        # Assuming modifications are already made on the user instance.
        self.repository.update()
        return user

    def delete_user(self, user):
        # Delete the user from the database.
        self.repository.delete(user)
        return {"msg": "User deleted"}
