from .base_model import BaseModel

class Review(BaseModel):
    """Review model linked to a Place"""

    def __init__(self, *args, **kwargs):
        """Initializes a Review instance"""
        super().__init__(*args, **kwargs)
        self.place_id = ""
        self.user_id = ""
        self.text = ""
