from app.repositories.user_repository import UserRepository
from app.models.user import User

class UserFacade:
    """Facade for handling user operations using the UserRepository."""

    def __init__(self, repository=None):
        # Dependency injection allows you to swap the repository if needed.
        self.repository = repository or UserRepository()

    def create_user(self, username, email, password, first_name=None, last_name=None, is_admin=False):
        """Creates a new user and returns the created user object."""
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )
        user.password = password  # Automatically hashes the password
        return self.repository.add(user)

    def get_user(self, user_id):
        """Retrieves a user by ID."""
        return self.repository.get(user_id)

    def update_user(self, user):
        """Updates the user record after modifications."""
        self.repository.update()
        return user

    def delete_user(self, user):
        """Deletes a user from the database."""
        self.repository.delete(user)
        return {"msg": "User deleted"}
