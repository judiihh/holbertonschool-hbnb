import uuid
from datetime import datetime

class BaseModel:
    """Base model with common attributes and methods"""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
                if key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.fromisoformat(value))
        else:
            self.id = str(uuid.uuid4())  # Generates a unique ID
            self.created_at = datetime.utcnow()  # Set creation time
            self.updated_at = datetime.utcnow()  # Set last update time

    def save(self):
        """Updates the updated_at attribute to the current time"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Converts object attributes to a dictionary"""
        obj_dict = self.__dict__.copy()
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["__class__"] = self.__class__.__name__
        return obj_dict
