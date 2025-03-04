from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        """Initialize repositories for Users, Amenities, Places, and Reviews"""
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ------------- User Management Methods -------------
    def create_user(self, user_data):
        """Creates a new User and stores it in the repository"""
        user = User(**user_data)
        self.user_repo.add(user)
        print(f"DEBUG: Stored user {user.id}: {user.to_dict()}")  # Debugging
        return user.to_dict()

    def get_user(self, user_id):
        """Retrieves a User by its ID"""
        print(f"DEBUG: Looking for user with ID: {user_id}")  # Debugging
        user = self.user_repo.get(user_id)
        print(f"DEBUG: Found user: {user}")  # Debugging
        return user

    def get_all_users(self):
        """Retrieves all users"""
        return [user.to_dict() for user in self.user_repo.get_all()]

    # ------------- Place Management Methods -------------
    def create_place(self, place_data):
        """Creates a new Place and stores it in the repository"""
        print(f"DEBUG: Received place data: {place_data}")  # Debugging

        # Validate user_id
        user = self.get_user(place_data['user_id'])
        print(f"DEBUG: Retrieved user {place_data['user_id']}: {user}")  # Debugging

        if not user:
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
        print(f"DEBUG: Created place: {place.to_dict()}")  # Debugging

        return place.to_dict()

    def get_place(self, place_id):
        """Retrieves a Place by its ID"""
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        """Retrieves all places"""
        return [place.to_dict() for place in self.place_repo.get_all()]

    # ------------- Review Management Methods -------------
    def create_review(self, review_data):
        """Creates a new Review and stores it in the repository"""

        # Validate user_id
        user = self.get_user(review_data.get("user_id"))
        print(f"DEBUG: Looking for user with ID: {review_data.get('user_id')} -> Found: {user}")  # Debugging
        if not user:
            raise ValueError("Invalid user_id: User does not exist")

        # Validate place_id
        place = self.get_place(review_data.get("place_id"))
        print(f"DEBUG: Looking for place with ID: {review_data.get('place_id')} -> Found: {place}")  # Debugging
        if not place:
            raise ValueError("Invalid place_id: Place does not exist")

        # Validate text field
        if "text" not in review_data or not review_data["text"].strip():
            raise ValueError("Review text is required")

        # Create and store the review
        review = Review(**review_data)
        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        """Retrieves a Review by its ID"""
        review = self.review_repo.get(review_id)
        return review.to_dict() if review else None

    def get_all_reviews(self):
        """Retrieves all reviews"""
        return [review.to_dict() for review in self.review_repo.get_all()]

    def update_review(self, review_id, review_data):
        """Updates an existing Review"""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            setattr(review, key, value)

        self.review_repo.update(review)
        return review.to_dict()

    def delete_review(self, review_id):
        """Deletes a Review"""
        review = self.review_repo.get(review_id)
        if review:
            del self.review_repo.storage[review_id]
            return True
        return False

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews for a specific place"""
        return [review.to_dict() for review in self.review_repo.get_all() if review.place_id == place_id]
