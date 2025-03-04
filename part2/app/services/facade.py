from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place  # Import Place model
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        # Separate repositories for Users, Amenities, and Places
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()  # Added for Places

    # ------------- User Management Methods -------------
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
        return list(self.user_repo.get_all())

    def update_user(self, user_id, user_data):
        """Updates an existing User's details"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        self.user_repo.update(user)
        return user

    # ------------- Amenity Management Methods -------------
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

    # ------------- Place Management Methods -------------
        def create_place(self, place_data):
        """Creates a new Place and stores it in the repository"""

        # Validate user_id (owner)
        user = self.get_user(place_data['user_id'])  # Explicitly use get_user
        print(f"DEBUG: Retrieved user {place_data['user_id']}: {user}")  # Debug print

        if 'user_id' not in place_data or not user:
            raise ValueError("Invalid user_id: User does not exist")

        # Validate required numeric attributes
        if 'price_by_night' not in place_data or place_data['price_by_night'] < 0:
            raise ValueError("price_by_night is required and must be positive")

        if 'latitude' in place_data and not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if 'longitude' in place_data and not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        # Create and store place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a Place by its ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all places"""
        return list(self.place_repo.get_all())

    def update_place(self, place_id, place_data):
        """Updates an existing Place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            setattr(place, key, value)

        self.place_repo.update(place)
        return place
