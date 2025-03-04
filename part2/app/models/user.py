from .base_model import BaseModel

class User(BaseModel):
    """User model with authentication attributes"""

    def __init__(self, *args, **kwargs):
        """Initializes a User instance with attributes from kwargs"""
        super().__init__(*args, **kwargs)

        # Set default values if not provided in kwargs
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
