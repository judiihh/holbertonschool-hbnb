from app.models.amenity import Amenity
from app.models.user import User  # Import User model
from app.persistence.repository import InMemoryRepository  # Correct import

class HBnBFacade:
    def __init__(self):
        # Separate repositories for Users and Amenities
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User Management Methods
    def create_user(self, user_data):
        """Creates a new User and stores it in the repository"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieves a User by its ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieves a user by their email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieves all users"""
        return list(self.user_repo.get_all())  # Convert to list for JSON response

    def update_user(self, user_id, user_data):
        """Updates an existing User's details"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        self.user_repo.update(user)
        return user

    # Amenity Management Methods (Already Correct)
    def create_amenity(self, amenity_data):
        """Creates a new Amenity and stores it in the repository"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an Amenity by its ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all amenities"""
        return list(self.amenity_repo.get_all())

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an existing Amenity's details"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        self.amenity_repo.update(amenity)
        return amenity
