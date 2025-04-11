from .base_model import BaseModel
from app import db

class Amenity(BaseModel):
    """Amenity model linked to a Place"""
    
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        """Initializes an Amenity instance"""
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name', "")
