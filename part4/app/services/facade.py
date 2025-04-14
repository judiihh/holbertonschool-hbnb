from app.persistence.repository import SQLAlchemyRepository
import re
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app import db

class HBnBFacade:
    """Facade service that encapsulates all business logic for HBnB application."""

    def __init__(self):
        """Initialize the facade with necessary repositories."""
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # ------------- User Management Methods -------------
    def create_user(self, user_data):
        """Creates a new User and stores it in the repository with validation"""
        # Validate user data
        self.validate_user(user_data)
        # Check for duplicate email before storing the user.
        existing_user = self.get_user_by_email(user_data["email"])
        if existing_user:
            raise ValueError(f"User with email {user_data['email']} already exists.")
        user = User(**user_data)
        self.user_repo.add(user)
        print(f"DEBUG: Stored user {user.id}: {user.to_dict()}")
        return user.to_dict()

    def get_user(self, user_id):
        """Retrieves a User by its ID"""
        print(f"DEBUG: Looking for user with ID: {user_id}")
        user = self.user_repo.get(user_id)
        print(f"DEBUG: Found user: {user}")
        if user:
            return user.to_dict()
        return None

    def get_all_users(self):
        """Retrieves all users"""
        return [user.to_dict() for user in self.user_repo.get_all()]

    @staticmethod
    def validate_user(user_data):
        # Validate first name
        first_name = user_data.get("first_name", "").strip()
        if not first_name:
            raise ValueError("First name cannot be empty")
        # Validate last name
        last_name = user_data.get("last_name", "").strip()
        if not last_name:
            raise ValueError("Last name cannot be empty")
        # Validate email
        email = user_data.get("email", "").strip()
        if not email:
            raise ValueError("Email cannot be empty")
        # Basic email format check
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

    def get_user_by_email(self, email):
        """Retrieve a user by email from the repository."""
        if not email:
            return None
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Updates an existing user with the provided data.
        Returns the updated user dictionary if successful; otherwise, None.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, user_data)
        updated_user = self.user_repo.get(user_id)
        return updated_user.to_dict()

    # ------------- Amenity Management Methods -------------
    def create_amenity(self, amenity_data):
        """
        Creates a new Amenity and stores it in the repository.
        """
        self.validate_amenity(amenity_data)
        print(f"DEBUG: Creating amenity with data: {amenity_data}")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        print(f"DEBUG: Created amenity: {amenity.to_dict()}")
        return amenity.to_dict()

    @staticmethod
    def validate_amenity(amenity_data):
        name = amenity_data.get("name", "").strip()
        if not name:
            raise ValueError("Amenity name cannot be empty")

    def get_amenity(self, amenity_id):
        print(f"DEBUG: Looking for amenity with ID: {amenity_id}")
        amenity = self.amenity_repo.get(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, amenity_data):
        print(f"DEBUG: Updating amenity with ID: {amenity_id} using data: {amenity_data}")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        updated_amenity = self.amenity_repo.get(amenity_id)
        print(f"DEBUG: Updated amenity: {updated_amenity.to_dict()}")
        return updated_amenity.to_dict()

    # ------------- Place Management Methods -------------
    def create_place(self, place_data):
        print(f"DEBUG: Received place data: {place_data}")
        
        # Convert user_id to owner_id if user_id is provided (for backward compatibility)
        if 'user_id' in place_data and 'owner_id' not in place_data:
            place_data['owner_id'] = place_data.pop('user_id')
            
        # Convert name to title if name is provided (for backward compatibility)
        if 'name' in place_data and 'title' not in place_data:
            place_data['title'] = place_data.pop('name')
            
        user = self.get_user(place_data['owner_id'])
        print(f"DEBUG: Retrieved user {place_data['owner_id']}: {user}")
        if not user:
            raise ValueError("Invalid owner_id: User does not exist")
        if 'price_by_night' not in place_data or place_data['price_by_night'] < 0:
            raise ValueError("price_by_night is required and must be positive")
        if 'latitude' in place_data:
            if not (-90 <= place_data['latitude'] <= 90):
                raise ValueError("Latitude must be between -90 and 90")
        if 'longitude' in place_data:
            if not (-180 <= place_data['longitude'] <= 180):
                raise ValueError("Longitude must be between -180 and 180")
        place = Place(**place_data)
        self.place_repo.add(place)
        print(f"DEBUG: Created place: {place.to_dict()}")
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        print(f"DEBUG: Updating place with ID: {place_id} using data: {place_data}")
        
        # Make a copy of place_data to avoid modifying the original
        place_data_copy = place_data.copy()
        
        # Convert user_id to owner_id if user_id is provided (for backward compatibility)
        if 'user_id' in place_data_copy and 'owner_id' not in place_data_copy:
            place_data_copy['owner_id'] = place_data_copy.pop('user_id')
            
        # Convert name to title if name is provided (for backward compatibility)
        if 'name' in place_data_copy and 'title' not in place_data_copy:
            place_data_copy['title'] = place_data_copy.pop('name')
            
        place = self.place_repo.get(place_id)
        if not place:
            return None
            
        if 'price_by_night' in place_data_copy and place_data_copy['price_by_night'] < 0:
            raise ValueError("price_by_night must be positive")
        if 'latitude' in place_data_copy and not (-90 <= place_data_copy['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if 'longitude' in place_data_copy and not (-180 <= place_data_copy['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180")
            
        # Handle amenity_ids if they exist in the data
        if 'amenity_ids' in place_data_copy:
            amenity_ids = place_data_copy.pop('amenity_ids')
            print(f"DEBUG: Updating amenities for place {place_id} with amenity_ids: {amenity_ids}")
            
            # First remove all existing place-amenity relationships
            # Use delete to remove all entries from the junction table
            from app.models.place import place_amenity
            db.session.execute(place_amenity.delete().where(place_amenity.c.place_id == place_id))
            
            # Add new amenities
            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
            
            # Commit the changes to amenities
            db.session.commit()
            
        # Update other place attributes
        self.place_repo.update(place_id, place_data_copy)
        
        updated_place = self.place_repo.get(place_id)
        print(f"DEBUG: Updated place: {updated_place.to_dict()}")
        return updated_place.to_dict()

    # ------------- Review Management Methods -------------
    def create_review(self, review_data):
        user = self.get_user(review_data.get("user_id"))
        print(f"DEBUG: Looking for user with ID: {review_data.get('user_id')} -> Found: {user}")
        if not user:
            raise ValueError("Invalid user_id: User does not exist")
        place = self.get_place(review_data.get("place_id"))
        print(f"DEBUG: Looking for place with ID: {review_data.get('place_id')} -> Found: {place}")
        if not place:
            raise ValueError("Invalid place_id: Place does not exist")
        if "text" not in review_data or not review_data["text"].strip():
            raise ValueError("Review text is required")
        if "rating" not in review_data:
            review_data["rating"] = 0  # Default rating if not provided (for backward compatibility)
        else:
            # Ensure rating is an integer and in a valid range (e.g., 0-5)
            try:
                rating = int(review_data["rating"])
                if not (0 <= rating <= 5):
                    raise ValueError("Rating must be between 0 and 5")
                review_data["rating"] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be a number between 0 and 5")
                
        review = Review(**review_data)
        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        return review.to_dict() if review else None

    def get_all_reviews(self):
        return [review.to_dict() for review in self.review_repo.get_all()]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        updated_review = self.review_repo.get(review_id)
        return updated_review.to_dict()

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False

    def get_reviews_by_place(self, place_id):
        # This needs to be refactored for SQLAlchemy
        place = self.place_repo.get(place_id)
        if not place:
            return []
        reviews = place.reviews
        return [review.to_dict() for review in reviews]
