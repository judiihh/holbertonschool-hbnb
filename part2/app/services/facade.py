from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.amenity_repo = InMemoryRepository()

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
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an existing Amenity's details"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        self.amenity_repo.update(amenity)
        return amenity
