from models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity model linked to a Place"""

    def __init__(self, *args, **kwargs):
        """Initializes an Amenity instance"""
        super().__init__(*args, **kwargs)
        self.name = ""
