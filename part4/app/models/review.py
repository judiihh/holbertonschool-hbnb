from .base_model import BaseModel
from app import db

class Review(BaseModel):
    """Represents a review of a place."""
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('place.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a Review instance with given attributes."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id", "")
        self.place_id = kwargs.get("place_id", "")
        self.text = kwargs.get("text", "")
        self.rating = int(kwargs.get("rating", 0))
