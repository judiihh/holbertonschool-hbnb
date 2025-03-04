from .base_model import BaseModel

class Place(BaseModel):
    """Represents a place (listing)."""

    def __init__(self, *args, **kwargs):
        """Initialize a Place instance with given attributes."""
        super().__init__(*args, **kwargs)

        # Convert or parse each argument from kwargs into the correct type
        self.user_id = str(kwargs.get("user_id", ""))
        self.name = str(kwargs.get("name", ""))
        self.description = str(kwargs.get("description", ""))

        self.number_rooms = int(kwargs.get("number_rooms", 0))
        self.number_bathrooms = int(kwargs.get("number_bathrooms", 0))
        self.max_guest = int(kwargs.get("max_guest", 0))
        self.price_by_night = int(kwargs.get("price_by_night", 0))

        # Cast latitude and longitude to float
        self.latitude = float(kwargs.get("latitude", 0.0))
        self.longitude = float(kwargs.get("longitude", 0.0))

        # Ensure amenity_ids is a list
        amenity_ids = kwargs.get("amenity_ids", [])
        if not isinstance(amenity_ids, list):
            amenity_ids = []
        self.amenity_ids = amenity_ids
