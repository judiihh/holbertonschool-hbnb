from .base_model import BaseModel

class Review(BaseModel):
    """Represents a review of a place."""

    def __init__(self, *args, **kwargs):
        """Initialize a Review instance with given attributes."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id", "")
        self.place_id = kwargs.get("place_id", "")
        self.text = kwargs.get("text", "")
