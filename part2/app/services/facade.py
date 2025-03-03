from app.models.user import User
from app.services.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Creates a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Fetch a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Fetch a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Returns a list of all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, updated_data):
        """Updates a user"""
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in updated_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user
